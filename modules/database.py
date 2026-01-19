import sqlite3
import pandas as pd
from config.db_config import DB_PATH

def insert_properties():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_csv("data/cleaned/cleaned_properties.csv")

    conn.execute("DROP TABLE IF EXISTS properties")

    df.to_sql("properties", conn, if_exists="replace", index=False)

    conn.close()
    print("Database updated successfully")

if __name__ == "__main__":
    insert_properties()
