import argparse
import json
import os
from pathlib import Path
import pandas as pd
from copy import deepcopy


def parse_args():
    
    parser = argparse.ArgumentParser(description='Analyze My Little Pony dialog stats')
    parser.add_argument('-o', help='<word_counts_json>', required=True)
    parser.add_argument('-d', help='<clean_dialog.csv file>', required=True)
    args = parser.parse_args()
    
    return args.o, args.d


def verify_directory(path):
    
    # Verify if save directory exists, make it if necessary
    save_dir = os.path.split(path)[0]
    if save_dir != '':
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)


def clean(dialog_fname):
    
    pony = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    data = pd.read_csv(dialog_fname)
    
    # Make all pony names  lowercase
    data['pony'] = data['pony'].str.lower()
    
    # Strip trailing and leading whitespace
    data['pony'] = data['pony'].str.strip()
    
    # Keep rows where pony is in valid pony list
    data = data[data['pony'].isin(pony)]
    
    # Make everything in dialog lowercase to facilitate analysis
    data['dialog'] = data['dialog'].str.lower()
    
    # Drop title and writer
    data = data.drop(['title', 'writer'], axis=1)
    
    # Replace punctuation characters with space
    pat = '[()[\],[()[\],\-.?!:;#&]'
    data['dialog'] = data['dialog'].str.replace(pat, ' ', regex=True)
    
    # Remove non alphabetic words
    data['dialog'] = data['dialog'].apply(lambda x: ' '.join(
        [word for word in x.split() if word.isalpha()]))

    # Remove stop words
    stop = load_stop_words()
    data['dialog'] = data['dialog'].apply(
        lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    # Remove words that appear less than 5 times across all speech acts
    word_count_all = data['dialog'].str.split(expand=True).stack().value_counts()
    word_count_all = word_count_all[word_count_all >= 5]
    words = word_count_all.index.tolist()
    data['dialog'] = data['dialog'].apply(
        lambda x: ' '.join([word for word in x.split() if word in (words)]))

    return data, words
    
def load_stop_words():
    
    parent_dir = Path(__file__).parents[1]
    stopword_fname = os.path.join(parent_dir, 'data', 'stopwords.txt')
    stopwords = []
    with open(stopword_fname, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                stopwords.append(line.rstrip('\n'))
    return stopwords

def word_count(data,words):
    
    # Initialize pony word count dictionary
    pony_word_count = {'twilight sparkle':{}, 'applejack':{}, 'rarity':{}, 'pinkie pie':{},
            'rainbow dash':{}, 'fluttershy':{}}
   
    # Initialize word dictionary with zero for each pony
    words = {words[i]:0 for i in range(len(words))}
    for p in pony_word_count:
        pony_word_count[p] = deepcopy(words)

    with open('initdict.txt', 'w') as f:
        f.write(str(pony_word_count))

    # Group by character
    data['dialog'] = data.groupby(['pony'])['dialog'].transform(lambda x: ' '.join(x))
    data = data.drop_duplicates()

    # Count for each pony
    for i in range(len(data)):
        row = data.iloc[i, :]
        speech = row['dialog'].split()
        for w in speech:
            pony_word_count[row['pony']][w] += 1

    return pony_word_count

def save_to_json(o_fname, data):
    
    with open(o_fname, 'w') as f:
        f.write(json.dumps(data))

def main():
    
    o_fname, dialog_fname = parse_args()
    
    verify_directory(o_fname)

    data, words = clean(dialog_fname)
    
    pony_word_count = word_count(data, words)
    
    save_to_json(o_fname, pony_word_count)
    

if __name__=='__main__':
    main()
