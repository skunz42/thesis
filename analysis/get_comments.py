import os
import requests

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

def get_comments(crime_poster, non_crime_poster):
    url = "https://oauth.reddit.com/user/"

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
    res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    print(res.json())


def main():
    crime_poster = set()
    non_crime_poster = set()

    get_users(crime_poster, non_crime_poster)
    get_comments(crime_poster, non_crime_poster)

main()
