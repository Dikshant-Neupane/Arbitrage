import sys
sys.path.insert(0, '.')
from modules.database import insert_properties

if __name__ == "__main__":
    print("Updating database with cleaned data...")
    insert_properties()
    print("Database updated successfully!")
