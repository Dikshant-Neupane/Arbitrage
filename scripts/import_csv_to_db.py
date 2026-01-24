import sqlite3
import pandas as pd
import os
from config.db_config import DB_PATH  # your SQLite DB path

# Get the project root directory (parent of scripts folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def import_csv():
    db_path = os.path.join(PROJECT_ROOT, DB_PATH)
    csv_path = os.path.join(PROJECT_ROOT, "data", "raw", "raw_properties.csv")
    
    # Load scraped CSV
    df = pd.read_csv(csv_path)

    # Connect to SQLite and save as table 'properties'
    conn = sqlite3.connect(db_path)
    df.to_sql("properties", conn, if_exists="replace", index=False)
    conn.close()

    print("CSV imported into SQLite table: properties")

if __name__ == "__main__":
    import_csv()
