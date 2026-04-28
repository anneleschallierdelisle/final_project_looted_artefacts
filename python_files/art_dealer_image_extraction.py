# This script aims to collect any relevant image from the wbepages that were identified for artifacts. The objective is a further step to compare text and images from both sources: yemeni national authority and art dealers platforms artifacts. 

# Imports
import os
import re
import io
import time
import hashlib
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from tqdm import tqdm
from playwright.sync_api import sync_playwright


# Directories and parameters
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# dry run testing
DRY_RUN = True
MAX_PAGES_PER_DRY_RUN = 1
OUTPUT_DIR = BASE_DIR / "figures" / "dry_run_web_photos"
OUTPUT_CSV = BASE_DIR / "data" / "raw" / "dry_run_web_photos_manifest.csv"


INPUT_PATH = BASE_DIR / "data" / "raw" / "web_links.csv" # output from data cleaning notebook
#OUTPUT_DIR = BASE_DIR / "figures" / "web_photos"
#OUTPUT_CSV = BASE_DIR / "data" / "raw" / "web_photos_manifest.csv"

# Delimiter csv
INPUT_SEP = ";"

MAX_IMAGES_PER_PAGE = 3

# Timeout HTTP (avoid blocking)
REQUEST_TIMEOUT = 20
PLAYWRIGHT_TIMEOUT_MS = 25000
SLEEP_BETWEEN_PAGES = 0.2

# Image size
MIN_WIDTH = 250
MIN_HEIGHT = 250
MIN_FILE_BYTES = 8_000


# Headers HTTP  
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}


# image constraints

BAD_IMAGE_PATTERNS = re.compile(
    r"logo|icon|sprite|avatar|banner|ads?|thumb|thumbnail|"
    r"placeholder|favicon|social|facebook|instagram|twitter|"
    r"linkedin|youtube|tiktok|pixel|tracking|cookie|brand|"
    r"header|footer|nav|menu",
    flags=re.IGNORECASE
)

GOOD_IMAGE_PATTERNS = re.compile(
    r"object|artifact|art|lot|item|collection|museum|full|large|zoom|main|hero|image",
    flags=re.IGNORECASE
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# helpers

# several cleanings

def clean_text(text):
    return re.sub(r"\s+", " ", str(text or "")).strip()

# absolute url
def normalize_url(base_url, candidate_url): 
    if not candidate_url:
        return ""
    return urljoin(base_url, candidate_url.strip())

# longest url
def parse_srcset(srcset_value): 
    if not srcset_value:
        return ""
    parts = [p.strip() for p in srcset_value.split(",") if p.strip()]
    if not parts:
        return ""
    return parts[-1].split()[0].strip()


def image_extension_from_content_type(content_type):
    if not content_type:
        return ""
    content_type = content_type.lower()
    if "jpeg" in content_type or "jpg" in content_type:
        return ".jpg"
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "gif" in content_type:
        return ".gif"
    if "bmp" in content_type:
        return ".bmp"
    if "tiff" in content_type:
        return ".tiff"
    return ""


def image_extension_from_bytes(content):
    try:
        img = Image.open(io.BytesIO(content))
        fmt = (img.format or "").lower()
        if fmt == "jpeg":
            return ".jpg"
        if fmt:
            return f".{fmt}"
    except Exception:
        pass
    return ""

# build an image scoring threshold
def score_candidate(url, alt_text="", extra_text="", width=None, height=None, source="img"):
    blob = clean_text(f"{url} {alt_text} {extra_text}")
    score = 0

    if not url:
        return -10000

    if GOOD_IMAGE_PATTERNS.search(blob):
        score += 120
    if BAD_IMAGE_PATTERNS.search(blob):
        score -= 600

    if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", url, flags=re.I):
        score += 60

    try:
        if width and int(width) >= 400:
            score += 80
        if height and int(height) >= 400:
            score += 80
    except Exception:
        pass

    if source == "og:image": #main image of the site
        score += 300
    elif source == "twitter:image":
        score += 220
    elif source == "playwright_img":
        score += 140
    elif source == "img":
        score += 80

    return score

    
# extract images from html
def extract_candidates_from_soup(page_url, soup, source_label="img"):
    candidates = []

    # Meta images -> best place to get the most reliable content
    for meta in soup.find_all("meta"):
        prop = (meta.get("property") or meta.get("name") or "").strip().lower()
        content = (meta.get("content") or "").strip()

        if prop == "og:image" and content:
            candidates.append({
                "url": normalize_url(page_url, content),
                "alt": "",
                "extra": prop,
                "width": None,
                "height": None,
                "source": "og:image"
            })

        elif prop == "twitter:image" and content:
            candidates.append({
                "url": normalize_url(page_url, content),
                "alt": "",
                "extra": prop,
                "width": None,
                "height": None,
                "source": "twitter:image"
            })

    # Img tags
    for img in soup.find_all("img"):
        src = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-original")
            or img.get("data-lazy-src")
            or img.get("data-image")
            or ""
        ).strip()

        srcset = (img.get("srcset") or img.get("data-srcset") or "").strip()
        if srcset:
            src = parse_srcset(srcset) or src

        if not src:
            continue

        full = normalize_url(page_url, src)
        alt = clean_text(img.get("alt", ""))
        cls = " ".join(img.get("class", [])) if img.get("class") else ""
        ident = clean_text(img.get("id", ""))
        title = clean_text(img.get("title", ""))
        extra = clean_text(f"{cls} {ident} {title}")
        width = img.get("width")
        height = img.get("height")

        candidates.append({
            "url": full,
            "alt": alt,
            "extra": extra,
            "width": width,
            "height": height,
            "source": source_label
        })

    deduped = []
    seen = set()
    for c in candidates:
        u = c["url"]
        if not u or u in seen:
            continue
        seen.add(u)
        c["score"] = score_candidate(
            c["url"], c["alt"], c["extra"], c["width"], c["height"], c["source"]
        )
        deduped.append(c)

    deduped.sort(key=lambda x: x["score"], reverse=True)
    return deduped


