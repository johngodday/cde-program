import pandas as pd

def extract(csv_path="data/sample_sales.csv"):
    print("[ETL] Extracting data from CSV...")
    return pd.read_csv(csv_path)
