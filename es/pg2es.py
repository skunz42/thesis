import os
import psycopg2
import requests

#resp = requests.get(os.environ['ES_ENDPOINT'], auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout = 5)
#print("connected to es")

conn = psycopg2.connect(
    host=os.environ['PG_HOST'],
    database=os.environ['PG_NAME'],
    user=os.environ['PG_USERNAME'],
    password=os.environ['PG_PASSWORD'],
)

print('connected to pg')

cur = conn.cursor()

cur.execute("select * from posts")

rows = cur.fetchall()

for row in rows:
    timestamp = row[1]
    pid = row[0]
    about_crime = row[3]
    data = row[2]
    final_data = {
        'id': data['id'],
        'score': data['score'],
        'url': data['url'],
        'name': data['name'],
        'title': data['title'],
        'author': data['author'],
        'created': data['created'],
        'permalink': data['permalink'],
        'subreddit': data['subreddit'],
        'created_utc': data['created_utc'],
        'author_fullname': data['author_fullname'],
        'subreddit_name_prefixed': data['subreddit_name_prefixed'],
    }
    json_data = {
        '@timestamp': timestamp.isoformat(),
        'post_id': pid,
        'data': final_data,
        'about_crime': about_crime,
    }
    try:
        resp = requests.post(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_create/{pid}", auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), json=json_data, timeout=5)
    except requests.exceptions.ConnectionError as e:
        print(f"connection timed out on {pid}")
        continue

    resp_j = resp.json()
    try:
        print(resp_j['error']['reason'])
    except:
        print(f"inserting {pid}")
        continue



cur.close()


'''json_data = {
    "query": {
        "match": {
            "about_crime": False
            }
        }
    }
resp = requests.post(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_delete_by_query", auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), json=json_data)'''
