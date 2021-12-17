import pandas as pd
from os.path import dirname, join


curdir = dirname(__file__)
datafile = join(curdir, '..', 'data', 'nyc_311_2020_trimmed.csv')


def main():
	# Load datafile
        data = pd.read_csv(datafile)

        # Add a month column 
        data['month'] = pd.to_datetime(data['Closed Date']).dt.to_period('M')

        # Drop the unique key, created date and closed date columns
        data.drop(['Unique Key', 'Created Date', 'Closed Date'], axis=1, inplace=True)

        # Get rid of negative response times
        data = data[data['response_time'] > 0]

        # Rename incident zip column
        data = data.rename(columns={'Incident Zip':'zip'})

        # Group by zip code and month
        groups = data.groupby(by=['zip', 'month'], as_index=False).mean()
        
        # Pivot data into useable table 
        groups = groups.pivot_table(index='month', columns='zip', values='response_time', fill_value=0.0,
                                    margins=True)

        # Round values to 2 decimal places
        groups = groups.round(2)

        # Remove all row
        groups = groups.drop('All', axis=0)
        
        # Add missing months
        #allmonths = pd.date_range(start='2020-01-01', end='2020-12-01', freq='MS').strftime('%Y-%m')
        #allmonths = [str(f) for f in allmonths]
        #indexmonths = [str(f) for f in groups.index]
        #diff = list(set(allmonths) - set(indexmonths))
        #toadd = pd.to_datetime(diff).to_period('M')
        #for d in toadd:
        #    groups.loc[d] = [0.0 for i in range(groups.shape[1])]
        
        # Reset index
        groups = groups.reset_index()

        # Sort by month
        data = data.sort_values(by='month')

        # Change datetime to month string
        #groups['month'] = groups['month'].dt.strftime('%b')

        # Set index to month
        #groups = groups.set_index('month')

        # Remove index names
        groups.index.name = None

        # Save to csv 
        groups.to_csv(join(curdir, '..', 'data', 'nyc_grouped.csv'))

if __name__ == '__main__':
	main()
