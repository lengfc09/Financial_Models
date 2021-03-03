import pandas as pd
import numpy as np
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals()) # Shortcut function.

# Import CRSP and convert the date strings to `datetime64`.
crsp = pd.read_csv('data-CRSP-extract.csv')
crsp['date'] = pd.to_datetime(crsp['date'])

# Same for Compustat.
cs = pd.read_csv('data-Compustat-extract.csv')
cs['datadate'] = pd.to_datetime(cs['datadate'])

# Next we define the time window during which the accounting
# information from Compustat is valid. First, we wait for three months
# before using any Compustat data. The reason is that in real life,
# the data is often released with a lag. For example, if a company's
# balance sheet is as of December 31, 2014, it is often released in
# January or February 2015. To be on the safe side, we therefore add
# three months to `datadate`. This date corresponds to the BEGINNING
# of the time window we will use when merging.
cs['datadate'] = cs['datadate'] + np.timedelta64(121, 'D')
# Second, we let the accounting data expire after about one year. This
# date corresponds to the END of the time window we will use when
# merging.
cs['datadate2'] = cs['datadate'] + np.timedelta64(380, 'D')

# Extract a subset of the data for better illustration of the
# following merge. `PRC` is the stock price and `atq` is total assets.
crsp = crsp[['TICKER', 'date', 'PRC']]
cs = cs[['tic', 'datadate', 'datadate2', 'atq']]

# Inspect the data. Our GOAL in the remaining code is to add Compustat
# data to CRSP such that `date` (from CRSP) lies in the time window
# given by `datadate` and `datadate2` (from Compustat).
crsp.tail()
cs.tail()

# Here we use SQL syntax to merge the two DataFrames using a left join
# (i.e. we add data to CRSP from Compustat because the `crsp`
# DataFrame is mentioned to the "left" side of the `cs` DataFrame in
# the `FROM ...` part of the SQL query). The following merge could be
# done in a more memory-efficient way completely in SQL. But for
# simplicity we show this version first. `SELECT *` means to select
# all columns from the resulting merged data. In the `ON...` part, in
# order to tell SQL the DataFrame and column it should use, we add the
# DataFrame name in front of the column, separated by a dot. For
# example, `crsp.TICKER` means that we are referring to the `TICKER`
# column from the `crsp` DataFrame.
df1 = \
    pysqldf(
        'SELECT * ' + \
        'FROM crsp LEFT JOIN cs ' + \
        'ON crsp.TICKER=cs.tic AND ' + \
        'crsp.date BETWEEN cs.datadate AND cs.datadate2')
# Clean up the result from the merge. PandaSQL converts `datetime64`
# to `str`. So we need to convert it back to `datetime64` here.
df1['date'] = pd.to_datetime(df1['date'])
df1['datadate'] = pd.to_datetime(df1['datadate'])
df1['datadate2'] = pd.to_datetime(df1['datadate2'])
# Let's take a look at the resulting merge. The first thing you should
# notice is that `date` is always between `datadate` and
# `datadate2`. So we were successful in adding data to CRSP based on
# the time window specified in Compustat through `datadate` (the
# beginning of the time window) and `datadate2` (the end of the
# window).
df1.tail()
# There's still one problem we need to solve. The merge has added ALL
# rows from Compustat that fit the merging criteria, i.e. whose time
# window contains a `date` from CRSP. So for each observation
# originally in CRSP, we now have around FOUR observations. One for
# each quarter from Compustat whose one-year time window between
# `datadate` and `datadate2` matches a given `date` from CRSP. If you
# look closely at the `date` column, you will see that many dates are
# repeated.
df1.tail()
# You can look at these multiple matches from a different angle by
# counting how many matches from Compustat we have on average for each
# Ticker-date combination. For illustration, we look at the `size()`
# of each ticker-date group and save it in the column name
# `counts`. This gives us the number of observations we have for each
# ticker and each date. Most of these values turn out to be four as we
# typically have four observations in Compustat per year (i.e. four
# quarters). To further summarize this, we then calculate the mean of
# the `count` column for each ticker. (When entering the code below,
# make sure to add NO SPACE after the the backslashes `\`, otherwise
# it won't work.)
df1.\
    groupby(['TICKER', 'date']).\
    size().\
    to_frame(name='counts').\
    reset_index().\
    groupby('TICKER').\
    agg({'counts': 'mean'})
# To finally solve this problem of the multiple matches, we only keep
# the most recent match from Compustat and discard all the others. To
# do that, we first need to sort by `datadate` to ensure we are
# picking the latest information from Compustat. (Keep in mind that
# the following code works because `groupby()` preserves the order.)
# Then we grab the latest observation in each ticker-date group using
# `tail()` and thus discard all the earlier observations.
df1 = df1.sort_values('datadate').groupby(['TICKER', 'date']).tail(1)
df1 = df1.sort_values(by=['TICKER', 'date']).reset_index(drop=True) # Cosmetics.
df1.tail()   # Inspect the data. Now there is only ONE date per ticker.
del df1['datadate2']

# The approach above works, but it is a bit clumsy. First, it might
# require a lot of memory if your data size gets larger because the
# SQL query keeps a lot of data that we don't need in the end. Second,
# it would be more elegant if we can perform the whole merge directly
# in SQL without having to remove some data using Pandas at the
# end. We will show how to solve these two problems next.

# The following code gives the same result, but the whole merging is
# done in SQL and it is more memory-friendly in case your dataset is
# large. The reason is that SQL has some internal optimizations it can
# perform when executing the query. Here it is important to keep in
# mind the order of execution of the SQL statements: 1) FROM ... LEFT
# JOIN ... ON ... (specifies which DataFrames to use and the kind of
# join to perform), 2) GROUP BY (specifies the grouping), 3) SELECT
# (specifies which columns to select; `*` means all columns and
# `MAX(cs.datadate)` takes the maximum value of `datadate` from the
# `cs` DataFrame in each group and discards all other observations in
# the group).
df2 = \
    pysqldf(
        'SELECT *, MAX(cs.datadate) ' + \
        'FROM crsp LEFT JOIN cs ' + \
        'ON crsp.TICKER=cs.tic AND ' + \
        'crsp.date BETWEEN cs.datadate AND cs.datadate2 ' + \
        'GROUP BY crsp.TICKER, crsp.date')
df2['date'] = pd.to_datetime(df2['date'])
df2['datadate'] = pd.to_datetime(df2['datadate'])
df2.drop(['MAX(cs.datadate)', 'datadate2'], axis=1, inplace=True) # Remove columns.
df2 = df2.sort_values(by=['TICKER', 'date']).reset_index(drop=True) # Cosmetics.

# Inspect the data. It should be same as with `df1`.
df2.tail()

# Check if both DataFrames are the same. They should be the same as
# both ways of merging should yield the same results.
df2.equals(df1)
