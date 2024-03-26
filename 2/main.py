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

job_config = bigquery.QueryJobConfig(
    # Run at batch priority, which won't count toward concurrent rate limit.
    priority=bigquery.QueryPriority.BATCH
)

sql = """create or replace table testdataset.test2 as SELECT * from testdataset.people;"""

query_job = client.query(sql, job_config=job_config)  # Make an API request.


query_job = client.get_job(
    query_job.job_id, location=query_job.location
)  

print("Job {} is currently in state {}".format(query_job.job_id, query_job.state))

