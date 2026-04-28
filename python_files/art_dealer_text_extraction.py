# This script aims to collect any relevant text from the wbepages that were identified for artifacts. The objective is a further step to compare text and images from both sources: yemeni national authority and art dealers platforms artifacts. 

# Imports
import argparse
import html
import re
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

tqdm.pandas()


# Directories and parameters
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# dry run testing
DRY_RUN = True
MAX_PAGES_PER_DRY_RUN = 1
OUTPUT_CSV = BASE_DIR / "data" / "raw" / "dry_run_wartefacts_with_web.csv"

INPUT_CSV = BASE_DIR / "data" / "raw" / "web_links.csv" # output from data cleaning notebook
#OUTPUT_CSV = BASE_DIR / "data" / "raw" / "artefacts_with_web.csv"

# Delimiter csv
INPUT_SEP = ";"

# Timeout HTTP (avoid blocking)
TIMEOUT = 20

# Max length characters
MAX_OUTPUT_CHARS = 5000

# Headers HTTP  
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}


# Deleting Tags HTML out of scope

BAD_TAGS = [
    "script", "style", "noscript", "svg", "img", "header", "footer",
    "nav", "aside", "form", "button", "input", "iframe"
]

# Regex to detect useless content (UI, cookies...)

BAD_TEXT_PATTERNS = re.compile(
    r"cookie|privacy|newsletter|subscribe|sign in|login|register|"
    r"facebook|instagram|twitter|linkedin|youtube|tiktok|"
    r"all rights reserved|accept cookies|manage preferences|"
    r"breadcrumb|skip to content|terms of use",
    flags=re.IGNORECASE
)

# Key words for scoring text
GOOD_KEYWORDS = re.compile(
    r"artifact|object|statue|head|bust|figure|figurine|relief|stela|stele|coin|"
    r"bowl|vessel|jar|amphora|bronze|marble|limestone|terracotta|ceramic|iron|"
    r"roman|greek|egyptian|byzantine|sudarabian|hellenistic|century|dated|period|"
    r"provenance|dimensions|height|width|depth|cm|inches|lot",
    flags=re.IGNORECASE
)

# Text cleaning
def normalize_text(text):
    """
    Basic :
    - decode HTML (&nbsp; etc.)
    - delete URLs
    - remove too many spaces
    """
    if text is None:
        return ""

    text = html.unescape(str(text))
    text = text.replace("\xa0", " ")  #non-standard spaces
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)  #urls
    text = re.sub(r"\s+", " ", text).strip()  #spaces
    return text


def looks_like_javascript_page(text):
    """
    detect js
    """
    text = (text or "").lower()
    signals = [
        "enable javascript",
        "javascript is required",
        "please turn javascript on",
        "app-root",
        "__next",
        "window.__",
    ]
    return any(signal in text for signal in signals)


# Html cleaning
def remove_bad_nodes(soup):
    """
    delte useless html (scripts, nav, etc.)
    """
    for tag_name in BAD_TAGS:
        for node in soup.find_all(tag_name):
            node.decompose()

# Scoring html blocks
def score_block(tag):
    """
   Score an html block if relevant content like object description
    """
    text = normalize_text(tag.get_text(" ", strip=True))

    if not text:
        return -10_000

    text_len = len(text)

    # shortness threshold
    if text_len < 80:
        return -1000

    # simple features
    p_count = len(tag.find_all("p"))
    li_count = len(tag.find_all("li")) #list like table
    heading_count = len(tag.find_all(["h1", "h2", "h3"]))

    keyword_hits = len(GOOD_KEYWORDS.findall(text[:3000])) #count good keywords
    bad_hits = len(BAD_TEXT_PATTERNS.findall(text[:1500])) #count bad keywords, suaully at the beginning

    # "UI" penalty
    penalty = 300 * bad_hits

    # global score
    score = (
        text_len
        + p_count * 120
        + li_count * 30
        + heading_count * 40
        + keyword_hits * 100
        - penalty
    )

    return score