# retrieve the image itself
def fetch_image_content(image_url):
    try:
        r = requests.get(image_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.content, r.headers.get("Content-Type", ""), ""
    except Exception as e:
        return None, None, str(e)

# keep image according to constraints
def validate_image(content):
    if content is None:
        return False, None, None, "no_content"

    if len(content) < MIN_FILE_BYTES:
        return False, None, None, "too_small_bytes"

    try:
        img = Image.open(io.BytesIO(content))
        width, height = img.size
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return False, width, height, "too_small_dimensions"
        return True, width, height, "ok"
    except Exception:
        return False, None, None, "invalid_image"

# create a unique filename
def build_filename(artifact_id, rank, image_url, content, ext):
    url_hash = hashlib.sha1(image_url.encode("utf-8")).hexdigest()[:10]
    content_hash = hashlib.sha1(content).hexdigest()[:12]
    safe_artifact = re.sub(r"[^A-Za-z0-9_-]+", "_", str(artifact_id))
    return f"{safe_artifact}_img{rank}_{url_hash}_{content_hash}{ext}"

# bad pattern identification
def looks_like_bad_image_candidate(candidate):
    blob = clean_text(f"{candidate['url']} {candidate['alt']} {candidate['extra']}")
    return bool(BAD_IMAGE_PATTERNS.search(blob))

# requesting url
def get_html_requests(page_url):
    try:
        r = requests.get(page_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.text, ""
    except Exception as e:
        return None, str(e)

# launch as a browser to get images (js, dynamic)
def get_candidates_playwright(page_url, browser):
    page = browser.new_page(user_agent=HEADERS["User-Agent"])
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT_MS)

    try:
        page.goto(page_url, wait_until="networkidle")
        page_html = page.content()
        soup = BeautifulSoup(page_html, "html.parser")
        candidates = extract_candidates_from_soup(page_url, soup, source_label="playwright_img")

        dom_imgs = page.locator("img")
        count = min(dom_imgs.count(), 80)

        extra_candidates = []
        for i in range(count):
            try:
                img = dom_imgs.nth(i)
                src = img.get_attribute("src") or img.get_attribute("data-src") or ""
                srcset = img.get_attribute("srcset") or ""
                if srcset:
                    src = parse_srcset(srcset) or src

                if not src:
                    continue

                full = normalize_url(page_url, src)
                alt = clean_text(img.get_attribute("alt") or "")
                cls = clean_text(img.get_attribute("class") or "")
                width = img.get_attribute("width")
                height = img.get_attribute("height")

                extra_candidates.append({
                    "url": full,
                    "alt": alt,
                    "extra": cls,
                    "width": width,
                    "height": height,
                    "source": "playwright_img",
                    "score": score_candidate(full, alt, cls, width, height, "playwright_img")
                })
            except Exception:
                pass

        all_candidates = candidates + extra_candidates

        deduped = []
        seen = set()
        for c in sorted(all_candidates, key=lambda x: x["score"], reverse=True):
            u = c["url"]
            if not u or u in seen:
                continue
            seen.add(u)
            deduped.append(c)

        return deduped, ""
    except Exception as e:
        return [], str(e)
    finally:
        page.close()

# keep best top 3
def download_best_images_for_page(artifact_id, page_url, browser=None):
    results = []

    try:
        html_text, req_err = get_html_requests(page_url)
        candidates = []

        if html_text:
            soup = BeautifulSoup(html_text, "html.parser")
            candidates = extract_candidates_from_soup(page_url, soup, source_label="img")

        if (len(candidates) < MAX_IMAGES_PER_PAGE) and browser is not None:
            js_candidates, _ = get_candidates_playwright(page_url, browser)
            merged = candidates + js_candidates

            deduped = []
            seen = set()
            for c in sorted(merged, key=lambda x: x["score"], reverse=True):
                u = c["url"]
                if not u or u in seen:
                    continue
                seen.add(u)
                deduped.append(c)
            candidates = deduped

        if not candidates:
            return [{
                "artifact_id": artifact_id,
                "source_page_url": page_url,
                "image_rank": None,
                "image_url": None,
                "image_name": None,
                "width": None,
                "height": None,
                "status": f"no_candidates | req_err={req_err}" if req_err else "no_candidates"
            }]

        kept = 0
        seen_hashes = set()

        for cand in candidates[:40]:
            if kept >= MAX_IMAGES_PER_PAGE:
                break

            if looks_like_bad_image_candidate(cand):
                continue

            image_url = cand["url"]
            content, content_type, img_err = fetch_image_content(image_url)
            if img_err:
                continue

            ok, width, height, _ = validate_image(content)
            if not ok:
                continue

            content_hash = hashlib.sha1(content).hexdigest()
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)

            ext = image_extension_from_content_type(content_type) or image_extension_from_bytes(content) or ".jpg"
            filename = build_filename(artifact_id, kept + 1, image_url, content, ext)
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(content)

            kept += 1
            results.append({
                "artifact_id": artifact_id,
                "source_page_url": page_url,
                "image_rank": kept,
                "image_url": image_url,
                "image_name": filename,
                "width": width,
                "height": height,
                "status": "downloaded"
            })

        if kept == 0:
            return [{
                "artifact_id": artifact_id,
                "source_page_url": page_url,
                "image_rank": None,
                "image_url": None,
                "image_name": None,
                "width": None,
                "height": None,
                "status": "no_valid_images"
            }]

        return results

    except Exception as e:
        return [{
            "artifact_id": artifact_id,
            "source_page_url": page_url,
            "image_rank": None,
            "image_url": None,
            "image_name": None,
            "width": None,
            "height": None,
            "status": f"error: {e}"
        }]


