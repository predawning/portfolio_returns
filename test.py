import numpy as np
import pandas as pd
import pandas_datareader.data as web

"""
this test is demo to show the cumulative returns calculation
which is usually the simple daily returns line

refs: 'Mastering pandas For finance'

https://github.com/quantopian/zipline/issues/29

"""

#stocks = ['AAPL','MSFT','AMZN','YHOO']
stocks = ['AAPL']

#download daily price data for each of the stocks in the portfolio
data = web.DataReader(stocks,data_source='yahoo',start='01/01/2017')['Adj Close']
simple_ret = data.pct_change()
#print(simple_ret)
print((1+simple_ret).cumprod()-1)
#print((1+simple_ret).cumprod().iloc[-1]-1)

log_return = np.log(data/data.shift(1))
#print(log_return.cumsum().iloc[-1])
#print(log_return)
print(np.exp(log_return.cumsum())-1)
#print(np.exp(log_return.cumsum().iloc[-1]) -1)

print('='*20)
print('voltality')
print(np.sqrt(252*log_return.var()))

