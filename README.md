# Chicago Luxury Apartment Scraper
A data engineering + analytics project that tracks rental trends of luxury apartment buildings in Downtown Chicago over time.
This project collects structured unit-level data (rent, availability, floorplan, unit number, etc.), stores historical snapshots, and enables time-series analysis of pricing dynamics in high-end residential markets.

## Goals
The primary objectives of this project are:
1. Track rent trends at the unit level over time
2. Capture detailed unit information:
  Unit number
  Floorplan
  Bedrooms / Bathrooms
  Square footage
  Date available
  Listed rent
3. Build a historical dataset for longitudinal analysis
4. Enable downstream analytics (price distribution, seasonal trends, building comparison)
This project is designed as a reusable and extensible scraping + data pipeline system.

## Features
Automated scraping of Chicago luxury apartment listings
Unit-level structured data extraction
Timestamped snapshots for historical tracking
CSV export for analysis
Designed to extend to database integration (PostgreSQL, etc.)
Clean, modular scraping architecture

## Pipeline Overview
High-level workflow:
Extract: Scrapy spiders crawl apartment listing endpoints/pages
Transform: Normalize/clean raw fields into consistent schema
Load: Persist snapshot data to storage (CSV and/or database)
Orchestrate: Run recurring jobs via DAGs to build a longitudinal dataset

## Project Structure
.
├── RentScrape/\n
│   ├── loaders/            # Data sinks (e.g., CSV writer, DB writer)\n
│   ├── spiders/            # Scrapy spiders: request + parse listing data
│   ├── transformers/       # Field normalization / schema standardization
│   ├── __init__.py
│   ├── items.py            # Scrapy Items (record schema)
│   ├── middlewares.py      # Scrapy downloader/spider middlewares
│   ├── pipelines.py        # Scrapy pipelines (post-processing + persistence hooks)
│   └── settings.py         # Scrapy project settings
│
├── dags/                   # Scheduled workflow definitions (e.g., Airflow DAGs)
├── models/                 # Database models / schema definitions
│   ├── __init__.py
│   └── db.py               # DB connection/session utilities
│
├── scrapy.cfg              # Scrapy config entry
├── docker-compose.yaml     # Local infra (e.g., DB service) for development
├── Pipfile                 # Python dependencies (pipenv)
├── Pipfile.lock
├── pyproject.toml          # Tooling config (formatters, linters, build metadata)
├── __init__.py
└── .gitignore

## Using the Project Yourself
### Data Model
Records are defined via Scrapy items.py and (optionally) database models in models/.
Typical fields include:
- building_name
- unit_number
- floorplan
- rent
- availability_date
- scrape_timestamp
- (optional) sqft, bedrooms, bathrooms, etc.
Each run produces a full snapshot of units currently listed. Historical analysis is performed by comparing records across scrape timestamps.

### Setup
1. Clone the repo
2. Run ```pipenv install -r requirements.txt``` then ```pipenv shell (note: requires pipenv be installed first)
3. In the terminal, change directory to be in RentScrape
4. Run ```python dags/{building dag}.py --crawl --tl
