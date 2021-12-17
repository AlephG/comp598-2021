import pandas as pd
import argparse
import json
import os

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<coded_file.tsv>', required=True)
    parser.add_argument('-o', help='<output_file>', required=False)
    args = parser.parse_args()

    return args.i, args.o

def verify_directory(out_fname):

    # Verify if save directory exists, make it if necessary
    save_dir = os.path.split(out_fname)[0]
    if save_dir != '':
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

def analyze(data, out):
    
    # Get count for each coding
    count = data['coding'].value_counts()
    
    # Save data in dictionary
    keys = {'course-related':'c', 'food-related':'f', 'other':'o', 'residence-related':'r'}
    data_dict = {}

    for k in keys:
        if keys[k] in count.keys():
            data_dict[k] = int(count[keys[k]])
        else:
            data_dict[k] = 0
    
    pretty_json = json.dumps(data_dict, sort_keys=True, indent=1)

    if out is None:
        print(pretty_json)
    else:
        with open(out, 'w') as f:
            f.write(pretty_json)

def main():
    
    coded_fname, out = parse_args()
    
    data = pd.read_csv(coded_fname, delimiter='\t')
    
    if out is not None:
        verify_directory(out)

    analyze(data, out)

if __name__=='__main__':
    main()
