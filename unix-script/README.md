# UNIX and Data Filtering
In this project, I explore standard data science tools. Notably, I write a data filtering script using Bash to speed up data exploration and compute speech verbosity for My Little Pony speech acts.


## Setup 

### Dependencies

#### Using conda

Run `conda create --name <envname> --file requirements.txt`.

#### Using pip

Run `pip -r requirements.txt`.

### Data
The data for this project is from [https://www.kaggle.com/liury123/my-little-pony-transcript].
## Running

Run `stats.sh [sample.csv]` to print .csv file statistics

Run `dialog_analysis.py -o output.json clean_dialog.csv` to compute and produce a JSON formatted pony verbosity file. 

