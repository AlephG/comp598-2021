import argparse
import json
import os.path as osp
import datetime as dt


def parse_args():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='input_file', required=True)
    parser.add_argument('-o', help='output_file', required=True)
    args = parser.parse_args()

    return args


def load_json(fname):
    # Create empty list for json entries
    data = []
    # Read the json file and load each line as a json object 
    with open(fname) as f:
        for line in f:
            # Try loading the line as a json object, if it fails pass that line
            try:
                data.append(json.loads(line))
            except ValueError:
                continue

    return data

def verify_title(entry):

    # Verify that title or title_text field exists
    if 'title' not in entry and 'title_text' not in entry:
        return None
    # Replace with title when title_text
    elif 'title_text' in entry:
        entry['title'] = entry.pop('title_text')
    return entry

def standardize_dt(entry):
    # Standardize 'createdAt'
    if 'createdAt' in entry:
        # If string cannot be converted to datetime using ISO datetime standard, discard entry
        try:
            time = dt.datetime.strptime(entry['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            return None

        # Convert to UTC timezone
        time = time.astimezone(dt.timezone.utc)

        # Convert time back to string
        time = dt.datetime.strftime(time, '%Y-%m-%dT%H:%M:%S%z')

        # Save back into dictionary 
        entry['createdAt'] = time

    return entry


def verify_author(entry):
    # Verify contents of 'author' 
    if 'author' in entry:
        if entry['author'] == '' or entry['author'] == None or entry['author'] == 'N/A':
            return None
    return entry

def cast_totalcount(entry):
    # Cast contents of 'total_count' to int
    if 'total_count' in entry:
        try:
            entry['total_count'] = int(float(entry['total_count']))
        except:
            return None
    return entry

def parse_tags(entry):
    # Verify the contents of tags
    if 'tags' in entry:
        # TODO Make sure this is enough ie no edge cases
        entry['tags'] = [tags for strings in entry['tags'] for tags in strings.split()]
    return entry

def clean_data(json_entries):
    clean_data = []

    for entry in json_entries:

        if verify_title(entry) is None:
            continue

        if standardize_dt(entry) is None:
            continue

        if verify_author(entry) is None:
            continue

        if cast_totalcount(entry) is None:
            continue
        
        parse_tags(entry)

        clean_data.append(entry)

    return clean_data 

def write_json(data, out_fname):
    with open(out_fname, 'w') as f:
        for i, entry in enumerate(data):
            f.write(json.dumps(entry))
            if i != (len(data) - 1):
                f.write('\n')


def main():
    
    args = parse_args()
    in_fname = args.i
    out_fname = args.o
    
    json_entries = load_json(in_fname)
    
    data = clean_data(json_entries)

    write_json(data, out_fname)

if __name__=='__main__':
    main()
