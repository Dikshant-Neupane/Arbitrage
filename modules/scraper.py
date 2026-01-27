import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

BASE_URL = "https://newyork.craigslist.org/search/rea"

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "raw_properties.csv")


def get_property_details(url, headers):
    """Scrape individual listing page for additional details."""
    area = None
    bedrooms = None
    bathrooms = None

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Try multiple selector patterns for details
        attr_groups = soup.select(".attrgroup span, .attrgroup li, .mapAndAttrs span")
        for elem in attr_groups:
            text = elem.text.lower()
            if "ft" in text or "sqft" in text:
                area = "".join(filter(str.isdigit, text))
            elif "br" in text:
                bedrooms = "".join(filter(str.isdigit, text))
            elif "ba" in text:
                bathrooms = "".join(filter(str.isdigit, text))

    except Exception as e:
        print(f"Detail scrape failed for {url}: {e}")

    return area, bedrooms, bathrooms


def scrape_properties(pages=3, delay=2, fetch_details=False):
    """
    Scrape Craigslist real estate listings.
    
    Args:
        pages: Number of pages to scrape
        delay: Delay between pages in seconds
        fetch_details: If True, fetches individual listing pages for more details (SLOW!)
    """
    listings = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for page in range(pages):
        start = page * 120
        url = f"{BASE_URL}?s={start}" if start > 0 else BASE_URL
        print(f"Scraping page {page+1}: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch page {page+1}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # New Craigslist structure uses different selectors
        # Try multiple possible selectors
        results = soup.select(".cl-static-search-result, .result-row, li.cl-search-result, .gallery-card")
        
        if not results:
            # Try finding all links that look like listings
            results = soup.select("a[href*='/reo/'], a[href*='/apa/'], a[href*='/rea/']")
        
        print(f"  Found {len(results)} listings on page {page+1}")

        for item in results:
            title = None
            price = None
            property_url = None
            location = None

            # Handle different element types
            if item.name == 'a':
                # Direct link element
                title = item.get_text(strip=True)
                property_url = item.get('href', '')
            else:
                # Container element - find nested elements
                title_tag = item.select_one(".title, .result-title, a")
                title = title_tag.get_text(strip=True) if title_tag else None
                
                link_tag = item.select_one("a[href]") or (title_tag if title_tag and title_tag.name == 'a' else None)
                property_url = link_tag.get('href', '') if link_tag else None

            # Extract price
            price_tag = item.select_one(".price, .result-price, .priceinfo")
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                price = re.sub(r'[^\d]', '', price_text)
            elif title:
                # Try to extract price from title
                price_match = re.search(r'\$?([\d,]+)', title)
                if price_match:
                    price = price_match.group(1).replace(',', '')

            # Extract location
            location_tag = item.select_one(".location, .result-hood, .meta")
            if location_tag:
                location = location_tag.get_text(strip=True).strip(" ()")

            # Make URL absolute if needed
            if property_url and not property_url.startswith('http'):
                property_url = f"https://newyork.craigslist.org{property_url}"

            # Skip if no valid data
            if not title and not property_url:
                continue

            # Try to extract area/bedrooms/bathrooms from title first (fast!)
            area, bedrooms, bathrooms = None, None, None
            if title:
                # Extract sqft - patterns like "1000sqft", "1,000 sq ft", "1000 ft2"
                sqft_match = re.search(r'([\d,]+)\s*(?:sq\.?\s*ft|sqft|ft2|sf)', title, re.IGNORECASE)
                if sqft_match:
                    area = sqft_match.group(1).replace(',', '')
                
                # Extract bedrooms - patterns like "3br", "3 br", "3 bed", "3 bedroom"
                br_match = re.search(r'(\d+)\s*(?:br|bed(?:room)?s?)\b', title, re.IGNORECASE)
                if br_match:
                    bedrooms = br_match.group(1)
                
                # Extract bathrooms - patterns like "2ba", "2 bath", "2 bathroom"
                ba_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:ba|bath(?:room)?s?)\b', title, re.IGNORECASE)
                if ba_match:
                    bathrooms = ba_match.group(1)

            # Only fetch details if we're missing area AND fetch_details is enabled
            if fetch_details and property_url and not area:
                fetched_area, fetched_br, fetched_ba = get_property_details(property_url, headers)
                area = area or fetched_area
                bedrooms = bedrooms or fetched_br
                bathrooms = bathrooms or fetched_ba
                time.sleep(0.5)  # Reduced delay

            listings.append({
                "title": title,
                "price": price,
                "area_sqft": area,
                "location": location,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "url": property_url
            })

        time.sleep(delay)

    df = pd.DataFrame(listings)
    
    # Ensure columns exist even if empty
    expected_columns = ["title", "price", "area_sqft", "location", "bedrooms", "bathrooms", "url"]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    df.to_csv(RAW_PATH, index=False)

    print("\nScraper finished successfully!")
    print(f"Total listings scraped: {len(df)}")
    print(df.head())


if __name__ == "__main__":
    scrape_properties(pages=3)
