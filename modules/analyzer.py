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
    return df

def find_arbitrage(df):
    avg_ppsqft=df["price_per_sqft"].mean()
    threshold=avg_ppsqft*0.85###this may not be accurate but hit the sweet spot below 15% market
    df["is_undervalued"]=df["price_per_sqft"]<threshold
    arbitrage_df=df[df["is_undervalued"]==True]
    print("Undervalued Properties(Arbitrage Opportunities):")
    
    print(arbitrage_df)
    return arbitrage_df

def save_arbitrage(arbitrage_df):
    conn=sqlite3.connect(DB_PATH)
    arbitrage_df.to_sql(
        "arbitrage_opprotunities",
        conn,
        if_exists="replace",
        index=False
    )
    conn.close()
    print("\nSaved to the table:arbitrage_opportunities")
    



if __name__ == "__main__":
    df = load_data()
    basic_analysis(df)
    arbitrage_df=find_arbitrage(df)
    save_arbitrage(arbitrage_df)
