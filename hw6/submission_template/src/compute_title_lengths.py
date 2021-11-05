import json
import os.path as osp
from pathlib import Path
import sys

# Get parent dir
parentdir = Path(__file__).parents[1]

# Get args
def parse_args():
    error = 'Wrong usage - python3 compute_title_lengths.py <input_file>'
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        raise Exception (error)
        
    return sys.argv[1]
    
def title_length(input_fname):
    num_posts = 0
    total_title_length = 0
    
    # Read JSON entries for each post from input file
    with open(input_fname, 'r') as f:
        for line in f:
            num_posts += 1
            title = json.loads(line)['data']['title']
            total_title_length += len(title) 

    return total_title_length/num_posts
    
def main():
    input_fname = parse_args()
    print(title_length(input_fname))

if __name__ == '__main__':
    main()
