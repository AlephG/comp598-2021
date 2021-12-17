import json
import argparse
import random
import os

def parse_args():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='<output_file>  <json_file> <num_posts_to_output>', nargs=3, required=True)
    args = parser.parse_args()

    return args.o[0], args.o[1], int(args.o[2])

def verify_directory(out_fname):
    
    # Verify if save directory exists, make it if necessary
    save_dir = os.path.split(out_fname)[0]
    if save_dir != '':
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

def extract(out_fname, in_json_fname, num_posts):
    
    # Randomly select post lines to extract
    posts_to_extract = [line for line in range(100)]
    if num_posts < 100:
        posts_to_extract = random.sample(posts_to_extract, k=num_posts)
    posts_to_extract.sort()

    # Initialize empty array for json objects
    reddit_posts = []

    # Load file lines
    with open(in_json_fname, 'r') as f:
        next_post = posts_to_extract.pop(0)
        for l, line in enumerate(f):
            # Load current line as JSON if matches sample
            if l == next_post:
                reddit_posts.append(json.loads(line))
                if len(posts_to_extract) != 0:
                    next_post = posts_to_extract.pop(0)
                else:
                    break
     
    # Extract name and title, write to file
    with open(out_fname, 'w') as f:
        f.write('Name\ttitle\tcoding\n')
        for post in reddit_posts:
            name = post['data']['name']
            title = post['data']['title']
            f.write(f'{name}\t{title}\t\n')


def main():
    
    out_fname, in_json_fname, num_posts = parse_args()
    
    verify_directory(out_fname)

    extract(out_fname, in_json_fname, num_posts)
    
if __name__ == '__main__':
    main()
