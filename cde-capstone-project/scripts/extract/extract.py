import pandas as pd
import time 
import json
import boto3
import requests
from dotenv import dotenv_values
import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy import create_engine
from pathlib import Path


env_path = os.path.join(os.path.dirname(__file__), '../../.env')
env_path = os.path.abspath(env_path)
#-----------------------------------------------------------------
secret = dotenv_values(env_path)
#=================================================================


class BaseExtractor:
    def __init__(self, config_file=".env"):

        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../")
        )

        env_path = os.path.join(project_root, config_file)
        print("Loading ENV from:", env_path)

        self.secret = dotenv_values(env_path)

        self.s3_client_input = boto3.client(
            "s3",
            aws_access_key_id=self.secret["access_key"],
            aws_secret_access_key=self.secret["secret_access_key"],
            region_name=self.secret["region_input"]
        )

        self.s3_client_output = boto3.client(
            "s3",
            aws_access_key_id=self.secret["access_key_output"],
            aws_secret_access_key=self.secret["secret_access_key_output"],
            region_name=self.secret["region_output"]
        )

    def upload_parquet(self, bucket, key, df):
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)

        self.s3_client_output.put_object(
            Bucket=bucket,
            Key=key,
            Body=buffer.getvalue()    
        )
        print(f"Uploaded: s3://{bucket}/{key}")



class CsvExtractor(BaseExtractor):
    def __init__(self, input_bucket, output_bucket):
        super().__init__()
        self.input_bucket = input_bucket
        self.output_bucket = output_bucket

    def extract_csv_files(self, prefix):
        response = self.s3_client_input.list_objects_v2(
            Bucket=self.input_bucket, Prefix=prefix
        )
        contents = response.get("Contents", [])
        csv_files = [obj["Key"] for obj in contents if obj["Key"].endswith(".csv")]

        for file in csv_files:
            print(f"Found CSV file: {file}")

            obj = self.s3_client_input.get_object(Bucket=self.input_bucket, Key=file)
            df = pd.read_csv(io.BytesIO(obj["Body"].read()))

            self.upload_parquet(
                bucket=self.output_bucket,
                key=file.replace(".csv", ".parquet"),
                df=df,
            )

class JSONExtractor(BaseExtractor):
    def __init__(self, input_bucket, output_bucket):
        super().__init__()
        self.input_bucket = input_bucket
        self.output_bucket = output_bucket

    def extract_json_files(self, prefix):
        response = self.s3_client_input.list_objects_v2(
            Bucket=self.input_bucket, Prefix=prefix
        )
        contents = response.get("Contents", [])
        json_files = [obj["Key"] for obj in contents if obj["Key"].endswith(".json")]

        for file in json_files:
            print(f"Processing JSON file: {file}")

            obj = self.s3_client_input.get_object(Bucket=self.input_bucket, Key=file)
            df = pd.read_json(io.BytesIO(obj["Body"].read()), lines=True)

            self.upload_parquet(
                bucket=self.output_bucket,
                key=file.replace(".json", ".parquet"),
                df=df,
            )

class GoogleSheetExtractor(BaseExtractor):
    def __init__(self, output_bucket, service_key="service_key.json"):
        super().__init__()
        self.output_bucket = output_bucket

      
        self.service_key = str(Path(service_key).resolve())
        print("Using service account file:", self.service_key)

        self.creds = service_account.Credentials.from_service_account_file(
            self.service_key,
            scopes=['https://www.googleapis.com/auth/spreadsheets'],
        )

    def extract_sheet(self, spreadsheet_id, sheet_range, output_folder, output_name):

        print(f"Reading Google Sheet: {spreadsheet_id} [{sheet_range}]")

        service = build("sheets", "v4", credentials=self.creds)
        sheet = service.spreadsheets()

        try:
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=sheet_range
            ).execute()

            values = result.get("values", [])

        except HttpError as e:
            print("Google Sheets Error:", e)
            return

        df = pd.DataFrame(values)

        key = f"{output_folder}/{output_name}.parquet"

        self.upload_parquet(
            bucket=self.output_bucket,
            key=key,
            df=df,
        )

        print("Google Sheet uploaded successfully ✓")

