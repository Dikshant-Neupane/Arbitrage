import sys
sys.path.insert(0, '.')
from modules.cleaner import clean_properties

if __name__ == "__main__":
    print("Starting cleaner...")
    clean_properties()
    print("Cleaner finished and saved to data/cleaned/cleaned_properties.csv")
