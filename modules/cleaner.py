import pandas as pd
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "raw_properties.csv")
CLEANED_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned", "cleaned_properties.csv")

def clean_properties():
    df = pd.read_csv(RAW_PATH)
    df["price_per_sqft"] = df["price"] / df["area"]
    average_price=df["price_per_sqft"].mean()
    df["undervalued"]=df["price_per_sqft"]<average_price

    os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
    df.to_csv(CLEANED_PATH, index=False)  # <- fixed typo
    print(f"Cleaned data saved to {CLEANED_PATH}")

if __name__ == "__main__":
    clean_properties()
