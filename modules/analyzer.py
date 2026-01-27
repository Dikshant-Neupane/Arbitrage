import sqlite3
import pandas as pd
from config.db_config import DB_PATH

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM properties", conn)
    conn.close()
    return df

def basic_analysis(df):
    print("\n" + "="*50)
    print("BASIC ANALYSIS")
    print("="*50)
    print(f"Total Properties: {len(df)}")

    # Ensure price is numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['area_sqft'] = pd.to_numeric(df['area_sqft'], errors='coerce')

    print(f"Average Price: ${df['price'].mean():,.2f}")
    print(f"Min Price: ${df['price'].min():,.2f}")
    print(f"Max Price: ${df['price'].max():,.2f}")

    # Calculate price_per_sqft if not already present
    if "price_per_sqft" not in df.columns and "area_sqft" in df.columns:
        df["price_per_sqft"] = df["price"] / df["area_sqft"]
    
    if "price_per_sqft" in df.columns:
        avg_ppsqft = df["price_per_sqft"].mean()
        if not pd.isna(avg_ppsqft):
            print(f"Average Price per Sqft: ${avg_ppsqft:,.2f}")
    
    return df

def find_arbitrage(df):
    print("\n" + "="*50)
    print("ARBITRAGE DETECTION")
    print("="*50)
    
    # Check if undervalued column already exists from cleaner
    if "undervalued" in df.columns:
        arbitrage_df = df[df["undervalued"] == True].copy()
    # Use price_per_sqft if area_sqft exists
    elif "area_sqft" in df.columns and "price_per_sqft" in df.columns:
        avg_ppsqft = df["price_per_sqft"].mean()
        threshold = avg_ppsqft * 0.85
        df["is_undervalued"] = df["price_per_sqft"] < threshold
        arbitrage_df = df[df["is_undervalued"] == True].copy()
    else:
        # Fallback to price-based detection
        avg_price = df["price"].mean()
        threshold = avg_price * 0.85
        df["is_undervalued"] = df["price"] < threshold
        arbitrage_df = df[df["is_undervalued"] == True].copy()

    print(f"Found {len(arbitrage_df)} undervalued properties (arbitrage opportunities)")
    if len(arbitrage_df) > 0:
        print("\nTop 10 Opportunities:")
        display_cols = ["title", "price", "area_sqft", "price_per_sqft", "location"]
        display_cols = [c for c in display_cols if c in arbitrage_df.columns]
        print(arbitrage_df[display_cols].head(10).to_string())
    return arbitrage_df

def save_arbitrage(arbitrage_df):
    conn = sqlite3.connect(DB_PATH)
    arbitrage_df.to_sql(
        "arbitrage_opportunities",  # fixed typo
        conn,
        if_exists="replace",
        index=False
    )
    conn.close()
    print("\nSaved to the table: arbitrage_opportunities")

if __name__ == "__main__":
    df = load_data()
    df = basic_analysis(df)
    arbitrage_df = find_arbitrage(df)
    save_arbitrage(arbitrage_df)
