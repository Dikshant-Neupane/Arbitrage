# Arbitrage Real Estate Scanner

## Project Overview
The Arbitrage Real Estate Scanner is a Python-based automation tool designed to scrape real estate listings, clean and filter the data, and store it in a SQL database. The goal is to identify undervalued properties for potential investment opportunities.

The project demonstrates the full pipeline: data collection, processing, and storage.

---

## Folder Structure

```
Arbitrage_RealEstate/
│
├── config/
│   └── db_config.py          # Database connection settings
│
├── data/
│   ├── raw/                  # Raw scraped data (CSV/JSON)
│   └── cleaned/              # Cleaned and filtered data
│
├── modules/
│   ├── scraper.py            # Web scraping functions
│   ├── cleaner.py            # Data cleaning and filtering functions
│   └── database.py           # Functions to insert/query data in SQL
│
├── scripts/
│   ├── run_scraper.py        # Script to run scraping
│   ├── run_cleaner.py        # Script to clean data
│   └── run_db_update.py      # Script to save data in SQL
│
├── logs/
│   └── app.log               # Log file for errors and activity
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── main.py                   # Orchestrates full workflow
```

---

## Features

- Scrapes property listings from multiple websites.
- Cleans and filters data to identify undervalued properties.
- Stores processed data in a SQL database for querying.
- Modular design for easy updates and maintenance.

---

## Libraries & Tools Used

**Python Libraries:**
- `requests` – for HTTP requests to websites
- `BeautifulSoup` (`bs4`) – for parsing HTML pages
- `pandas` – for data cleaning and manipulation
- `numpy` – for numerical operations (optional if needed)
- `sqlite3` or `SQLAlchemy` – for database interaction
- `logging` – for application logging
- `os` – for file handling

**Tools:**
- Python 3.12+
- SQL database (SQLite/MySQL/PostgreSQL)
- VS Code or any Python IDE
- Git (optional, for version control)

---

## How to Run

1. Install required libraries:

```bash
pip install -r requirements.txt
```

2. Configure your database connection in `config/db_config.py`.

3. Run individual scripts:
   - Scraper: `python scripts/run_scraper.py`
   - Cleaner: `python scripts/run_cleaner.py`
   - Database update: `python scripts/run_db_update.py`

4. Or run the full pipeline with:

```bash
python main.py
```
