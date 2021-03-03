# This script illustrates downloading financial data from
# AlphaVantage.

# Your AlphaVantage key. In order to download the data, you can get a
# key directly from the AlphaVantage website for free.
mykey = 'demo'

# Specify the stock ticker here. You can also use stock indices,
# e.g. IXIC (Nasdaq Composite), DJI (Dow Jones Industrial Average),
# INX (S&P 500) etc. You can also get data from stock markets around
# the world. For example, 'NSE:TITAN' gets the stock value of TITAN
# from the Indian Exchange NSE, or 'AI.PA' is for Air Liquide at the
# Paris stock exchange (PA).
myticker = 'MSFT'

import matplotlib.pyplot as plt
import pandas as pd

# Here we manually download some data from AlphaVantage, using only
# the Pandas package.
df = \
    pd.read_csv(
        'https://www.alphavantage.co/query?' + \
        'function=TIME_SERIES_DAILY_ADJUSTED&' +\
        'symbol=' + myticker + \
        '&apikey=' + mykey + \
        '&datatype=csv')
# Take a look at the data we just downloaded. Keep in mind that
# AlphaVantage gives you the raw data sorted DESCENDINGLY based on the
# timestamp.
df.head()
df.sort_values(by='timestamp', inplace=True) # Sort by `timestamp`.
df.reset_index(drop=True, inplace=True) # Reset the index to 0,1,2,3...
df.timestamp = pd.to_datetime(df.timestamp).dt.date # Convert to datetime and discard time.
# Plot the stock price, adjusted for dividends and stock splits.
df.plot(x='timestamp', y='adjusted_close')
plt.title(myticker + ' Stock Price')
plt.show()

# Calculate stock return.
df['L_close'] = df.adjusted_close.shift() # Lag the closing price.
df['RET'] = df.close / df.L_close - 1 # Calculate stock index return.
df.dropna(inplace=True)        # Drop missing data.
df.reset_index(drop=True, inplace=True) # Reset the index to 0,1,2,3...

# Cut returns into low (0), medium (1), and high (2) returns based on
# quantiles.
df['q_RET'] = pd.qcut(df.RET, 3, labels=False)
df[df.q_RET == 2].head()        # Show examples of high returns.
df[df.q_RET == 2].RET.mean()    # Mean return of high quantile.



from pprint import pprint       # For pretty printing.
# Here we import a bunch of things from the `alpha_vantage`
# package. Depending on what you want to download, you just need some
# of these imports.
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange


# You can get the data in JSON format if you like. However, most of
# the time it is better to ask for a Pandas DataFrame as we do in the
# remaining examples.
ts = TimeSeries(key=mykey)      # In JSON by default.
data, meta_data = ts.get_daily_adjusted(symbol=myticker)
pprint(data)

# Here we request a Pandas DataFrame, which often is more convenient
# to work with.
ts = TimeSeries(key=mykey, output_format='pandas')
# Get object with data and another with the call's metadata. By
# default, it just returns a subset of the data. If you want the whole
# dataset, use `outputsize='full'` as an additional function argument.
data, meta_data = ts.get_daily_adjusted(symbol=myticker)
# Plot the data.
data['5. adjusted close'].plot()
plt.title('Times Series for ' + myticker)
plt.show()

# Bollinger Bands.
ti = TechIndicators(key=mykey, output_format='pandas')
data, meta_data = ti.get_bbands(symbol=myticker, time_period=20)
data.tail(252).plot()           # Plot last year only.
plt.title('BBbands indicator for ' + myticker)
plt.show()

# Sector performance.
sp = SectorPerformances(key=mykey, output_format='pandas')
data, meta_data = sp.get_sector()
data['Rank G: Year Performance'].plot(kind='bar')
plt.title('Sector Performance (Year)')
plt.tight_layout()
plt.grid()
plt.show()

# Crypto currencies.
cc = CryptoCurrencies(key=mykey, output_format='pandas')
data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='CNY')
data['4b. close (USD)'].plot(logy=True)
plt.tight_layout()
plt.title('Daily Value for Bitcoin (BTC)')
plt.grid()
plt.show()

# Foreign exchange data is only available as JSON format (not in CSV
# or Pandas format). There's also no metadata in this call (so we just
# use a placeholder `_`).
cc = ForeignExchange(key=mykey)
data, _ = cc.get_currency_exchange_rate(from_currency='EUR', to_currency='USD')
pprint(data)
