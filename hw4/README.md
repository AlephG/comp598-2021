# New York City Dashboard Project

In this project, I setup a simple password protected Bokeh dashboad on an Amazon EC2 instance that allows users to compare average monthly incident response times of different areas to the city's average monthly incident response time in 2020. This project was done in the context of COMP598: Data Science at McGill University.

Note: the server does not exist anymore.

## Setup

1. First download the dataset into the data directory from https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9

2. Run the following command in your terminal: `egrep '^\d+,.{6}2020' DATASET_FILENAME >> nyc_311_2020.csv`

3. Run src/trim-data.ipynb to further trim the data and explore it.

4. Run src/preprocess.py to prepare the data for the Bokeh dashboard

## Running

1. Use the command `bokeh serve nyc_dash --port PORT --auth-module path\to\nyc-dash\auth.py`

2. Access the Bokeh dashboard through your browser!


