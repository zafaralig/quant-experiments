# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:05:04 2022

@author: Zafar.Ahmed
"""

import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('ignore')
ema = 12
end1 = datetime.date.today()
start1 = end1 - pd.Timedelta(days=50)

df_orignal = yf.download('^NSEI', start=start1, end = end1, interval='5m')

df = df_orignal.copy()

df.drop(columns=['High', 'Low','Volume'],inplace=True)
df['cc_returns'] = df['Close'].pct_change()

df['ema'] = df['Close'].ewm(span=ema, adjust=False).mean()

df['position'] = np.where((df['ema']<df['Close']),1,0)
df['position'] = df['position'].shift(1)

# df['position'].value_counts()

df['strategy_returns'] = df['cc_returns']*df['position']

df['strategy_returns'] = df['strategy_returns'] + 1 
df['cc_returns'] = df['cc_returns'] + 1


df[['cc_returns', 'strategy_returns']].cumprod().plot(grid=True,linewidth=1,figsize=(14,9))

print('Buy and Hold returns: ', np.round((df['cc_returns'].cumprod()[-1] - 1)*100,3),' %')
print('Strategy returns: ', np.round((df['strategy_returns'].cumprod()[-1] - 1)*100,3),' %')






