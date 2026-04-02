import schedule
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load, create_table

def run_pipeline():
    print("Pipeline starting...")
    create_table()
    df_raw = extract()
    df_transformed = transform(df_raw)
    load(df_transformed)
    print("Pipeline complete!")

# Lance le pipeline tous les jours à 9h00
schedule.every().day.at("09:00").do(run_pipeline)

if __name__ == "__main__":
    run_pipeline()  
    while True:
        schedule.run_pending()
        time.sleep(60)