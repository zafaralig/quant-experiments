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

class backtesting_sma_crossover:
    
    def __init__(self, ticker, start_date, end_date , ma_short, ma_long):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.ma_short = ma_short
        self.ma_long = ma_long
        
        self.fetch_data()
        self.indicators()
        self.signals()
        self.positions()
        self.returns()
        
        
    def fetch_data(self):
        self.df = yf.download(self.ticker, self.start_date, self.end_date)
        
    def indicators(self):
        self.df['ma_short'] = self.df['Adj Close'].rolling(window= self.ma_short, center=False).mean()
        self.df['ma_long'] = self.df['Adj Close'].rolling(window= self.ma_long, center=False).mean()
        self.df['ma_short_prev'] = self.df['ma_short'].shift()
        self.df['ma_long_prev'] = self.df['ma_long'].shift()
        self.df.dropna(inplace=True)
   
    def signals(self):
        self.df['signal'] = np.where((self.df['ma_short'] > self.df['ma_long']) 
                            & (self.df['ma_short_prev'] < self.df['ma_long_prev']), 1, 0)
        
        self.df['signal'] = np.where((self.df['ma_short'] < self.df['ma_long']) 
                            & (self.df['ma_short_prev'] > self.df['ma_long_prev']), -1, self.df['signal'])
    
    def positions(self):
        self.df['position'] = self.df['signal'].replace(to_replace=0, method='ffill')
        
    def returns(self):
        self.df['bnh_returns'] = np.log(self.df['Adj Close'] / self.df['Adj Close'].shift(1))
        self.df['strategy_returns'] = self.df['bnh_returns'] * self.df['position'].shift(1)
        return self.df['strategy_returns'].cumsum()[-1]
       
    def analysis(self):
        # A plot to check if the strategy is working as planned:
        self.df[['ma_short','ma_long', 'position']].plot(figsize=(15, 6), secondary_y='position', grid=True)
        plt.title('checking if positions are generated properly')
        plt.show()

        # A plot to check how the strategy strategy performs relative to buy & hold
        self.df[['bnh_returns','strategy_returns']].cumsum().plot(figsize=(15, 6), secondary_y='position', grid=True)
        plt.title("Buy & hold' vs 'crossover strategy' cumulative returns")
        plt.show()

        #analytics
        #run this in HTML supported IDE like Jupyter
        pf.create_returns_tear_sheet(self.df['strategy_returns'])

class backtesting_ema_crossover(backtesting_sma_crossover):
    def indicators(self):
        self.df['ma_short'] = self.df['Adj Close'].ewm(span=self.ma_short, adjust=False).mean()
        self.df['ma_long'] = self.df['Adj Close'].ewm(span=self.ma_long, adjust=False).mean()
        self.df['ma_short_prev'] = self.df['ma_short'].shift()
        self.df['ma_long_prev'] = self.df['ma_long'].shift()
        self.df.dropna(inplace=True)

        
# =============================================================================
# Run below code to call above Class
# =============================================================================
end1 = dt.date.today()
start1 = end1 - pd.Timedelta(days=3*252)

nifty_10_20_sma = backtesting_sma_crossover('^NSEI', start1, end1, 10, 20)
nifty_10_20_ema = backtesting_ema_crossover('^NSEI', start1, end1, 10, 20)


print('Total return SMA:',np.round(nifty_10_20_sma.df['strategy_returns'].cumsum()[-1] *100,3), '%' )
print('Total return EMA:',np.round(nifty_10_20_ema.df['strategy_returns'].cumsum()[-1] *100,3), '%' )

# data = nifty_10_20_sma.df['strategy_returns']
# nifty_10_20_sma.analysis()
# nifty_10_20_ema.analysis()




