class DataBaseExtractor(BaseExtractor):
    def __init__(self, output_bucket, db_credentials):
        super().__init__()
        self.output_bucket = output_bucket

        self.database = db_credentials["dbname"]
        self.port = db_credentials["port"]
        self.user = db_credentials["username"]
        self.password = db_credentials["password"]
        self.host = db_credentials["host"]

        self.url = (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

        self.engine = create_engine(self.url)

    def extract_db_data(self, query, s3_path):
        df = pd.read_sql(query, self.engine)
        df.columns = [(col.lower()).replace(" ", "_") for col in df.columns]

        print(df.head(3))
        print(df.columns)
        print(f"Fetched {len(df)} rows.")

        # Force parquet extension
        if s3_path.endswith(".csv"):
            s3_path = s3_path.replace(".csv", ".parquet")

        self.upload_parquet(
            bucket=self.output_bucket,
            key=s3_path,
            df=df
        )
        

if __name__ == "__main__":

    # Load env the RIGHT way
    base = BaseExtractor()  
    secret = base.secret

    input_bucket = "core-telecoms-data-lake"
    output_bucket = "capstone-dumps"

    customer_prefix = 'customers/' 
    call_logs_prefix = 'call logs/' 
    media_prefix = 'social_medias/' 

    spread_sheet_id = "1Aj3nydhvpRKhfeG91T3j_KuIId-Z8Pu3HS-xiMBX7QE"
    spread_sheet_range = "Sheet1!A:D"
    sheet_name = "agents_details"
    folder = "agents_data"

    process_date = "2025-11-21"

    s3_path = f"customer_complaints/web_form_request_{process_date.replace('-', '_')}.parquet"

    query = f"""
        SELECT * FROM customer_complaints.web_form_request_{process_date.replace('-', '_')}
    """

    # DB credentials from SSM
    ssm_client = boto3.client(
        "ssm",
        aws_access_key_id=secret["access_key"],
        aws_secret_access_key=secret["secret_access_key"],
        region_name=secret["region_input"],
    )

    def get_parameter(name, decrypt=True):
        return ssm_client.get_parameter(Name=name, WithDecryption=decrypt)["Parameter"]["Value"]

    db_credentials = {
        "host": get_parameter("/coretelecomms/database/db_host"),
        "dbname": get_parameter("/coretelecomms/database/db_name"),
        "password": get_parameter("/coretelecomms/database/db_password"),
        "username": get_parameter("/coretelecomms/database/db_username"),
        "port": get_parameter("/coretelecomms/database/db_port"),
    }

    # RUN DB extraction
    db = DataBaseExtractor(output_bucket, db_credentials)
    db.extract_db_data(query, s3_path)
    print("Database extraction completed.")

    # CSV extractor
    csv_extractor = CsvExtractor(input_bucket, output_bucket)
    csv_extractor.extract_csv_files(prefix=customer_prefix)
    print("Customer extraction completed.")

    csv_extractor = CsvExtractor(input_bucket, output_bucket)
    csv_extractor.extract_csv_files(prefix=call_logs_prefix)
    print("Media extraction completed.")


    # JSON extractor
    json_extractor = JSONExtractor(input_bucket, output_bucket)
    json_extractor.extract_json_files(prefix=media_prefix)
    print("Call logs extraction completed.")

    # Google Sheet extractor
    gs_extractor = GoogleSheetExtractor(output_bucket,service_key = 'service_key.json')
    gs_extractor.extract_sheet(spread_sheet_id,spread_sheet_range,folder,sheet_name)
    print("Google Sheet extraction completed.")