def main():
    df = pd.read_csv(INPUT_PATH, sep=INPUT_SEP, encoding="utf-8-sig")

    required_cols = {"artifact_id", "link"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    work_df = df.loc[
        df["link"].notna() & (df["link"].astype(str).str.strip() != ""),
        ["artifact_id", "link"]
    ].copy()

    print(f"Pages to process: {len(work_df)}")

    if DRY_RUN is True:
        work_df = work_df.head(MAX_PAGES_PER_DRY_RUN)
        print("[DRY RUN] Urls processed:")
        print(work_df.to_string(index=False))
        return

    all_rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for _, row in tqdm(work_df.iterrows(), total=len(work_df)):
            artifact_id = row["artifact_id"]
            page_url = str(row["link"]).strip()

            rows = download_best_images_for_page(
                artifact_id=artifact_id,
                page_url=page_url,
                browser=browser
            )
            all_rows.extend(rows)

            time.sleep(SLEEP_BETWEEN_PAGES)

        browser.close()

    manifest = pd.DataFrame(all_rows)

    if manifest.empty:
        print("No result.")
    else:
        manifest.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print("\nDone.")
        print("Images folder :", OUTPUT_DIR)
        print("Manifest CSV   :", OUTPUT_CSV)
        print("\nSummary status :")
        print(manifest["status"].value_counts(dropna=False).to_string())

    print("\nOverview :")
    print(manifest.head(10).to_string(index=False))
    print("INPUT_PATH:", INPUT_PATH)
    print("EXISTS:", INPUT_PATH.exists())


if __name__ == "__main__":
    main()