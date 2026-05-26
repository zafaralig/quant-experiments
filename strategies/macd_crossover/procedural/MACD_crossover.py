# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 22:15:11 2022

@author: Zafar.Ahmed
"""
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('ignore')

ticket1 = 'FB'
end1 = datetime.date.today()
start1 = end1 - pd.Timedelta(days=365*7)

df = yf.download(ticket1, start1, end1)

df['ema26'] = df['Close'].ewm(span=26,adjust=False).mean()
df['ema12'] = df['Close'].ewm(span=12,adjust=False).mean()

df['MACD'] = df['ema12'] - df['ema26']

df['signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

df[['signal','MACD', 'Close']].plot(figsize=(12,8),grid=True,secondary_y = 'Close')

df['position'] = np.where(df['MACD']>df['signal'],1,-1)

df['position'] = df['position'].shift(1)

df['cc_returns'] = df['Close'].pct_change()
df['strategy_returns'] = df['cc_returns'] * df['position']

df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod() - 1

df[['cumulative_returns']].plot(figsize=(12,8),grid=True)

df[['cumulative_returns', 'position']].plot(figsize=(12,8),grid=True,secondary_y = 'position')



























