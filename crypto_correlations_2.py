import pandas as pd
import pandas_datareader as web
import mplfinance as mpf
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import requests

pd.set_option('display.max_columns', 30)
req = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=25'
                   '&page=1&sparkline=false')
dataj = req.json()
li = [item.get('symbol').upper() for item in dataj]
ignore_usd = [x for x in li if not (x.endswith('USD') | x.startswith('USD'))]
list1 = ['WBTC', 'UST', 'DAI', 'STETH', 'CETH']
filtered = [x for x in ignore_usd if all(y not in x for y in list1)]

print(filtered)

currency = "USD"
metric = "Close"

start = dt.datetime(2021, 1, 12)
end = dt.datetime.now()

# crypto = ['BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'LUNA', 'AVAX', 'LTC', 'XRP', 'SOL', 'MATIC', 'LINK']
colnames = []

first = True

for ticker in filtered:
    data = web.DataReader(f"{ticker}-{currency}", "yahoo", start, end)
    if first:
        combined = data[[metric]].copy()
        colnames.append(ticker)
        combined.columns = colnames
        first = False
    else:
        combined = combined.join(data[metric])
        colnames.append(ticker)
        combined.columns = colnames

# # Correlation Heat Map

print(combined)

combined = combined.pct_change().corr(method='pearson')

sns.heatmap(combined, annot=True, cmap="coolwarm")
plt.show()
