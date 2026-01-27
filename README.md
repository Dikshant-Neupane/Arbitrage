# Real Estate Arbitrage Scanner

A Python tool I built to find undervalued properties automatically. It scrapes Craigslist, cleans the data, and flags properties that are priced below market value.

## What it does

1. **Scrapes** - Pulls listings from Craigslist NY real estate
2. **Cleans** - Removes spam, rentals, duplicates. Calculates price/sqft
3. **Stores** - Saves everything to SQLite database
4. **Analyzes** - Finds properties below average price/sqft

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the whole pipeline
python main.py
```

That is it. Results go into the database.

## Project structure

```
 main.py              # Run this - executes full pipeline
 config/
    db_config.py     # Database path
 data/
    raw/             # Scraped data (unprocessed)
    cleaned/         # Cleaned data (ready for analysis)
 modules/
    scraper.py       # Scrapes Craigslist
    cleaner.py       # Cleans data, filters rentals
    database.py      # Saves to SQLite

   # Real Estate Arbitrage Scanner

   Professional, end-to-end ETL pipeline to discover undervalued real estate. It scrapes listings from Craigslist NY, cleans and enriches the data, stores it in SQLite, and flags opportunities based on price-per-square-foot analysis.

   ## Highlights

   - Automated scraping with resilient selectors (supports evolving Craigslist HTML)
   - Smart cleaning: rental filtering, deduplication, normalization
   - Location-aware price-per-sqft metrics and undervaluation detection
   - SQLite storage for history, reproducibility, and downstream analytics
   - Modular codebase with single-command pipeline run

   ## Repository Layout

   ```
   main.py                  # Orchestrates the full pipeline
   requirements.txt         # Project dependencies
   wrok_done.txt           # Progress log / changelog

   config/
      db_config.py          # SQLite database path configuration

   data/
      raw/
         raw_properties.csv  # Scraped listings (as-is)
      cleaned/
         cleaned_properties.csv  # Cleaned listings (ready for analysis)

   modules/
      scraper.py            # Scrapes listings (price, sqft, beds, baths, location, URL)
      cleaner.py            # Cleans, dedupes, categorizes, computes metrics & flags undervalued
      database.py           # Persists cleaned data into SQLite
      analyzer.py           # Loads DB, runs analysis, saves arbitrage opportunities

   scripts/
      run_scraper.py        # Optional: run only the scraper
      run_cleaner.py        # Optional: run only the cleaner
      run_db_updates.py     # Optional: run only DB updates
   ```

   ## Setup

   ### Prerequisites
   - Windows (tested), Python 3.12+

   ### Create venv and install
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

   ### Configuration
   SQLite path is set in [config/db_config.py](config/db_config.py):
   ```python
   DB_PATH = "data/properties.db"
   ```
   Change if you need a different database location.

   ## Usage

   ### Run the full pipeline
   ```bash
   python main.py
   ```
   This will:
   1) Scrape → write [data/raw/raw_properties.csv](data/raw/raw_properties.csv)
   2) Clean → write [data/cleaned/cleaned_properties.csv](data/cleaned/cleaned_properties.csv)
   3) Load → update `properties` table in SQLite
   4) Analyze → save `arbitrage_opportunities` table

   ### Run steps individually
   ```bash
   python scripts/run_scraper.py
   python scripts/run_cleaner.py
   python scripts/run_db_updates.py
   ```

   ## How It Works

   ### Scraper ([modules/scraper.py](modules/scraper.py))
   - Targets: https://newyork.craigslist.org/search/rea
   - Extracts: `title`, `price`, `area_sqft` (from title), `location`, `bedrooms`, `bathrooms`, `url`
   - Options: `fetch_details=False` by default (fast); enable to fetch per-listing pages for missing sqft

   ### Cleaner ([modules/cleaner.py](modules/cleaner.py))
   - Converts numeric fields
   - Filters rentals: `/reb/` URLs and prices < $100k
   - Deduplicates by `url` and by `title+price`
   - Categorizes property type (Commercial, Land, Multi-Family, etc.)
   - Computes `price_per_sqft` and location averages
   - Flags `undervalued` using location average; falls back to global average

   ### Database Loader ([modules/database.py](modules/database.py))
   - Writes cleaned data to `properties` table in [data/properties.db](data/properties.db)

   ### Analyzer ([modules/analyzer.py](modules/analyzer.py))
   - Loads `properties`, runs `basic_analysis()`
   - Builds arbitrage view from `undervalued` or computed thresholds
   - Saves to `arbitrage_opportunities` table

   ## Data Model

   ### Cleaned CSV Columns
   - `title` (str)
   - `price` (float)
   - `area_sqft` (float)
   - `price_per_sqft` (float)
   - `location` (str)
   - `bedrooms` (int, optional)
   - `bathrooms` (float, optional)
   - `property_type` (str)
   - `undervalued` (bool)
   - `avg_price_per_sqft_location` (float)
   - `url` (str)

   ### Database Tables
   - `properties`: mirrors cleaned CSV
   - `arbitrage_opportunities`: subset flagged as undervalued

   ## Example Output (Analyzer)

   ```
   Found 4 undervalued properties (arbitrage opportunities)

   Property                                 Price       $/SqFt   Location
   Commercial condo space , 22,000 sf       $2,000,000  $90.91    New York
   Prime Vacant Lot - 17,600 Sq Ft          $4,250,000  $241.48   Brooklyn
   ...                                      ...         ...       ...
   ```

   ## Notes & Limitations
   - Craigslist HTML changes frequently; selectors are maintained but may need updates
   - Title-based sqft extraction is heuristic; enable detail fetch for precision
   - Avoid aggressive scraping; respect robots and site policies

   ## Roadmap
   - Multi-source support (Zillow, Redfin)
   - Trend tracking and time-series analytics
   - Email/Slack alerts for new opportunities
   - Lightweight dashboard (Streamlit)
   - ML-assisted valuation

   ## Contributing
   Open to improvements—PRs welcome. Ideas: new sources, better heuristics, dashboards, alerting.

   ## License
   For educational and research purposes.

   ## Author
   Built to learn and apply Python, data engineering, and real estate analytics.


