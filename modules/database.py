import sqlite3
import pandas as pd
import os
from config.db_config import DB_PATH

# Get the project root directory (parent of modules folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def insert_properties():
    db_path = os.path.join(PROJECT_ROOT, DB_PATH)
    csv_path = os.path.join(PROJECT_ROOT, "data", "cleaned", "cleaned_properties.csv")
    
    conn = sqlite3.connect(db_path)

    df = pd.read_csv(csv_path)

    conn.execute("DROP TABLE IF EXISTS properties")

    df.to_sql("properties", conn, if_exists="replace", index=False)

    conn.close()
    print("Database updated successfully")

if __name__ == "__main__":
    insert_properties()
