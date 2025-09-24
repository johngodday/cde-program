import extract
import transform
import load

def run_pipeline():
    df = extract.extract("data/sample_sales.csv")
    df = transform.transform(df)
    load.load(df)
    print("[ETL] Pipeline completed successfully ✅")

if __name__ == "__main__":
    run_pipeline()
