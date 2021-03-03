# This script shows how to calculate monthly trading volume and merge
# it back to daily data.

import pandas as pd
import numpy as np

df = pd.read_csv('data-CRSP-extract.csv') # Import from CSV file.
df['date'] = pd.to_datetime(df['date'])   # Convert to date (and time).
df = df[['TICKER', 'date', 'PRC', 'VOL']] # Just need a few columns.

# Calculate monthly trading volume. We first extract the columns we
# need from the original `df` DataFrame, group it by ticker and month,
# and sum up the (monthly) volume.
mvol = df[['TICKER', 'date', 'VOL']]
mvol = mvol.groupby(['TICKER', pd.Grouper(key='date', freq='M')]).sum().reset_index()
mvol.rename(columns={'VOL': 'MVOL'}, inplace=True) # Rename column.

# Take a look at the data. You can see that here we have ONE
# observation per ticker and per month.
mvol.tail()

# Here we create a column in each DataFrame that has the day removed,
# so we only have year and month. This is necessary for merging both
# DataFrames (`df` and `mvol`) together in a later step where we use
# the year-month information to link up both DataFrames.
mvol['mdate'] = mvol.date.dt.to_period('M') # Convert to monthly dates.
del mvol['date']                            # Not needed any more.
df['mdate'] = df.date.dt.to_period('M') # Convert to monthly dates.

# Convert year-month to string. Although not strictly necessary, it
# makes some things easier to handle, e.g. querying a DataFrame in the
# subsequent step.
df['mdate'] = df.mdate.astype(str)
mvol['mdate'] = mvol.mdate.astype(str)

# Here we select some subsets of both DataFrames. In production, you
# would SKIP this step. Here we use it only to better illustrate the
# following merge to have a small result we can actually look at and
# inspect.
df = df.query("TICKER == 'AAPL' & date >= '2014-12-20' & date <= '2015-01-15'")
mvol = mvol[(mvol.TICKER == 'AAPL') & (mvol.mdate >= '2014-11') & (mvol.mdate <= '2015-02')]

# Next we merge both DataFrames together using the ticker symbol
# (`TICKER`) and a column representing the year-month (`mdate`). Here
# we are using a so-called "left join," which is for our purposes the
# most important kind of join. It means that we are adding data to the
# "left" DataFrame `df` (instead of the "right" DataFrame `mvol`). The
# data added comes from the "right" DataFrame `mvol`. We use "left"
# and "right" because in the call to `pd.merge`, the `df` DataFrame
# comes first, so is on the "left" side, while `mvol` is on the
# "right" side.
df_mvol = pd.merge(df, mvol, how='left', on=['TICKER', 'mdate'])

# Take a look at the two original DataFrames `df` and `mvol` and the
# merged DataFrame `df_mvol`. It will hopefully become clear what has
# happened during the merge, i.e. information about monthly trading
# volume from `mvol` has been added to `df`. Observe that if there is
# a row in `mvol` with no match in `df`, then this row from `mvol`
# will NOT be included in the merged DataFrame `df_mvol`. For example,
# the rows from November and February 2014 are in `mvol`, but they are
# NOT added to `df_mvol` because there is no matching row in `df`.
df
mvol[['TICKER', 'mdate', 'MVOL']]
df_mvol

# Finally we can delete the `mdate` column as we don't need it any
# more.
del df_mvol['mdate']

# Here is our final result, with monthly trading volume added to each
# observation (i.e. to each row).
df_mvol
