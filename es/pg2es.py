import os
from elasticsearch import Elasticsearch

es = Elasticsearch(
        os.environ['ES_HOST'],
        ca_certs=os.environ['ES_CERTS'],
        basic_auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD'])
    )

resp = es.info()
print(resp)
