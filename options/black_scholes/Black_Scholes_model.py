from scipy.stats import norm
import numpy as np


# defining the function to calculate the call/put price by Black-Scholes model
def black_scholes(interest_rate,stock_price,strike_price,time,volatility, type="Call"):
    d1 = (np.log(stock_price/strike_price) + (interest_rate + (volatility**2)/2)*time)/\
         (volatility*np.sqrt(time))
    d2 = d1 - volatility*np.sqrt(time)
    if type == "Call":
        price = stock_price * norm.cdf(d1, 0, 1) - strike_price * np.exp(-interest_rate*time)*norm.cdf(d2, 0, 1)
    elif type == "Put":
        price = - stock_price * norm.cdf(-d1, 0, 1) + strike_price * np.exp(-interest_rate * time) * norm.cdf(-d2, 0, 1)
    return price




# interest_rate = 0.07
# stock_price = 30
# strike_price = 40
# time = 240/365
# volatility = 0.3

# call_price = black_scholes(interest_rate,stock_price,strike_price,time,volatility, type="Call")
# put_price = black_scholes(interest_rate,stock_price,strike_price,time,volatility, type="Put")

# print(f'Call price : {np.round(call_price,2)}')
# print(f'Put price : {np.round(put_price,2)}')
