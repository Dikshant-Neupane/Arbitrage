from modules.scraper import scrape_properties
from modules.cleaner import clean_properties
from modules.database import insert_properties

def run_pipeline():
    print("....Starting Scraper.....")
    scrape_properties()
    
    print("....Starting Cleaner....")
    clean_properties()
    
    print("....Updating Database....")
    insert_properties()
    
    print("Pipeline completed sucessfully!")
    
if __name__=="__main__":
    run_pipeline()