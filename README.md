# Looted Artefacts Detection — Yemen

## Project Overview

This project explores how data science and AI can support the identification and tracking of looted cultural artefacts from Yemen.

It focuses on building a reproducible pipeline to:
- extract data (text and images) from heterogeneous sources (PDF catalogues and web platforms)
- structure and store this data
- compare artefacts using embedding techniques
- detect potential matches between catalogued artefacts and objects found online

---

## Context

Since 1994, the Yemeni National Authority for Antiquities and Museums have been documenting looted artefacts through catalogues. 
With the ongoing conflict, the destruction of heritage sites and the illicit trafficking of artefacts have intensified.

This project aims to contribute to ongoing efforts in:
- archaeological research
- cultural heritage protection
- combating illicit art trafficking

---

##  Pipeline Overview

The project is based on a full data pipeline:

1. **PDF Processing**
   - Extraction of artefacts (text + images)
   - Creation of structured "artefact chunks"

2. **Web Scraping**
   - Collection of data from auction websites and blogs
   - Extraction of text and images

3. **Data Wrangling**
   - Cleaning and restructuring data
   - Tokenization and translation (HuggingFace & OpenAI Transformers)
   - Standardization of artefact descriptions

4. **Embedding / Vectorization**
   - Transformation of text and images into high-dimensional vectors
   - Use of embeddings to capture semantic meaning

5. **Storage**
   - SQL database (MySQL → migrated to Cloud SQL)
   - Vector database (Chroma) for similarity search

6. **Similarity Analysis**
   - Cosine distance to compare artefacts
   - Matching between catalogue data and online objects

---

##  Technologies Used

### Models & NLP
- OpenAI (GPT models)
- HuggingFace Transformers (MarianMT for translation)
- SentenceTransformers (MiniLM) / OpenCLIP (embeddings)

### Data Processing
- Python (pandas, numpy, maplotlib)
- PyMuPDF / pdfplumber (PDF extraction)
- BeautifulSoup / requests (web scraping)
- Intensive use of regex

### Databases
- MySQL (relational database)
- ChromaDB (vector database)

---

##  Dataset

- ~1125 artefacts from catalogues
- ~985 images extracted from PDFs
- ~200 textual descriptions
- ~240 images compared

---

## Results

- Strong similarity observed in text due to semantic proximity 
- High image similarity partly influenced by reused or duplicated images
- Outliers highlight mismatches and data inconsistencies

---

## Limitations

- General-purpose embedding models (not domain-specific)
- Heterogeneous and incomplete data sources
- Missing original archival images
- Some artefacts may already be in private collections

---

## Future Work

- Develop domain-specific embedding models (archaeology-focused)
- Improve webscraping extraction
- Enrich dataset with additional image sources
- Improve matching accuracy
- Deploy an API for querying and tracking artefacts

---

## Key Insight

By integrating heterogeneous data sources (PDFs, web content, and images), this project highlights how data pipelines can uncover relationships between artefacts, actors, and geographic patterns.

The matching process provides a foundation for identifying potential links in looted artefact networks.

This type of pipeline can support researchers, institutions, and investigators working on cultural heritage preservation and restitution.

This project reveals a structural gap in current data tools: they are largely designed for English, structured, and business-oriented data.

When applied to multilingual and culturally complex contexts, these tools struggle to capture, connect, and interpret information.

Bridging this gap is key to building more inclusive and globally relevant data systems.


---



## Project Structure

.
├── data/                              # Project datasets
│   ├── raw/                           # Raw, unprocessed data
│   │   ├── pdf_webscraping/
│   │   │   ├── only_pdfs_with_pictures/
│   │   │   └── pdf_files/
│   │   │
│   │   └── pdf_artifact_extraction/
│   │
│   └── clean/                         # Cleaned and structured datasets
│       ├── art_dealers.csv
│       ├── looted_artefacts.csv
│       ├── match_scoring.csv
│       ├── pdf_images.csv
│       ├── web_pages.csv
│       └── web_photos.csv

├── figures/                           # Generated visualizations
│   ├── bplo.png
│   ├── hist.png
│   ├── icones.png
│   ├── mapbocmap.png
│   ├── score_bplots.png
│   ├── score_histograms.png
│   ├── Yemenite_Looted_Artefacts_ERM.png
│   ├── ref.txt
│   │
│   ├── pdf_images/                    # Extracted images from PDFs (on request)
│   └── web_photos/                    # Scraped web images (on request)

├── notebooks/                         # Analysis and processing notebooks
│   ├── 01_pdf_webscraping.ipynb
│   ├── 02_pdf_image_extraction.ipynb
│   ├── 03_web_image_extraction.py
│   ├── 04_vector_database.ipynb
│   ├── data_cleaning.ipynb
│   │
│   └── chroma_db/                     # Local vector database
│       └── chroma.sqlite3

├── functions/                         # Reusable Python functions
│   └── extract_web_images.py

├── slides/                            # Presentation materials
│   ├── presentation.pdf               # Tableau dashboard export
│   ├── website_cities_metadata.xlsx
│   └── prezi_link.txt

├── sql_scripts/                       # SQL scripts for database setup & queries
│   ├── create_db.sql
│   ├── load_data.sql
│   ├── output_data.sql
│   ├── initial_schema.sql
│   │
│   └── dump/                          # Database exports and updates
│       ├── looted_artefacts_dump.sql
│       └── data_cleaning_updates.sql

└── src/                               # Core project source code

---

## Project Resources

| Resource | Link |
|--------|------|
| Looted Artefacts Database | https://goam.gov.ye/Looted |
| Project Management (Trello) | https://trello.com/b/0ixAwwVG/final-project |
| Project Presentation | https://prezi.com/view/xHVJrrxd9lEARBQZGtH7/ |
| Roadmap | https://miro.com/app/board/uXjVGm7gUdQ=/ |
| Data Visualization | https://public.tableau.com/views/final_project_17762709103470/Dashboard |


---

## Installation

```bash
git clone https://github.com/anneleschallierdelisle/final_project_looted_artefacts.git
cd final_project_looted_artefacts

# Create environment
uv venv
source ./venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt


## Author

Anne Leschallier de Lisle  