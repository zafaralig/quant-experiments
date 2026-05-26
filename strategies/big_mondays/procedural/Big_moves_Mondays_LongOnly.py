# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:23:14 2022

@author: Zafar.Ahmed
"""

import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('ignore')


def download_daily_data(ticker, start, end):
    """
    Parameters
    ----------
    ticker : String
        DESCRIPTION.
    start : datetime
        DESCRIPTION.
    end : datetime
        DESCRIPTION.

    Returns: DataFrame containing Daily Data
    -------
    None.

    """
    
    data = yf.download(ticker, start, end)
    return data


def compute_daily_log_returns(data):
    """
    
    """
    data['cc_returns'] = np.log(data['Close'] / data['Close'].shift(1))
    return data

def compute_indicators(data):
    
    # columns to check condition1
    data['day'] = data.index.day_name()
    data['prev_day'] = data['day'].shift(1)
    data['four_days_after'] = data['day'].shift(-4)
    
    # columns to check condition 2
    data['relative_range'] = (data['High'] - data['Low']) / data['Close']
    data['rel_range_ma'] = data['relative_range'].rolling(window=25).mean()
    
    # column to check condition 3
    data['ibs'] = (data['Close'] - data['Low']) / (data['High'] - data['Low'])
    
    return data

def backtest_strategy(data):
    data['condition1'] = np.where((data['day']=="Monday") & (data['prev_day']=="Friday") & (data['four_days_after']=="Friday"),
                                  1,0)
    data['condition2'] = np.where((1-data['Close']/data['Close'].shift(1))>=0.25*data['rel_range_ma'],
                                  1,0)
    data['condition3'] = np.where(data['ibs']<0.3,1,0)
    
    data['signal'] = np.where((data['condition1']==1) & (data['condition2']==1) & (data['condition3']==1),
                              1,0)
    data['signal'] = data['signal'].shift(1)
    data['position'] = data['signal'].replace(to_replace=0,method='ffill',limit=3)
    data['strategy_returns'] = data['cc_returns'] * data['position']

def show_backtesting_results(data):
    print('Buy and hold returns: ',np.round(data['cc_returns'].cumsum()[-1],3))
    print('Strategy returns: ',np.round(data['strategy_returns'].cumsum()[-1],3))
    
    data[['cc_returns','strategy_returns']] = data[['cc_returns','strategy_returns']].cumsum()
    data[['cc_returns','strategy_returns']].plot(grid=True, figsize=(12,8))

ticker2 = 'SPY'
end2 = datetime.date(2020,7,2)
# end2 = datetime.date.today() #this can be used to download from todays date
start2 = end2 - pd.Timedelta(days=365*15) # pd.Timedelta(days=days*(#years))

df_orignal = download_daily_data(ticker2, start2, end2)

df = df_orignal.copy()

compute_daily_log_returns(data=df)

compute_indicators(data=df)

backtest_strategy(data=df)

show_backtesting_results(data=df)














