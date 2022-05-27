import os
import psycopg2
from elasticsearch import Elasticsearch

es = Elasticsearch(
    cloud_id=os.environ['ES_CID'],
    basic_auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']),
)

resp = es.info()
print(resp)

conn = psycopg2.connect(
    host=os.environ['PG_HOST'],
    database=os.environ['PG_NAME'],
    user=os.environ['PG_USERNAME'],
    password=os.environ['PG_PASSWORD'],
)

print('connected to pg')
