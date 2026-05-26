"""
Monte-Carlo based simulation to analyse the portfolio evolution after certain period of time
CoVariance of each stock in the portfolio is calculate 
With the help of CoVariance, Corelated noise/returns is generated
Random weight is also assigned to each stock in the portfolio (this can be changed to specific value)
weight is the fraction of investemt to each stock in the portfolio


@author: zafar.ahmed
"""
import pandas as pd
import numpy as np
import datetime as dt
from time import time
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

sim_start = time()

def get_data(ticket,start_date,end_date):
    
    stock_data = pdr.get_data_yahoo(ticket,start_date,end_date)
    stock_data = stock_data['Close']
    returns = stock_data.pct_change()
    meanReturn = returns.mean()
    covMatrix = returns.cov()
    return meanReturn, covMatrix, stock_data

stockList = ['CAMS', 'DMART', 'IRCTC', 'PIIND', 'POLYCAB', 'SUBEXLTD']
stocks = [stock + '.NS' for stock in stockList]

endDate = dt.datetime.today()
startDate = endDate - dt.timedelta(days=260*2.0)

meanReturns, covMatrix, stock_data = get_data(stocks, startDate, endDate)

weights = np.random.random(len(meanReturns))
weights /= np.sum(weights)


# Monte Carlo Method
mc_sims = 10000 # number of simulations
T = 260*1 #timeframe in days

meanM = np.full(shape=(T, len(weights)), fill_value=meanReturns)
meanM = meanM.T

portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)

initialPortfolio = 100

for m in range(0, mc_sims):
    Z = np.random.normal(size=(T, len(weights)))#uncorrelated RV's
    L = np.linalg.cholesky(covMatrix) #Cholesky decomposition to Lower Triangular Matrix
    dailyReturns = meanM + np.inner(L,Z) #Correlated daily returns for individual stocks
    portfolio_sims[:,m] = np.cumprod(np.inner(weights, dailyReturns.T)+1)*initialPortfolio

plt.plot(portfolio_sims)
plt.ylabel('Percentage Portfolio')
plt.xlabel('Trading Days')
plt.title('Monte-Carlo simulation of a stock portfolio')
plt.show()

print(f'Maximum portfolio value can reach after {T} trading days : {np.round(portfolio_sims.max(),2)} with investment of {initialPortfolio}')
print(f'Minimum portfolio value can reach after {T} trading days : {np.round(portfolio_sims.min(),2)} with investment of {initialPortfolio}')
sim_end = time()

simulation_time =  sim_end - sim_start
print(f'Simulation time: {np.round(simulation_time,3)} sec')



