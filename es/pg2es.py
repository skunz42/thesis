import os
import psycopg2
import requests

resp = requests.get(os.environ['ES_ENDPOINT'], auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']))
print("connected to es")

conn = psycopg2.connect(
    host=os.environ['PG_HOST'],
    database=os.environ['PG_NAME'],
    user=os.environ['PG_USERNAME'],
    password=os.environ['PG_PASSWORD'],
)

print('connected to pg')

cur = conn.cursor()

cur.execute("select * from posts limit 1")

rows = cur.fetchall()

for row in rows:
    timestamp = row[1]
    pid = row[0]
    about_crime = row[3]
    data = row[2]
    print(data["title"])
    json_data = {
        '@timestamp': timestamp.isoformat(),
        'post_id': pid,
        'data': data,
        'about_crime': about_crime,
    }

cur.close()

'''resp = requests.post(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_doc?pretty", auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), json=json_data)
print(resp.json())'''
