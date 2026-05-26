"""
@author: Zafar.Ahmed
"""

import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import pyfolio as pf
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class big_mondays_moves:
    
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        
        self.fetch_data()
        self.compute_daily_log_returns()
        self.indicators()
        self.backtest_strategy()
        self.show_backtesting_results()
    
    def fetch_data(self):
        self.df = yf.download(self.ticker, self.start_date, self.end_date)
        
    def compute_daily_log_returns(self):
        self.df['cc_returns'] = np.log(self.df['Close'] / self.df['Close'].shift(1))

    def indicators(self):
        self.df['day'] = self.df.index.day_name()
        self.df['prev_day'] = self.df['day'].shift(1)
        self.df['four_days_after'] = self.df['day'].shift(-4)
        
        self.df['relative_range'] = (self.df['High'] - self.df['Low']) / self.df['Close']
        self.df['rel_range_ma'] = self.df['relative_range'].rolling(window=25).mean()
        
        self.df['ibs'] = (self.df['Close'] - self.df['Low']) / (self.df['High'] - self.df['Low'])
    
    def backtest_strategy(self):
        self.df['condition1'] = np.where((self.df['day']=="Monday") & (self.df['prev_day']=="Friday") & (self.df['four_days_after']=="Friday"),
                                      1,0)
        self.df['condition2'] = np.where((1-self.df['Close']/self.df['Close'].shift(1))>=0.25*self.df['rel_range_ma'],
                                      1,0)
        self.df['condition3'] = np.where(self.df['ibs']<0.3,1,0)
        
        self.df['signal'] = np.where((self.df['condition1']==1) & (self.df['condition2']==1) & (self.df['condition3']==1),
                                  1,0)
        self.df['signal'] = self.df['signal'].shift(1)
        self.df['position'] = self.df['signal'].replace(to_replace=0,method='ffill',limit=3)
        self.df['strategy_returns'] = self.df['cc_returns'] * self.df['position']
    def show_backtesting_results(self):
        print('Buy and hold returns: ',np.round(self.df['cc_returns'].cumsum()[-1],3))
        print('Strategy returns: ',np.round(self.df['strategy_returns'].cumsum()[-1],3))
    
        self.df[['cc_returns','strategy_returns']] = self.df[['cc_returns','strategy_returns']].cumsum()
        self.df[['cc_returns','strategy_returns']].plot(grid=True, figsize=(12,8))


# =============================================================================
# Run below code to call above Class
# =============================================================================

ticker2 = 'SPY'
end2 = dt.date(2020,7,2)
# end2 = datetime.date.today() #this can be used to download from todays date
start2 = end2 - pd.Timedelta(days=365*15) # pd.Timedelta(days=days*(#years))

df_orignal = big_mondays_moves(ticker2, start2, end2)