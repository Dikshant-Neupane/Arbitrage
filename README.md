# Real Estate Arbitrage Scanner

## Project Overview

The **Real Estate Arbitrage Scanner** is an intelligent Python-based automation system that helps identify undervalued properties in the real estate market. Think of it as your personal real estate analyst that works 24/7!

### What Does This Project Do?

1. **Scrapes Real Estate Data** - Automatically collects property listings from websites
2. **Cleans & Structures Data** - Removes duplicates, fixes errors, and calculates important metrics
3. **Identifies Opportunities** - Uses market analysis to find properties priced below market value
4. **Stores Intelligence** - Saves everything in a database for future reference and trend analysis

This is a complete **ETL (Extract, Transform, Load) pipeline** for real estate investment research.

---

## Why This Project?

Finding undervalued properties manually is time-consuming. This tool automates the entire process, allowing you to:
- Save hours of manual research
- Make data-driven investment decisions
- Track market trends over time
- Identify arbitrage opportunities automatically

---

## Project Structure

```
REAL_STATE/
│
├── main.py                     # Main orchestrator - Run this to execute the full pipeline
├── README.md                   # You are here!
├── requirements.txt            # All Python dependencies listed
├── wrok_done.txt              # Development notes and progress tracking
│
├── config/                     # Configuration Files
│   └── db_config.py           # Database connection settings (SQLite path)
│
├── data/                       # Data Storage
│   ├── raw/                   # Raw scraped data (as-is from websites)
│   │   └── raw_properties.csv # Unprocessed property listings
│   └── cleaned/               # Cleaned and processed data
│       └── cleaned_properties.csv # Ready-to-analyze data
│
├── logs/                       # Application Logs
│   └── app.log                # Tracks errors, warnings, and execution history
│
├── modules/                    # Core Business Logic
│   ├── scraper.py             # Web scraping engine - Collects property data
│   ├── cleaner.py             # Data cleaning - Removes noise, adds metrics
│   ├── database.py            # Database operations - Insert/query properties
│   └── analyzer.py            # Market analysis - Identifies undervalued properties
│
└── scripts/                    # Individual Task Runners
    ├── run_scraper.py         # Run only the scraper
    ├── run_cleaner.py         # Run only the cleaner
    └── run_db_updates.py      # Run only database updates
```

---

## Key Features

### 1. Automated Data Collection
- Scrapes property listings from real estate websites
- Handles dynamic content and pagination
- Robust error handling for network issues

### 2. Intelligent Data Cleaning
- Removes duplicate listings
- Fixes formatting issues (price, area, location)
- Calculates **price per square foot** automatically
- Validates data integrity

### 3. Market Analysis
- Calculates market average for price per square foot
- Identifies properties priced **15% below market average**
- Flags undervalued opportunities with `is_undervalued` marker
- Supports custom threshold adjustments

### 4. Database Storage
- Stores all properties in SQLite database
- Easy to query and analyze historical data
- Supports data export for further analysis

### 5. Modular Architecture
- Each component works independently
- Easy to test, debug, and extend
- Clean separation of concerns

---

## Technologies & Libraries Used

### Core Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **requests** | 2.32.5 | HTTP requests to fetch web pages |
| **beautifulsoup4** | 4.14.3 | HTML parsing and web scraping |
| **pandas** | 2.3.3 | Data manipulation and analysis |
| **numpy** | 2.4.1 | Numerical operations and calculations |
| **sqlite3** | Built-in | Database storage and queries |

### Supporting Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **soupsieve** | 2.8.2 | CSS selectors for BeautifulSoup |
| **python-dateutil** | 2.9.0.post0 | Date parsing and manipulation |
| **pytz** | 2025.2 | Timezone handling |
| **urllib3** | 2.6.3 | HTTP connection pooling |
| **certifi** | 2026.1.4 | SSL certificate validation |

### Development Tools
- **Python 3.12+** - Programming language
- **SQLite** - Lightweight database (no separate installation needed)
- **VS Code** - Recommended IDE
- **Git** - Version control

---

## How to Get Started

### Step 1: Set Up Your Environment

First, create a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required libraries automatically!

### Step 3: Configure Database (Optional)

The default configuration uses SQLite and stores data in `data/properties.db`. 
If you want to change this, edit `config/db_config.py`:

```python
DB_PATH = "data/properties.db"  # Change this path if needed
```

### Step 4: Run the Full Pipeline

Simply run:

```bash
python main.py
```

This will:
1. Scrape properties from websites
2. Clean and process the data
3. Calculate price per square foot
4. Store everything in the database

### Step 5: Run Individual Components (Optional)

You can also run each step separately:

```bash
# Only scrape data
python scripts/run_scraper.py

# Only clean data
python scripts/run_cleaner.py

# Only update database
python scripts/run_db_updates.py
```

---

## How the Analysis Works

### Market-Based Pricing Logic

1. **Calculate Market Average**: The system calculates the average price per square foot across all properties
2. **Set Threshold**: Properties priced 15% below the market average are flagged
3. **Identify Opportunities**: These properties are marked as `is_undervalued = True`
4. **Store Intelligence**: Results are saved in the database for tracking

### Example:
- Market average: $200/sqft
- Threshold: $200 × 0.85 = $170/sqft
- Any property below $170/sqft is flagged as undervalued

---

## Project Phases

### Phase 1: Data Pipeline Foundation (Completed)
- Automated web scraping
- Data cleaning pipeline
- SQLite database integration
- One-command execution

### Phase 2: Market Analysis (Completed)
- Price per square foot calculation
- Undervaluation detection
- Arbitrage opportunity identification
- Structured intelligence storage

### Phase 3: Advanced Features (Upcoming)
- Multiple website support
- Price trend analysis
- Email alerts for new opportunities
- Interactive dashboard
- Machine learning price predictions

---

## Data Flow Diagram

```
Internet (Real Estate Websites)
          ↓
    [scraper.py]
          ↓
  data/raw/raw_properties.csv
          ↓
    [cleaner.py]
          ↓
  data/cleaned/cleaned_properties.csv
          ↓
    [database.py]
          ↓
  SQLite Database (data/properties.db)
          ↓
    [analyzer.py]
          ↓
  Arbitrage Opportunities Identified!
```

---

## Learning Outcomes

This project demonstrates mastery of:
- **Web Scraping**: Automated data collection
- **Data Engineering**: ETL pipeline design
- **Data Analysis**: Statistical analysis and market insights
- **Database Design**: Structured data storage
- **Python Programming**: Clean, modular code
- **Software Architecture**: Separation of concerns

---

## Contributing

Want to improve this project? Here are some ideas:
- Add support for more real estate websites
- Implement machine learning for better predictions
- Create a web dashboard for visualization
- Add email notifications for opportunities
- Improve scraping efficiency

---

## License

This project is for educational and research purposes.

---

## Author

Built to master Python, data engineering, and real estate analysis.

---

## Quick Links

- [requirements.txt](requirements.txt) - All dependencies
- [main.py](main.py) - Pipeline orchestrator
- [modules/](modules/) - Core logic
- [scripts/](scripts/) - Individual runners

---

**Ready to find your next real estate opportunity? Run `python main.py` and let the scanner do the work!**
