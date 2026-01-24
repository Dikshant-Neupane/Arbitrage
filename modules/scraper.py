import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import json

BASE_URL = "https://newyork.craigslist.org/search/rea"

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "raw_properties.csv")

def scrape_properties(pages=3, delay=2):
    listings = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for page in range(pages):
        start = page * 120
        url = f"{BASE_URL}?s={start}" if start > 0 else BASE_URL
        print(f"Scraping page {page+1}: {url}")

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Craigslist now uses JSON-LD structured data
        json_script = soup.find("script", {"id": "ld_searchpage_results"})
        
        if json_script:
            try:
                data = json.loads(json_script.string)
                items = data.get("itemListElement", [])
                
                for item in items:
                    property_data = item.get("item", {})
                    address = property_data.get("address", {})
                    
                    title = property_data.get("name", "")
                    location = f"{address.get('addressLocality', '')}, {address.get('addressRegion', '')}"
                    property_type = property_data.get("@type", "")
                    
                    # Try to get price and area if available
                    price = property_data.get("price", None)
                    area = property_data.get("floorSize", {}).get("value", None) if isinstance(property_data.get("floorSize"), dict) else None
                    bedrooms = property_data.get("numberOfBedrooms", None)
                    bathrooms = property_data.get("numberOfBathroomsTotal", None)
                    
                    listings.append({
                        "title": title,
                        "price": price,
                        "area": area,
                        "location": location.strip(", "),
                        "property_type": property_type,
                        "bedrooms": bedrooms,
                        "bathrooms": bathrooms
                    })
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")

        time.sleep(delay)

    df = pd.DataFrame(listings)

    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    df.to_csv(RAW_PATH, index=False)

    print(f"\nScraper finished!")
    print(f"Total listings scraped: {len(df)}")
    print(df.head())
