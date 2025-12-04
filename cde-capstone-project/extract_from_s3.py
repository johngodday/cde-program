import boto3
import pandas as pd
import json
import requests
from dotenv import dotenv_values
from datetime import datetime
from sqlalchemy import create_engine



secret = dotenv_values('.env')

#=========================================================
#=========================================================
#  Credenntials
#=========================================================
#=========================================================
s3_resource = boto3.resource(
    's3',
    aws_access_key_id = secret['access_key'],
    aws_secret_access_key = secret['secret_access_key']
)

s3_client = boto3.client(
      's3',
    aws_access_key_id = secret['access_key'],
    aws_secret_access_key = secret['secret_access_key']
)

ssm_client = boto3.client(
    'ssm',
    aws_access_key_id = secret['access_key'],
    aws_secret_access_key = secret['secret_access_key'],
    region_name = 'eu-north-1'
)

#========================================================
input_bucket = 'core-telecoms-data-lake'
prefix = 'call logs'
file_tag = str(datetime.today().date())
#========================================================


def get_s3_files(*args):

    response = s3_client.list_objects_v2(Bucket = input_bucket, Prefix = prefix)
    contents = response.get("Contents", [])

    objects = [obj['Key'] for obj in contents if obj['Key'].endswith(f".csv")]

    for files in objects:
        print(files)

def get_parameter(name, decrypt=True):
    response = ssm_client.get_parameter(
        Name=name,
        WithDecryption=decrypt
    )
    return response['Parameter']['Value']


db_credentials = {
    "host": get_parameter("/coretelecomms/database/db_host"),
    "dbname": get_parameter("/coretelecomms/database/db_name"),
    "password": get_parameter("/coretelecomms/database/db_password"),
    "username": get_parameter("/coretelecomms/database/db_username"),
    "port": get_parameter("/coretelecomms/database/db_port"),
    "schema_name": get_parameter("/coretelecomms/database/table_schema_name")
}

# print(db_credentials)
#=========================================================

# get_s3_files()


def db_connect(db_credentials):
    user = db_credentials['username']
    password = db_credentials['password']
    host = db_credentials['host']
    port = db_credentials['port']
    dbname = db_credentials['dbname']


    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    return create_engine(url)

# with db_connect(db_credentials) as conn:
#     result = conn.execute("""
#         SELECT table_schema, table_name
#         FROM information_schema.tables
#         WHERE table_type = 'BASE TABLE'
#         ORDER BY table_schema, table_name;
#     """)
    
#     for row in result:
#         print(row)

query = '''
        select * from customer_complaints.web_form_request_2025_11_20
        '''
engine = db_connect(db_credentials)
df = pd.read_sql(query, engine)
print(df.head())
print(df.columns)
