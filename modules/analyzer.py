import sqlite3
import pandas as pd
from config.db_config import DB_PATH

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM properties", conn)
    conn.close()
    return df

def basic_analysis(df):
    print("Total Properties:", len(df))
    print("Average Price:", df["price"].mean())
    print("Min Price:", df["price"].min())
    print("Max Price:", df["price"].max())

    if "area" in df.columns:
        df["price_per_sqft"] = df["price"] / df["area"]
        print("Average Price per Sqft:", df["price_per_sqft"].mean())

if __name__ == "__main__":
    df = load_data()
    basic_analysis(df)
