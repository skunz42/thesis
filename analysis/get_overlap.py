import os
import requests
import csv

def get_users(crime_poster, non_crime_poster):
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
        author = h['_source']['data']['author']
        if h['_source']['about_crime'] == True:
            if author in non_crime_poster:
                non_crime_poster.remove(author)
            crime_poster.add(author)
        else:
            if author not in crime_poster:
                non_crime_poster.add(author)

    print(len(non_crime_poster))
    print(len(crime_poster))

def get_comments(poster_set):
    subreddit_map = {}

    url = "https://oauth.reddit.com/user"
    sub_url = "https://oauth.reddit.com/r"
    auth = requests.auth.HTTPBasicAuth(os.environ['REDDIT_CLIENT_ID'], os.environ['REDDIT_CLIENT_SECRET'])

    data = {
        'grant_type': 'password',
        'username': os.environ['REDDIT_USER_NAME'],
        'password': os.environ['REDDIT_PASSWORD'],
    }

    headers = {
        'User-Agent': os.environ['REDDIT_USER_AGENT'],
    }

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']

    headers['Authorization'] = f"bearer {TOKEN}"

    while len(poster_set) > 0:
        author = poster_set.pop()
        print(f'Author: {author}')

        res = requests.get(f'{url}/{author}/comments', headers=headers, params={'limit':50})
        if res.status_code == 404 or res.status_code == 403:
            continue

        children = res.json()['data']['children']

        #num_crime_posts += len(children)

        for c in children:
            subreddit = c['data']['subreddit']
            karma = c['data']['score']
            if subreddit not in subreddit_map:
                subreddit_map[subreddit] = [1, karma, 0]
                sub_res = requests.get(f'{sub_url}/{subreddit}/about', headers=headers)
                subscribers = sub_res.json()['data']['subscribers']
                subreddit_map[subreddit][2] = subscribers
            else:
                subreddit_map[subreddit][0] += 1
                subreddit_map[subreddit][1] += karma

    with open(f'noncrimeposters.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(["SUB", "HITS", "KARMA", "SUBSCRIBERS"])

        for k in subreddit_map:
            csv_writer.writerow([k, subreddit_map[k][0], subreddit_map[k][1], subreddit_map[k][2]])

def main():
    crime_poster = set()
    non_crime_poster = set()

    get_users(crime_poster, non_crime_poster)
    #get_comments(crime_poster)
    get_comments(non_crime_poster)

main()
