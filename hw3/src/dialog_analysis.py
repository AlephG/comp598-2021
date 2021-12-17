# This file will contain functions to analyze dialog data!

# Imports
import pandas as pd
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze My Little Pony dialog stats')
    parser.add_argument('-o', type=str, help='Path of output file')
    parser.add_argument('fname', help='Path of input file')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Names of the ponies
    pony = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    
    # Read file and extract stats 
    df = pd.read_csv(args.fname)
    count = {}
    verbosity = {}
    num_spacts = df['pony'].count()
    
    for p in pony:
        count[p] = int(df['pony'].str.fullmatch(p, case=False).sum())
        verbosity[p] = round(count[p]/num_spacts, 2)
    
    # Write stats to JSON
    stats = {'count':count, 'verbosity':verbosity}

    # Save JSON file
    with open(args.o, 'w') as f:
        json.dump(stats, f, indent=1)

if __name__ == "__main__":
    main()
