import os
import requests
from pprint import pprint

def get_users(crime_poster):
    headers = {}
    json_data = {
        'query': {
            'term': {
                'data.subreddit': 'nyc',
            },
        },
    }

    while True:
        try:
            resp = requests.get(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_search?pretty&size=10000",
                auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout=5, headers=headers, json=json_data)
            if resp.status_code == 404:
                continue
        except requests.exceptions.ConnectionError as e:
            continue
        break

    hits = resp.json()['hits']['hits']

    for h in hits:
        author = h['_source']['data']['subreddit']
        if h['_source']['about_crime'] == True:
            if author in crime_poster:
                crime_poster[author] += 1
            else:
                crime_poster[author] = 1
    pprint(crime_poster)

def main():
    crime_poster = {}

    get_users(crime_poster)

main()
