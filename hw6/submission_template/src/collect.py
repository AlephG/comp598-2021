import json
import requests
import os
import os.path as osp
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Get parent dir
parentdir = Path(__file__).parents[1]

# Authentication keys
# Need to have .env file with authetication in root directory of script
load_dotenv()


def authenticate():
    # Create authentication token
    auth = requests.auth.HTTPBasicAuth(os.getenv('CLIENT_ID'), os.getenv('SECRET_KEY'))

    # Create login type dictionary with login credentials
    data = {
        'grant_type': 'password',
        'username': os.getenv('REDDIT_USER'),
        'password': os.getenv('REDDIT_PWD')
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
    
    # Determine which subreddits to scrape and which output file to use
    if by_subscriber:
        subreddits = ['funny','AskReddit','gaming', 'aww', 'pics', 'Music', 'science',
                      'worldnews', 'videos', 'todayilearned']
        savefile = osp.join(parentdir, 'sample1.json')
    else:
        subreddits = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets',
                      'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']
        savefile = osp.join(parentdir, 'sample2.json') 
     
    for sub in subreddits:
        # Send request for data
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

