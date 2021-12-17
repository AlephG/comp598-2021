# University Subreddit Comparison
In this project, I explore data annotation and the issues faced by data scientists themselves or people assisting data scientists in their work. Data is scraped from McGill University and Concordia University subreddits. Cleaned data files are then manually annotated using four categories:

category          |code
------------------|----
course-related    |c
residence-related |r
food-related      |f
other             |o

## Setup

After cloning the repository, do the following.

### Dependencies

#### Using conda

Run `conda create --name <envname> --file requirements.txt`.

#### Using pip

Run `pip -r requirements.txt`.

### Dotenv

Create a .env file with required variables for authentication.

## Running

### Collecting the data

Run `python3 collect.py`

### Generating TSV files for annotation

Run `python3 extract_to_tsv.py`

Now that you have extracted post names and titles, annotate them manually. Two examples are provided: annotated_concordia.tsv and annotated_mcgill.tsv.


### Analyze the distribution of categories 

Run `python3 analyze.py` to analyze the distribution of categories.