# Split blocks: Split the text into sentence-like chunks, then keep only long, relevant, and non-duplicate pieces
def split_into_chunks(text):
    """
    Split a text in relevant chunks (sentences/blocs)
    remove noize and duplicates
    """
    text = normalize_text(text)
    if not text:
        return []

    chunks = re.split(r"(?<=[\.\!\?])\s+|\s{2,}", text) #based on sentends ends

    cleaned = []
    seen = set()

    for chunk in chunks:
        chunk = normalize_text(chunk)

        if len(chunk) < 40: #like ok, share
            continue
        if BAD_TEXT_PATTERNS.search(chunk): #useful
            continue
        if chunk in seen: #unique
            continue

        seen.add(chunk)
        cleaned.append(chunk)

    return cleaned


# Final data cleaning
def post_clean(text):
    text = normalize_text(text)
    # remove boilerplates
    text = re.sub(r"\bLOT\s*-\s*ART\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bshare\b|\bprint\b|\bdownload\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:MAX_OUTPUT_CHARS]


# Final extraction
def extract_candidate_blocks(soup):
    # get most likely relevant text blocs
    selectors = [
        "article", "main", '[role="main"]',
        ".content", ".main-content", ".post-content",
        ".entry-content", ".object-description",
        ".lot-description", ".product-description",
        ".description", ".article-body",
        "#content", "#main",
    ]

    candidates = []

    for sel in selectors:
        candidates.extend(soup.select(sel))

    # fallback wider if nothing found or text < 40
    if not candidates:
        candidates = soup.find_all(["section", "div"], limit=500)

    return candidates

# Pipeline to extract relevant text
def extract_best_text_from_html(html_text):
    # apply html cleaning
    soup = BeautifulSoup(html_text, "html.parser")
    remove_bad_nodes(soup)

    candidates = extract_candidate_blocks(soup)
    
    # scoring text
    scored = [(score_block(tag), tag) for tag in candidates if score_block(tag) > 0]

    if not scored:
        return post_clean(soup.get_text(" ", strip=True))

    scored.sort(reverse=True, key=lambda x: x[0])

    # top 3 blocs
    top_texts = []
    seen = set()

    for _, tag in scored[:20]:
        txt = normalize_text(tag.get_text(" ", strip=True))
        if txt and txt not in seen:
            seen.add(txt)
            top_texts.append(txt)
        if len(top_texts) == 3:
            break

    combined = " ".join(top_texts)

    # create chunks
    chunks = split_into_chunks(combined)

    # scoring chunks
    ranked = sorted(
        [(len(c) + len(GOOD_KEYWORDS.findall(c)) * 80, c) for c in chunks],
        reverse=True
    )

    # keep most relevant
    final = []
    total_len = 0

    for _, chunk in ranked:
        if total_len + len(chunk) > MAX_OUTPUT_CHARS:
            continue
        final.append(chunk)
        total_len += len(chunk)
        if len(final) >= 8:
            break

    return post_clean(" ".join(final))


# Scraping the link provided and get the best text
def scrape_text(url):
    if pd.isna(url) or not str(url).strip():
        return ""

    try:
        response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
        response.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    remove_bad_nodes(soup)

    # main extraction
    extracted = extract_best_text_from_html(response.text)

    # fallback JS 
    if len(extracted) < 120:
        visible = normalize_text(soup.get_text(" ", strip=True))
        if looks_like_javascript_page(visible):
            return "[JS_PAGE_OR_POOR_EXTRACTION]"
        return visible[:MAX_OUTPUT_CHARS]

    return extracted


# Global pipeline
def run(input_csv, output_csv, sep, dry_run=False):
    """
    full pipeline :
    - load csv
    - scrape url
    - checks
    - export
    """
    df = pd.read_csv(input_csv, sep=sep, encoding="utf-8-sig")

    if "link" not in df.columns:
        raise ValueError("Column link missing.")

    if dry_run:
        df = df.head(5)   
        print(f"[DRY RUN] Scraping only {len(df)} pages")
    
    else:
        df["text_for_matching_web"] = df["link"].progress_apply(scrape_text)
        df["web_text_len"] = df["text_for_matching_web"].str.len()

    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"\nSaved : {output_csv}")

# note:\n for new line

# Command line interface (CLI)
#python art_dealers_text_extraction.py 

def main():
    parser = argparse.ArgumentParser(description="Web scraping text artefacts")
    parser.add_argument("--input", default=INPUT_CSV)
    parser.add_argument("--output", default=OUTPUT_CSV)
    parser.add_argument("--sep", default=INPUT_SEP)

    args = parser.parse_args()

    run(args.input, args.output, args.sep, dry_run=DRY_RUN)


if __name__ == "__main__":
    main()