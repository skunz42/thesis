import os
import requests
import csv

with open('../data/urbanareas.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)

    for row in csv_reader:
        subreddit = row[1]

        json_data = {
            'query': {
                'term': {
                    'data.subreddit' : subreddit,
                },
            },
        }

        while True:
            try:
                resp = requests.get(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_count?pretty", auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout=5, json=json_data)
                if resp.status_code == 404:
#                    print(f"404 error on {subreddit}")
                    continue
            except requests.exceptions.ConnectionError as e:
#                print(f"connection timed out on {subreddit}")
                continue

            print(f"{resp.json()['count']}")
            break
