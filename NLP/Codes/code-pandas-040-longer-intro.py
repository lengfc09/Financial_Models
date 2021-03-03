import pandas as pd
import numpy as np

df = pd.read_csv('data-CRSP-extract.csv')

df['date'] = pd.to_datetime(df['date'])
# df['date'] = [time.date() for time in df['date']] # Get rid of time.
df['date'].head() + np.timedelta64(1, 'D')  # Add one day.

# Basic information about the DataFrame.
type(df)
list(df)
df.head()              # Top of df.
df.tail()              # Bottom of df.
df.dtypes              # Data types of columns.
df.shape               # Dimensions
len(df.index)          # Number of rows.
len(df.columns)        # Number of columns.
df.describe            # Basic summary statistics.

# Indexing and selecting data.
df[0:3]                # First three rows.
df.head(3)             # First three rows.
df.iloc[:3]            # First three rows.
df[-1:]                # Last row.
df.tail(1)             # Last row.
df.TICKER              # Same as df['TICKER'], returns a Series.
df[['TICKER']]         # Returns DataFrame. Inner brackets are a list.
df[['TICKER', 'PRC']]  # DataFrame with two columns.

# Querying the data (selecting rows that satisfy some condition(s)).
df[df.TICKER == 'FB']                    # Extract Facebook.
df.query("TICKER == 'FB'")               # Extract Facebook.
df[(df.TICKER == 'FB') & (df.PRC > 120)] # Facebook with price>120.
df.query("TICKER == 'FB' & PRC > 120")   # Facebook with price>120.
df[(df.TICKER == 'FB') | (df.PRC < 120)] # Facebook or price<120 (or both).
df.query("TICKER == 'FB' | PRC < 120") # Facebook or price<120 (or both).
df[df.TICKER.isin(['AAPL', 'FB'])]     # Apple and Facebook.
df.TICKER.unique()                     # All tickers.
df[['TICKER', 'SHROUT']].drop_duplicates() # Two columns w/ unique entries.

# Modify the data.
df.rename(columns={'VOL': 'Volume'}) # New DataFrame with renamed column.
df.rename(columns={'VOL': 'Volume', 'PRC': 'Price'}) # Two columns renamed.
df.assign(HIGH_PRC = (df.PRC > 120))    # New column created.
df.assign(abc = df.PRC + 8 * df.SHROUT) # New column.
df.drop('TICKER', axis = 1)     # New DataFrame without this column.
df.sort_values(by='PRC')        # Sort increasing by PRC.
df.sort_values(by='PRC', ascending=False) # Sort decreasing by PRC.
df.sort_values(by=['SHROUT', 'PRC'], ascending=[False, True])

# Aggregating (summarizing) the data.
df.PRC.max()                    # Maximum price.
df.PRC.min()                    # Minimum price.
df.agg('max')                   # Max applied to all columns.
df.agg(['max', 'min'])          # Max and min applied to all columns.
df.agg({                        # Different aggregations per column.
    'PRC': ['sum', 'max'],
    'VOL': ['max', 'min']})
# Group by ticker and then for each group calculate the maximum and
# the minimum on each column.
df.groupby('TICKER').agg(['max', 'min'])
# Maximum price for each ticker.
df.groupby('TICKER').agg({'PRC': 'max'})
# Maximum price for each ticker and each group of shares outstanding.
df.groupby(['TICKER', 'SHROUT']).agg({'PRC': 'max'})
# Count how many observations have a high price (i.e. PRC>120).
df.\
    assign(HIGH_PRC = (df.PRC > 120)).\
    groupby('HIGH_PRC').\
    agg({'HIGH_PRC': 'count'}).\
    rename(columns={'HIGH_PRC': 'Count'})
pd.DataFrame(                   # Summary statistics on subset.
    {'Max_PRC': [df[0:10].PRC.max()], \
     'Min_PRC': [df[0:10].PRC.min()], \
     'Std_PRC': [np.std(df[0:10].PRC)]})
# Total trading volume for each ticker, assigned to a new column.
df['TVOL'] = df['VOL'].groupby(df['TICKER']).transform('sum')

# Removing columns.
del df['TVOL']                # Delete column.
df.head()                       # Column is gone.
# df.drop('TVOL', axis=1, inplace=True) # Alternative way to delete column.
# df.drop(df.columns[[0, 1, 3]], axis=1, inplace=True) # Delete by column number.
