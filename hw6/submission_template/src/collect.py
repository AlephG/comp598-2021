import json
import requests
import os.path as osp
import argparse
from pathlib import Path

# Get parent dir
parentdir = Path(__file__).parents[1]

# Authentication files
reddit_auth_fname = '/Users/solimlegris/Projects/api_keys/comp598/reddit-login.json'
api_keys_fname = '/Users/solimlegris/Projects/api_keys/comp598/reddit-api-auth.json'

def authenticate():
    # Get reddit api credentials
    with open(api_keys_fname, 'r') as f:
        api_login = json.loads(f.readline())
    
    # Get Reddit login credentials
    with open(reddit_auth_fname, 'r') as f:
        reddit_login = json.loads(f.readline())

    # Create authetication token
    auth = requests.auth.HTTPBasicAuth(api_login['client_id'], api_login['secret_key'])

    # Create login type dictionary
    data = {
        'grant_type': 'password',
        'username': reddit_login['username'],
        'password': reddit_login['password']
    }
    
    # Create user-agent in headers
    headers = {'User-Agent':'data-science/0.0.1'}
    
    # Request access token from reddit api
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth,
                        data=data, headers=headers)

    # Get the token
    TOKEN = res.json()['access_token']
    
    # Add authorization to headers
    headers['Authorization'] = f'bearer {TOKEN}'

    return headers

def sample(headers, by_subscriber=True):
    
    # Determine which subreddits to scrape and save file
    if by_subscriber:
        subreddits = ['funny','AskReddit','gaming', 'aww', 'pics', 'Music', 'science',
                      'worldnews', 'videos', 'todayilearned']
        savefile = osp.join(parentdir, 'data', 'sample1.json')
    else:
        subreddits = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets',
                      'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']
        savefile = osp.join(parentdir, 'data', 'sample2.json') 
     
    for sub in subreddits:
        # Send request
        base_url = f'https://oauth.reddit.com/r/{sub}/new'
        request = requests.get(base_url, headers=headers, params={'limit':'100'})
        
        # Write json entries for each post in file
        with open(savefile, 'a') as f:
            json_posts = request.json()
            for child in json_posts['data']['children']:
                f.write(json.dumps(child) + '\n') 

def main():
    headers = authenticate()

    # Sample from most popular subreddits by # of subscribers
    sample(headers)

    # Sample from most popular subreddits by # of posts by day
    sample(headers, by_subscriber=False)

if __name__ == '__main__':
    main()

