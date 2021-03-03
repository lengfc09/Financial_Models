# This script calculated cumulative stock returns and plots them.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Here we import the data and select the columns we need.
df = pd.read_csv('data-CRSP-extract.csv')
df['date'] = pd.to_datetime(df['date']) # Convert string to `datetime64`.
df = df[['TICKER', 'date', 'RET']] # Just ticker, date, and stock returns.

# Calculate the cumulative stock returns. They show by how much each
# stock price has gone up or down during our sample's time period.
df.RET = np.log(1 + df.RET) # Convert to log-returns so that we can sum them up.
df = df.sort_values(['TICKER', 'date']) # Ensure data is sorted before running `cumsum`.
df['cum_RET'] = \
    df.\
    groupby('TICKER')['RET'].\
    apply(lambda x: x.cumsum()) # For each ticker, calculate cumulative sum.
df.cum_RET = np.exp(df.cum_RET) - 1 # Convert log returns to linear returns.
del df['RET']  # Don't need raw returns any more for this application.

# Reshape the data to have each ticker in a separate column. The
# `pivot()` method can save a lot of work if you compare it to
# reshaping the data yourself using for-loops! Keep in mind that here
# we specify `date` as the index, which is useful for the subsequent
# plotting commands, as the date will automatically be put on the
# x-axis.
df = df.pivot(index='date', columns='TICKER', values='cum_RET')

# Plot the cumulative stock returns for all stocks (i.e. in this case,
# for all columns).
df.plot()
plt.title('Cumulative Stock Returns')
plt.show()
