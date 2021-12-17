# Imports
import pandas as pd

# Read from data into dataframe from csv file
# Restrict to first 10000 rows
df = pd.read_csv('/Users/solimlegris/Documents/GitHub/comp598-2021/hw1/submission_template/data/IRAhandle_tweets_1.csv',
                nrows=10000)

# Only keep tweets that are in English
df = df[df['language'] == 'English']

# Get tweets that do not contain a question mark
df_noq = df[~df['content'].str.contains('\?')]

# Save dataframe as tsv
df_noq.to_csv('/Users/solimlegris/Documents/GitHub/comp598-2021/hw1/submission_template/dataset.tsv', sep='\t', index=None)

# Add column with T/F for trump mentions in tweets
mentions = df_noq['content'].str.contains('[\s\W]Trump[\s\W]|[\s\W]Trump$|^Trump[\s\W]|^Trump$', 
                                                           regex=True)
df_noq.loc[:, 'trump_mention'] = mentions

# How many trump mentions?
trump_mentions = df_noq['trump_mention'].sum()
print('There are {} tweets containing mentions of Trump'.format(trump_mentions))

# Select and order columns
df_noq = df_noq[['tweet_id','publish_date','content','trump_mention']]

# Create new version of the dataset
df_noq.to_csv('/Users/solimlegris/Documents/GitHub/comp598-2021/hw1/submission_template/dataset.tsv', sep='\t', index=None)

# Compute the trump statistics and save in dataframe
fraction = df_noq['trump_mention'].sum()/len(df_noq)*100
results = pd.DataFrame({'result': ['frac-trump-mentions'],
                       'value': ['{0:.3f}'.format(fraction)]})

# Save dataframe as tsv file
results.to_csv('/Users/solimlegris/Documents/GitHub/comp598-2021/hw1/submission_template/results.tsv', 
               sep='\t', index=None)

# Look to see if any tweets are duplicated
duplicates = df_noq['content'].duplicated(keep='first').sum()
print('There are {} duplicate tweets'.format(duplicates))