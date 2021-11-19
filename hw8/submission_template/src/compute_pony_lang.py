import json
import os
import argparse
import math
from copy import deepcopy

def parse_args():

    parser = argparse.ArgumentParser(description='Analyze My Little Pony dialog stats')
    parser.add_argument('-c', help='<pony_counts.json>', required=True)
    parser.add_argument('-n', help='<num_words>', required=True)
    args = parser.parse_args()

    return args.c, int(args.n)

def compute_score(pony_counts_fname, num_words):
    
    # Load pony counts json
    pony_counts = None
    with open(pony_counts_fname, 'r') as f:
        pony_counts = json.loads(f.read())
    
    # Initialize new dictionary for tf-idf
    pony_tf_idf = deepcopy(pony_counts)

    # Compute tf-idf for each word
    num_ponies = len(pony_counts)
    words = pony_counts[list(pony_counts.keys())[0]]
    for w in words:
        num_ponies_using = 0
        # Get the usage for the word across ponies
        for pony in pony_counts:
            if pony_counts[pony][w] > 0:
                num_ponies_using += 1
        # Compute tf-idf score for the word for each pony
        for pony in pony_counts:
            idf = math.log10(num_ponies/num_ponies_using)
            tf = pony_counts[pony][w]
            pony_tf_idf[pony][w] = tf*idf 

    # Sort by tf_idf in descending order
    for pony in pony_tf_idf:
        pony_tf_idf[pony] = {key:value for key, value in sorted(
            pony_tf_idf[pony].items(), key=lambda item: item[1], reverse=True)}
    
    # Write output to std_out
    outputs = {pony: 
               list(pony_tf_idf[pony].keys())[0:num_words] for pony in pony_tf_idf}
    
    return outputs

def main():
    
    pony_counts_fname, num_words = parse_args()
    
    outputs = compute_score(pony_counts_fname, num_words)
    
    print(json.dumps(outputs, indent=1))

if __name__=='__main__':
    main()
