from google.oauth2 import service_account
from google.cloud import bigquery
from sqlalchemy import create_engine
import pandas as pd
import os
import pandas_gbq

# Bigquery configuration
credentials_dict = {
      "project_id": os.getenv('PROJECT_ID'),
      "private_key": os.getenv('BIGQUERY_DEV_KEY'),
      "client_email":  os.getenv('BIGQUERY_DEV_CLIENTEMAIL'),
      "token_uri":  os.getenv('BIGQUERY_DEV_TOKENURI')
    }
    
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
client = bigquery.Client(credentials=credentials)


# postgresql configuration
db_username = os.environ['db_username']
db_password = os.environ['db_password']
db_host = os.environ['db_host']
db_port = os.environ['db_port']
db_name = os.environ['db_name']
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

project = os.environ['bq_project_source']
dataset = os.environ['bq_dataset_source']
table_name = os.environ['bq_table_source']

# Perform a query.
#QUERY = (f'SELECT * FROM `{project}`.`{dataset}`.`{table_name}`')
#df = client.query(QUERY).to_dataframe()


# Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "scenic-sunspot-273512"


# The credentials and project_id arguments can be omitted.
df = pandas_gbq.read_gbq(f"SELECT * FROM `{project}`.`{dataset}`.`{table_name}` limit 1000")

# write data to postgresql
df.to_sql(table_name+"_copy", engine, if_exists='replace', index=False)
