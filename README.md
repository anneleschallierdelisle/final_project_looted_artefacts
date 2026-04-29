# Looted Artefacts Detection — Yemen

## Project Overview

This project explores how data science and AI can support the identification and tracking of looted cultural artefacts from Yemen.

It focuses on building a reproducible pipeline to:
- extract data (text and images) from heterogeneous sources (PDF catalogues and web platforms)
- structure, store and expose this data
- compare artefacts using embedding techniques
- detect potential matches between catalogued artefacts and objects found online
- identify looted artefacts profiles and trajectories

---

## Context

Since 1994, the Yemeni National Authority for Antiquities and Museums have been documenting looted artefacts through catalogues. 
With the ongoing conflict, the destruction of heritage sites and the illicit trafficking of artefacts have intensified.
As a result, Yemen is at the second position of countries with the highest number (% and volume) of UNESCO World Heritage Sites in danger.

This project aims to contribute to ongoing efforts in:
- archaeological research
- cultural heritage protection
- fighting illicit art trafficking

---

##  Pipeline Overview

The project is based on a full data pipeline:

1. **PDF Processing**
   - Extraction of artefacts (text + images)
   - Creation of structured "artefact chunks"

2. **Web Scraping**
   - Collection of data from art dealers and commercial platforms
   - Extraction of text and images

3. **Data Wrangling**
   - Cleaning and restructuring data
   - Tokenization and translation (HuggingFace & OpenAI Transformers)
   - Standardization of artefact descriptions

4. **Embedding / Vectorization**
   - Transformation of text and images into high-dimensional vectors
   - Use of embeddings to capture semantic meaningand images similarity
     (SentenceTransformers MINI LM and CLIP for images)

5. **Storage and Access**
   - SQL database (MySQL → migrated to Cloud SQL)
   - API for querying and tracking artefacts
   - Vector database (Chroma) for similarity search

6. **Similarity Analysis**
   - Cosine distance to compare artefacts vectors
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
- API Flask app

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
```
├── config.yaml                # Project configuration settings
├── main.py                    # Main script to run project workflows
├── pyproject.toml             # Project dependencies and configuration
├── uv.lock                    # Dependency lock file
├── README.md                  # Project documentation

├── data/
│   ├── raw/                                        
│   │
│   └── clean/ 

├── notebooks/                          
│   ├── chroma_db/ 
│                       

├── python_files/                          
│ 
├── sql_scripts/                        
│   ├── dump/  
                            
├── figures/

├── slides_report/ 

├── src/
```
---


## Project Resources

| Resource | Link |
|--------|------|
| Yemeni Looted Artefacts Source | https://goam.gov.ye/Looted |
| Mola Artefacts source | https://mola.omeka.net |
| UNESCO World Cultural Heritage  | https://whc.unesco.org/en/list |
| API Documentation (local, in progress)  | http://127.0.0.1:5000 |
| Project Management (Trello) | https://trello.com/b/0ixAwwVG/final-project |
| Project Presentation | https://prezi.com/view/xHVJrrxd9lEARBQZGtH7/ |
| Roadmap | https://miro.com/app/board/uXjVGm7gUdQ=/ |
| Data Visualization | https://public.tableau.com/views/final_project_17762709103470/Dashboard |

## API Endpoints

| Resource                         | Link / Endpoint                                                                 | Description                                                                                          |
|----------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| Yemeni Looted Artefacts          | `GET /yemeni_looted_artefacts`                                                   | List and detailed descriptions of Yemeni looted artefacts (pagination: `limit`, `offset`)           |
| Single Artefact                  | `GET /yemeni_looted_artefacts/<artifact_id>`                                     | Get one artefact by ID                                                                                |
| Artefacts Scoring                | `GET /artefacts_scoring`                                                         | List artefact scoring and compare descriptions/images between sources (pagination supported)        |
| Search Looted Artefacts          | `GET /search_looted_artefacts`                                                   | Search Yemeni looted artefacts with filters (`country`, `normalized_domain`)                         |
| UNESCO Sites in Danger by State  | `GET /unesco_sites_in_danger/<states_name_en>`                                   | Get information about UNESCO sites in a country, especially those in danger                         |

---

## Data Restrictions & Compliance

- **No personal data (GDPR)**  
  This project does not process personal data. All information relates to cultural artefacts and public sources, and is therefore out of GDPR scope.

- **Image usage restrictions**  
  Images are not stored in the repository due to unclear ownership and copyright concerns. Only references (links/paths) are kept.


## Disclaimer

This project is for research and educational purposes only.  
The results do not constitute legal evidence and should not be used for enforcement without expert validation.


## Installation

```bash
git clone https://github.com/anneleschallierdelisle/final_project_looted_artefacts.git
cd final_project_looted_artefacts

# Create environment
uv venv
source ./venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run API locally
run flask_api.py in your terminal
API available at: http://127.0.0.1:5000

## Author

Anne Leschallier de Lisle  
