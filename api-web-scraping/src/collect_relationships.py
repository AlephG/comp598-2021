from bs4 import BeautifulSoup as bs
import json
import os, sys
import argparse
import requests
import hashlib
import re

def parse_args():
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Input config file', required=True)
    parser.add_argument('-o', help='Output file', required=True)
    args = parser.parse_args()
    
    return args.c, args.o


def get_config(config_fname):
    
    # Load JSON config file
    json_config = json.loads(open(config_fname).read())
    
    return json_config['cache_dir'], json_config['target_people']
 
def get_html_files(target_people, cache_dir):
    
    # Initialize file array
    files = []
    # Simulate browser user-agent
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'}
    
    # Get file for each target person
    for target in target_people:
        # Useful info
        base_url = f'https://www.whosdatedwho.com/dating/{target}'
        fname_hash = hashlib.sha1(base_url.encode()).hexdigest()
        file_path = os.path.join(cache_dir, fname_hash)
        
        # Make cache directory if does not exist
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        
        # If file downloaded, load from cache, else download
        if os.path.exists(file_path):
            # Add filename to list
            files.append(file_path)
        
        else:   
            # Request html content from base_url
            response = requests.get(base_url, headers=headers)
            
            # Verify request raised no error
            if response.raise_for_status() is None:
                # Get html content as text
                html_content = response.text
                # Save html to file and add to list
                with open(file_path, 'w') as f:
                    f.write(html_content)
                files.append(file_path)
            
            else:
                # Append none to list if request error
                files.append(None)
    
    return files

def get_relationships(files, target_people):
    
    # Initialize relationships dictionary
    relationships = {}
    
    # Parse html files to get relationships
    for i, f in enumerate(files):
        # Initialize relationship list for current file
        target_relationships = []
        target = target_people[i]
        
        # If no file, add empty list and continue
        if f is None:
            relationships[target] = target_relationships
            continue

        # Create our soup!
        soup = bs(open(f, 'r'), 'html.parser')
        
        # Look for dating history to figure out relationship count
        rel_hist = soup.find('a', href='#ff-dating-history')
        if rel_hist is None:
            count = 0
        else:
            count = int(rel_hist.find(class_='fact').string)

        # Find first person in relationships
        dated = soup.find('a', href=re.compile('^/dating/'))
        
        # Continue looking for relationships until exceed count or no more left to parse
        while dated is not None and count != 0:
            # Parse dated person
            person = dated['href'].split('/')[2]

            # Verify that person parsed is not our current target
            # and add them to list, update count
            if person != target:
                target_relationships.append(person)
                count -= 1
            # Find the next dated person
            dated = dated.find_next('a', href=re.compile('^/dating/'))
        
        # Add target relationships to dictionary
        relationships[target] = target_relationships
        
    return relationships

def save_to_json(relationships, output_fname):
    
    # Open file to write
    with open(output_fname, 'w') as f:
        # Dump relationship dictionary as json string and write to file
        json_data = json.dumps(relationships)
        f.write(json_data)

def main():

    config_fname, output_fname = parse_args()
    
    cache_dir, target_people  = get_config(config_fname) 
    
    files = get_html_files(target_people, cache_dir)
    
    relationships = get_relationships(files, target_people)
    
    save_to_json(relationships, output_fname)

if __name__ == '__main__':
    main()
