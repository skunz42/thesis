import os
import requests
import csv

VERY_SMALL = 0
SMALL = 1
MEDIUM = 2
LARGE = 3

VERY_CONSERVATIVE = 0
CONSERVATIVE = 1
MODERATE = 2
LIBERAL = 3
VERY_LIBERAL = 4

def city_factory(row):
    return {'name': row[0], 'subreddit': row[1], 'id': row[2], 'population': int(row[3]), 
            'dem': int(row[4]), 'rep': int(row[5]), 'crime_rate': float(row[8]), 'pcrime_rate': 0,
            'pcrime_hits': 0, 'total_hits': 0, 'pop_class': VERY_SMALL, 'pol_class': VERY_CONSERVATIVE}

def read_csv(cities):
    with open('../data/urbanareas.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)

        for row in csv_reader:
            cities.append(city_factory(row))

def populate_city_data(cities):
    for c in cities:

        if c["subreddit"] != "nyc":
            continue

        # set political class
        per_dem = 100.0 * (c["dem"]) / (c["dem"]+c["rep"])
        if per_dem >= 62.5:
            c['pol_class'] = VERY_LIBERAL
        elif per_dem >= 52.5:
            c['pol_class'] = LIBERAL
        elif per_dem >= 47.5:
            c['pol_class'] = MODERATE
        elif per_dem >= 37.5:
            c['pol_class'] = CONSERVATIVE
        else:
            c['pol_class'] = VERY_CONSERVATIVE

        # set population class
        if c['population'] >= 1000000:
            c['pop_class'] = LARGE
        elif c['population'] >= 500000:
            c['pop_class'] = MEDIUM
        elif c['population'] >= 200000:
            c['pop_class'] = SMALL
        elif c['population'] >= 50000:
            c['pop_class'] = VERY_SMALL

        # get number of subreddit posts
        json_data = {
            'query': {
                'term': {
                    'data.subreddit': c['subreddit'],
                },
            },
        }

        while True:
            try:
                resp = requests.get(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_count?pretty", 
                    auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout=5, json=json_data)
                if resp.status_code == 404:
#                    print(f"404 error on {subreddit}")
                    continue
            except requests.exceptions.ConnectionError as e:
#                print(f"connection timed out on {subreddit}")
                continue

            #print(resp.json())
            c["total_hits"] = resp.json()['count']
            break

        # get crime post hits
        json_data = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'term': {
                                'data.subreddit': c["subreddit"]
                            }
                        },
                        {
                                        'regexp': {
                                            'data.title': {
                                                'value': 'shooting.*',
                                                'flags': 'ALL',
                                                'case_insensitive': True
                                            },
                                        },
                        }
                    ],
                },
            },
            'size': 1000,
            'sort': {
                "@timestamp": {
                    "order": "desc"
                }
            }
        }

        while True:
            try:
                resp = requests.get(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_search?pretty",
                    auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout=5, json=json_data)
                if resp.status_code == 404:
                    continue
            except requests.exceptions.ConnectionError as e:
                continue

            for i in resp.json()['hits']['hits']:
                print(i["_source"]["data"]["title"])

            print(f"{c['name']}: {resp.json()['hits']['total']['value']}")
            break


def main():
    cities = []
    read_csv(cities)
    populate_city_data(cities)

main()
