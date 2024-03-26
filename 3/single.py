from google.oauth2 import service_account
from google.cloud import bigquery
from sqlalchemy import create_engine
import pandas as pd
import os
import pandas_gbq


project_id = os.getenv('PROJECT_ID')
# Bigquery configuration
credentials_dict = {
      "project_id": os.getenv('PROJECT_ID'),
      "private_key": os.getenv('BIGQUERY_DEV_KEY'),
      "client_email":  os.getenv('BIGQUERY_DEV_CLIENTEMAIL'),
      "token_uri":  os.getenv('BIGQUERY_DEV_TOKENURI')
    }
    
credentials = service_account.Credentials.from_service_account_info(credentials_dict)


# postgresql configuration
db_username = os.environ['db_username']
db_password = os.environ['db_password']
db_host = os.environ['db_host']
db_port = os.environ['db_port']
db_name = os.environ['db_name']
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

dataset= "testdataset"
table_name = os.environ['source_table_name']


# Write your SQL query
query = f"SELECT * FROM {table_name} limit 10;"

# Read data from PostgreSQL database into a pandas dataframe
df = pd.read_sql(query, engine)


# Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "scenic-sunspot-273512"

target_table = f"{dataset}.{table_name}_small"
# write the data to bigquery
pandas_gbq.to_gbq(df, target_table, project_id=project_id, if_exists='replace')
