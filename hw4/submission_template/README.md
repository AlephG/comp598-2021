# New York City Dashboard Project

In this project, I setup a simple password protected Bokeh dashboad that allows users to compare average monthly incident response times of different areas to the city's average monthly incident response time in 2020. This project was done in the context of COMP598: Data Science at McGill University.

## Setup

1. First download the dataset into the data directory from https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9

2. Run the trim-2020.sh script from the command line to generate a dataset restricted to 2020 incidents.

3. Run src/trim-data.ipynb to further trim the data and explore it.

4. Run src/preprocess.py to prepare the data for the Bokeh dashboard

## Running

1. Use the command `bokeh serve nyc_dash --port PORT --auth-module path\to\nyc-dash\auth.py`

2. Access the Bokeh dashboard through your browser!


