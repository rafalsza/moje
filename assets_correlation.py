import pandas as pd
from binance.client import Client
import numpy as np
import seaborn as sns
import requests
import matplotlib.pyplot as plt
from loguru import logger
import yfinance as yf

pd.set_option('display.max_columns', 10)

relevant = ['BTC-USD', 'ETH-USD', '^GSPC', '^DJI', 'TSLA', 'ARKK', 'AAPL', 'MSFT', 'FB', 'GC=F']


@logger.catch
def getdailydata(symbol):
    frame = yf.download(symbol, period='max', interval="1d")
    frame = frame.dropna()
    return frame


dfs = []
for coin in relevant:
    dfs.append(getdailydata(coin))

mergeddf = pd.concat(dict(zip(relevant, dfs)), axis=1)
# rename columns
mergeddf = mergeddf.rename(columns={'GC=F': 'GOLD', '^DJI': 'DOW JONES', '^GSPC': 'S&P500'})
closesdf = mergeddf.loc[:, mergeddf.columns.get_level_values(1).isin(['Close'])]
closesdf.columns = closesdf.columns.droplevel(1)
logretdf = np.log(closesdf.pct_change() + 1)
filtered_corr = logretdf.corr()

print(filtered_corr)
sns.heatmap(filtered_corr, annot=True, cmap="coolwarm")
plt.title('Assets correlation')
plt.show()
