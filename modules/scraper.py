import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

RAW_PATH = "data/raw/raw_properties.csv"

def scrape_properties():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.select(".quote")

    data = []

    for i, q in enumerate(quotes):
        title = q.select_one(".text").get_text(strip=True)
        price = 100000 + i * 10000        # fake price
        area = 500 + i * 20               # fake area
        location = "Test City"

        data.append({
            "title": title,
            "price": price,
            "area": area,
            "location": location
        })

    df = pd.DataFrame(data)

    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    df.to_csv(RAW_PATH, index=False)

    print(f"Scraped data saved to {RAW_PATH}")

if __name__ == "__main__":
    scrape_properties()
