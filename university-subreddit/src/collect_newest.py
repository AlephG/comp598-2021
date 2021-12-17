import requests
import json
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='<output_file>', required=True)
    parser.add_argument('-s', help='<subreddit>', required=True)
    args = parser.parse_args()

    return args.o, args.s

def verify_directory(out_fname):

    # Verify if save directory exists, make it if necessary
    save_dir = os.path.split(out_fname)[0]
    if save_dir != '':
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)


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

def collect(out_fname, subreddit, headers):
    # Send request for data
    base_url = f'https://oauth.reddit.com{subreddit}/new'
    request = requests.get(base_url, headers=headers, params={'limit':'100'})

    # Write json entries for each post in file
    with open(out_fname, 'a') as f:
        json_posts = request.json()
        for child in json_posts['data']['children']:
            f.write(json.dumps(child) + '\n')

def main():

    out_fname, subreddit = parse_args()
    
    verify_directory(out_fname)

    headers = authenticate()
    
    collect(out_fname, subreddit, headers)

if __name__ == '__main__':
    main()
