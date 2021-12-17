# Russian Troll Tweet Analysis
In this project, I looked at tweets from Russian Trolls from during the US 2016 elections. We analyze the frequency of Trump mentions in these tweets.

## Setup 
After cloning the repository, do the following.

### Dependencies
#### Using conda

Run `conda create --name <envname> --file requirements.txt`.

#### Using pip

Run `pip -r requirements.txt`.

### Data
The small dataset contained in `data/` is from https://github.com/fivethirtyeight/russian-troll-tweets/.

## Running 

Run `python3 clean_data.py`


## Results

We find that the 2.25% of tweets mention Trump. 

### Caveats
After looking at the dataset, it was found that there were 23 duplicate tweets. This means we are over-counting the number of Trump occurrences in the dataset. This issue can be remediated by removing duplicates.
