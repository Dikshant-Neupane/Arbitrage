import sys
sys.path.insert(0, '.')
from modules.scraper import scrape_properties

if __name__ == "__main__":
    print("Starting scraper...")
    scrape_properties()
    print("Scraper finished and saved to data/raw/raw_properties.csv")
