import pandas as pd


def transform(df):
    print("[ETL] Transforming data...")
    df["total_value"] = df["amount"] * 2
    return df
