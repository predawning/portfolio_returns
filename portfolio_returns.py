import numpy as np
import pandas as pd
import pandas_datareader.data as web

#stocks = ['AAPL','MSFT','AMZN','YHOO']
stocks = ['AAPL']

#download daily price data for each of the stocks in the portfolio
data = web.DataReader(stocks,data_source='yahoo',start='01/01/2017')['Adj Close']

#convert daily stock prices into daily returns
#returns = data.pct_change()

#print(returns)

def cal_pct_changes(closes):
    return closes.pct_change()

def cal_log_returns(closes):
    #return np.log(closes/closes.shift(1))
    return np.log(closes) - np.log(closes.shift(1))

def cal_log_returns2(pct_changes):
    return np.log(1 + pct_changes)

def cal_cum_returns(pct_changes):
    return (1 + pct_changes.fillna(0)).cumprod() - 1

def cal_cum_returns2(log_returns):
    return np.exp(log_returns.cumsum()) - 1

closes = data.copy(deep=True)
#print(data)

pct_changes = cal_pct_changes(closes)
data['pct_change'] = pct_changes

cum_returns = cal_cum_returns(pct_changes)
data['cum_return'] = cum_returns


log_returns = cal_log_returns(closes)
data['log_return'] = log_returns

#log_returns2 = cal_log_returns2(pct_changes)
#data['log_return2'] = log_returns2

cum_returns2 = cal_cum_returns2(log_returns)
data['cum_return2'] = cum_returns2

#print(data.tail(10))

def create_portfolio(tickers, weights=None):
    if (weights is None):
        weights = np.ones(len(tickers))/len(tickers)
    portfolio = pd.DataFrame({'Tickers': tickers,
                              'Weights': weights},
                              index=tickers)
    return portfolio


def calculate_weighted_portfolio_value(portfolio, returns, name='Value'):
    total_weights = portfolio.Weights.sum()
    weights = portfolio.Weights/total_weights
    weighted_returns = returns * weights
    return pd.DataFrame({name: weighted_returns.sum(axis=1)})


postions = {'AAPL': 100, 'MSFT': 100}
stocks = list(postions.keys())

#download daily price data for each of the stocks in the portfolio
prices = web.DataReader(stocks, data_source='yahoo',start='01/01/2016')['Adj Close']
portfolio = create_portfolio(stocks, [100, 100])
print(portfolio)

def test_case(prices, portfolio):

    #1 daily return , weight it, cumulative it, there is errors
    returns = cal_pct_changes(prices)
    weighted_returns = calculate_weighted_portfolio_value(portfolio, returns)
    cum_wr = cal_cum_returns(weighted_returns)

    # calculate the cumalative return first, then apply the weight
    cum_r = cal_cum_returns(returns)
    weighted_cum_r = calculate_weighted_portfolio_value(portfolio, cum_r, 'Value-1')

    #2 calaculate the log return , apply the weight, at last cumulative it
    returns2 = cal_log_returns(prices)
    weighted_returns2 = calculate_weighted_portfolio_value(portfolio, returns2, 'Value2')
    cum_wr2 = cal_cum_returns2(weighted_returns2)

    # calculate the cumalative return first, then apply the weight, there is errors
    cum_r2 = cal_cum_returns2(returns2)
    #print(cum_r2)
    weighted_cum_r2 = calculate_weighted_portfolio_value(portfolio, cum_r2, 'Value2-1')

    plus1_cum_r2 = cum_r2 + 1
    #print(plus1_cum_r2.to_dict())


    result = pd.concat([returns, weighted_returns, cum_wr, weighted_cum_r,
                                weighted_returns2, cum_wr2, weighted_cum_r2], axis=1)

    print(result.tail(10))

    # summary: the weighted_cum_r and weighted_cum_r2 are same, they are no errors
    # cum_wr and cum_wr2 acuumulated errors

def test_case2(prices, portfolio):
    returns2 = cal_log_returns(prices)
    # calculate the cumalative return first, then apply the weight, there is errors
    cum_r2 = cal_cum_returns2(returns2)
    weighted_cum_r2 = calculate_weighted_portfolio_value(portfolio, cum_r2, 'Value')

    #print(plus1_cum_r2.to_dict())


    result = pd.concat([returns2, weighted_cum_r2], axis=1)

    print(result.tail(10))

test_case(prices, portfolio)
#test_case2(prices, portfolio)

