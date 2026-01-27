import pandas as pd
import numpy as np
import os
import re

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "raw_properties.csv")
CLEANED_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned", "cleaned_properties.csv")


def extract_from_title(title):
    """Extract price, area, bedrooms, bathrooms from title text."""
    if not title or pd.isna(title):
        return None, None, None, None
    
    # Extract sqft
    sqft_match = re.search(r'([\d,]+)\s*(?:sq\.?\s*ft|sqft|ft2|sf)', title, re.IGNORECASE)
    area = int(sqft_match.group(1).replace(',', '')) if sqft_match else None
    
    # Extract bedrooms
    br_match = re.search(r'(\d+)\s*(?:br|bed(?:room)?s?)\b', title, re.IGNORECASE)
    bedrooms = int(br_match.group(1)) if br_match else None
    
    # Extract bathrooms
    ba_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:ba|bath(?:room)?s?)\b', title, re.IGNORECASE)
    bathrooms = float(ba_match.group(1)) if ba_match else None
    
    return area, bedrooms, bathrooms


def clean_properties():
    """Clean and optimize property data for analysis."""
    print("Starting data cleaning...")
    
    # Check if raw file exists and has data
    if not os.path.exists(RAW_PATH):
        print(f"Error: Raw data file not found at {RAW_PATH}")
        return None
    
    try:
        df = pd.read_csv(RAW_PATH)
    except pd.errors.EmptyDataError:
        print("Error: Raw data file is empty. No data to clean.")
        return None
    
    if df.empty or len(df) == 0:
        print("Warning: No listings found in raw data. Nothing to clean.")
        return None
    
    print(f"Loaded {len(df)} raw listings")
    
    # ===== 1. CLEAN NUMERIC COLUMNS =====
    df["price"] = pd.to_numeric(df["price"], errors='coerce')
    df["area_sqft"] = pd.to_numeric(df["area_sqft"], errors='coerce')
    df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors='coerce')
    df["bathrooms"] = pd.to_numeric(df["bathrooms"], errors='coerce')
    
    # ===== 2. TRY TO EXTRACT MISSING DATA FROM TITLE =====
    for idx, row in df.iterrows():
        if pd.isna(row["area_sqft"]) or pd.isna(row["bedrooms"]) or pd.isna(row["bathrooms"]):
            area, br, ba = extract_from_title(row["title"])
            if pd.isna(row["area_sqft"]) and area:
                df.at[idx, "area_sqft"] = area
            if pd.isna(row["bedrooms"]) and br:
                df.at[idx, "bedrooms"] = br
            if pd.isna(row["bathrooms"]) and ba:
                df.at[idx, "bathrooms"] = ba
    
    # ===== 3. CLEAN LOCATION =====
    df["location"] = df["location"].str.strip().str.title()
    df["location"] = df["location"].replace(['', 'None', 'Nan'], np.nan)
    
    # ===== 4. REMOVE INVALID/SPAM LISTINGS =====
    initial_count = len(df)
    
    # Remove $0 listings (likely spam or placeholder)
    df = df[df["price"] > 0]
    
    # Remove rentals: filter by URL pattern (/reb/ often contains rentals)
    # Keep only /reo/ (real estate by owner - for sale)
    if "url" in df.columns:
        df["is_rental"] = df["url"].str.contains("/reb/", na=False) & (df["price"] < 100000)
        df = df[~df["is_rental"]]
        df = df.drop(columns=["is_rental"])
    
    # Remove extremely low prices (likely rentals, not real estate sales)
    df = df[df["price"] >= 50000]  # Minimum $50k for real estate sales
    
    # Remove duplicates based on URL
    df = df.drop_duplicates(subset=["url"], keep="first")
    
    # Remove duplicates based on title + price
    df = df.drop_duplicates(subset=["title", "price"], keep="first")
    
    print(f"Removed {initial_count - len(df)} invalid/duplicate/rental listings")
    
    # ===== 5. CALCULATE DERIVED METRICS =====
    # Price per sqft (only where both values exist)
    df["price_per_sqft"] = np.where(
        (df["area_sqft"] > 0) & (df["price"] > 0),
        df["price"] / df["area_sqft"],
        np.nan
    )
    
    # ===== 6. IDENTIFY UNDERVALUED PROPERTIES =====
    # Calculate by location for more accurate comparison
    df["avg_price_per_sqft_location"] = df.groupby("location")["price_per_sqft"].transform("mean")
    df["undervalued"] = df["price_per_sqft"] < df["avg_price_per_sqft_location"]
    
    # Global average fallback
    global_avg = df["price_per_sqft"].mean()
    df["undervalued"] = df["undervalued"].fillna(df["price_per_sqft"] < global_avg)
    
    # ===== 7. CATEGORIZE PROPERTY TYPE =====
    def categorize_property(title):
        if pd.isna(title):
            return "Unknown"
        title_lower = title.lower()
        if any(x in title_lower for x in ["commercial", "retail", "office", "storefront"]):
            return "Commercial"
        elif any(x in title_lower for x in ["land", "lot", "acres"]):
            return "Land"
        elif any(x in title_lower for x in ["multi", "family", "duplex", "triplex"]):
            return "Multi-Family"
        elif any(x in title_lower for x in ["condo", "coop", "co-op", "apartment"]):
            return "Condo/Co-op"
        elif any(x in title_lower for x in ["house", "home", "single"]):
            return "Single Family"
        else:
            return "Other"
    
    df["property_type"] = df["title"].apply(categorize_property)
    
    # ===== 8. CLEAN UP COLUMNS =====
    # Round numeric columns
    df["price_per_sqft"] = df["price_per_sqft"].round(2)
    df["avg_price_per_sqft_location"] = df["avg_price_per_sqft_location"].round(2)
    
    # Reorder columns
    column_order = [
        "title", "price", "area_sqft", "price_per_sqft", "location", 
        "bedrooms", "bathrooms", "property_type", "undervalued", 
        "avg_price_per_sqft_location", "url"
    ]
    df = df[[col for col in column_order if col in df.columns]]
    
    # Sort by potential value (undervalued first, then by price)
    df = df.sort_values(by=["undervalued", "price_per_sqft"], ascending=[False, True])
    
    # ===== 9. SAVE CLEANED DATA =====
    os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
    df.to_csv(CLEANED_PATH, index=False)
    
    # ===== 10. PRINT SUMMARY =====
    print(f"\n{'='*50}")
    print("CLEANING COMPLETE!")
    print(f"{'='*50}")
    print(f"Total cleaned listings: {len(df)}")
    print(f"Listings with area_sqft: {df['area_sqft'].notna().sum()}")
    print(f"Undervalued properties: {df['undervalued'].sum()}")
    print(f"\nProperty Types:")
    print(df["property_type"].value_counts().to_string())
    print(f"\nPrice Range: ${df['price'].min():,.0f} - ${df['price'].max():,.0f}")
    if not pd.isna(global_avg):
        print(f"Avg Price/SqFt: ${global_avg:,.2f}")
    print(f"\nCleaned data saved to: {CLEANED_PATH}")
    
    return df


if __name__ == "__main__":
    clean_properties()
