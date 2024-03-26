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
client = bigquery.Client(credentials=credentials)

sql = """create or replace table testdataset.test1 as SELECT * from testdataset.people;"""

client.query(sql)