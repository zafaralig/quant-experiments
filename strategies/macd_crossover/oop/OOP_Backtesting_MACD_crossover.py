"""
@author: Zafar.Ahmed
"""

import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
# import pyfolio as pf
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class backtesting_MACD_crossover:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        
        self.fetch_data()
        self.MACD()
        self.signals()
        self.positions()
        self.returns()
        
    def fetch_data(self):
        self.df = yf.download(self.ticker, self.start_date, self.end_date)

    def MACD(self):
        self.df['ema26'] = self.df['Close'].ewm(span=26,adjust=False).mean()
        self.df['ema12'] = self.df['Close'].ewm(span=12,adjust=False).mean()
        self.df['MACD'] = self.df['ema12'] - self.df['ema26']
        
    def signals(self):
        self.df['signal'] = self.df['MACD'].ewm(span=9, adjust=False).mean()
        self.df[['signal','MACD', 'Close']].plot(figsize=(12,8),grid=True,secondary_y = 'Close')
        
    def positions(self):
        self.df['position'] = np.where(self.df['MACD']>self.df['signal'],1,-1)
        self.df['position'] = self.df['position'].shift(1)
        
    def returns(self):
        self.df['cc_returns'] = self.df['Close'].pct_change()
        self.df['strategy_returns'] = self.df['cc_returns'] * self.df['position']
        self.df['cumulative_returns'] = (1 + self.df['strategy_returns']).cumprod() - 1
        self.df[['cumulative_returns']].plot(figsize=(12,8),grid=True)
        self.df[['cumulative_returns', 'position']].plot(figsize=(12,8),grid=True,secondary_y = 'position')

# =============================================================================
# Run below code to call above Class
# =============================================================================
end1 = dt.date.today()
start1 = end1 - pd.Timedelta(days=3*252)

nifty_MACD_signal = backtesting_MACD_crossover('^NSEI', start1, end1)




