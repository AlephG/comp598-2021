# Reddit API and web scraping project

## Setup

After cloning the repository, do the following.

### Dependencies

#### Using conda

Run `conda create --name <envname> --file requirements.txt`.

#### Using pip

Run `pip -r requirements.txt`.

### Dotenv

Create a .env file with required variables for authentication.

## First part: Collecting data and exploring bias
In the first part of the assignment, data is collected and analyzed for average post title length using the Reddit API. Two different sampling methods are used for comparison: collecting 1000 new posts from the 10 most popular subreddits by subscribers and collecting 1000 new posts from the most popular subreddits by # of posts per day.

### Running

1. Run `python3 collect.py` to collect the data from the Reddit API
2. Run `python3 compute_average_length.py <input_file>` to compute the average length for sample1.json or sample2.json

## Second part: Scraping celebrity relationships
In this part of the assignment, data is scraped using HTML webpages downloaded from celebrity profiles on [https://www.whosdatedwho.com/]. Relationship information for each celebrity is outputted in a JSON format file.

### Running

1. Run `python3 collect_relationships.py -c <config-file.json> -o <output_file.json>`
