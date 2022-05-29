import os
import psycopg2
import requests
#from elasticsearch import Elasticsearch #trying just the restpi

'''es = Elasticsearch(
    cloud_id=os.environ['ES_CID'],
    basic_auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']),
)

resp = es.info()
print(resp)'''

resp = requests.get(os.environ['ES_ENDPOINT'], auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']))
print(resp.json())

conn = psycopg2.connect(
    host=os.environ['PG_HOST'],
    database=os.environ['PG_NAME'],
    user=os.environ['PG_USERNAME'],
    password=os.environ['PG_PASSWORD'],
)

print('connected to pg')
