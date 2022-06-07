import os
import requests
import csv
import json
import sys

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

def write_csv(cities, output_file_name):
    with open(f'../data/{output_file_name}.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(["NAME", "SUBREDDIT", "ID", "POP", "DEM", "REP", "CRIME_RATE", "P_CRIME_RATE",
            "P_CRIME_HITS", "TOTAL_HITS", "POP_CLASS", "POL_CLASS"])

        for c in cities:
            csv_writer.writerow([c['name'], c['subreddit'], c['id'], c['population'], c['dem'],
                c['rep'], c['crime_rate'], c['pcrime_rate'], c['pcrime_hits'], c['total_hits'],
                c['pop_class'], c['pol_class']])


def read_keywords(keywords):
    with open('../data/keywords.txt') as keys_file:
        for row in keys_file:
            keywords.append(row.rstrip())

def populate_city_data(cities, keywords):
    for c in cities:
        #if c["subreddit"] != "seattlewa":
            #continue

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
                "query_string": {
                    "query": f"(data.subreddit: {c['subreddit']}) AND (data.title: shooting* OR data.url: shooting*)"
                }
            },
            'size': 1000,
            'sort': {
                "@timestamp": {
                    "order": "desc"
                }
            },
        }

        header = {}
        headers = {'Content-Type': 'application/x-ndjson'}
        m_search_string = ""

        for k in keywords:
            m_search_string += json.dumps(header) + '\n'
            json_data['query']['query_string']['query'] = f"(data.subreddit: {c['subreddit']}) AND (data.title: {k} OR data.url: {k})"
            m_search_string += json.dumps(json_data) + '\n'
        
        while True:
            try:
                resp = requests.get(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_msearch?pretty",
                    auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout=5, headers=headers, data=m_search_string)
                if resp.status_code == 404:
                    continue
            except requests.exceptions.ConnectionError as e:
                continue

            #print(f"{k}: {resp.json()['hits']['total']['value']}")
            id_set = set()
            for r in resp.json()['responses']:
                #print(r['hits']['total']['value'])
                for h in r['hits']['hits']:
                    id_set.add(h['_id'])
            
            c['pcrime_hits'] = len(id_set)
            c['pcrime_rate'] = 100.0*c['pcrime_hits'] / c['total_hits']
            print(f"{c['subreddit']}: {c['pcrime_hits']}, {c['pcrime_rate']}")

            bulk_update_string = ""

            while len(id_set) != 0:
                curr_id = id_set.pop()
                updates = {'update': {"_id": curr_id, "_index": "reddit-posts"}}
                docs = {"doc": {"about_crime": True}}
                bulk_update_string += json.dumps(updates) + '\n'
                bulk_update_string += json.dumps(docs) + '\n'

            while True:
                try:
                    resp = requests.post(f"{os.environ['ES_ENDPOINT']}/reddit-posts/_bulk",
                        auth=(os.environ['ES_USERNAME'], os.environ['ES_PASSWORD']), timeout=5, headers=headers, data=bulk_update_string)
                    if resp.status_code == 404:
                        continue
                except requests.exceptions.ConnectionError as e:
                    continue
                break

            break

def main():
    if len(sys.argv) != 2:
        print("Input a filename for output CSV")
        return

    cities = []
    keywords = []
    read_csv(cities)
    read_keywords(keywords)
    populate_city_data(cities, keywords)
    write_csv(cities, sys.argv[1])

main()
