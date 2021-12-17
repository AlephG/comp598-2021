import pandas as pd
import argparse
import json
import networkx as nx
import os
from pathlib import Path


def verify_directory(path):

    # Verify if save directory exists, make it if necessary
    save_dir = os.path.split(path)[0]
    if save_dir != '':
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)


def parse_args():

    parser = argparse.ArgumentParser(description='build interaction network')
    parser.add_argument('-i', help='<script_input.csv>', required=True)
    parser.add_argument('-o', help='<interaction_network.json>', required=True)
    args = parser.parse_args()

    return args.i, args.o


def format_data(data):
    data['pony'] = data.pony.str.lower()
    data['title'] = data.title.str.lower()
    data = data[['title', 'pony']]
    
    return data


def get_ponies_list(data, exceptions):

    # Find 101 most popular ponies 
    data_no_exceptions = data[~data['pony'].str.contains('|'.join(exceptions), case=False, regex=True)]
    most_popular = data_no_exceptions['pony'].value_counts()
    most_popular = most_popular[:101].index.to_list()
    
    return most_popular


def get_interactions(data):
    
    exceptions = ['others', 'and', 'ponies', 'all'] 
    most_popular = get_ponies_list(data, exceptions)
    
    # Intialize interactions dictionary
    interactions = {}
    
    # Get interactions
    for idx, speech_act in data.iterrows():
        
        # If last speech, we are done
        if idx == len(data)-1:
            continue
        
        # Get cur_pony data
        cur_tile = speech_act.title
        next_title = data.title[idx+1]
        
        # Get next pony data
        cur_pony = speech_act.pony
        next_pony = data.pony[idx+1]

        # If next title is different, skip
        if cur_tile != next_title:
            continue
        
        # If this pony or next is not popular, skip
        if cur_pony not in most_popular or next_pony not in most_popular:
            continue

        # If next pony is self, skip
        if cur_pony == next_pony:
            continue
        
        # Add interaction between ponies, for both ponies
        if cur_pony in interactions:
            if next_pony in interactions[cur_pony]:
                interactions[cur_pony][next_pony] += 1
            else:
                interactions[cur_pony][next_pony] = 1 
        else:
            interactions[cur_pony] = {}
            interactions[cur_pony][next_pony] = 1
        
        if next_pony in interactions:
            if cur_pony in interactions[next_pony]:
                interactions[next_pony][cur_pony] += 1
            else: 
                interactions[next_pony][cur_pony] = 1
        else:
            interactions[next_pony] = {}
            interactions[next_pony][cur_pony] = 1

    
    return interactions


def main():
    
    input_fname, output_fname = parse_args()
    
    data = pd.read_csv(input_fname)
    
    data = format_data(data)

    interactions = get_interactions(data)
    
    verify_directory(output_fname)
    
    with open(output_fname, 'w') as f:
        json.dump(interactions, f, indent=2)
        #f.write(json.dumps(interactions, indent=2))


if __name__=='__main__':
    main()
