"""
@author: zafar.ahmed
"""

import requests
import pandas as pd
import numpy as np

IEX_CLOUD_API_TOKEN = "API_TOKEN" # api token to get data from brokers

snp_500_list = pd.read_csv('SnP_constituents.csv')
my_col = ['Symbol', 'Price', 'Market_Cap', '#_Shares_to_Buy']


# =============================================================================
# single API call per loop
# =============================================================================

# final_data = pd.DataFrame(columns=my_col)
# for symbol in snp_500_list['Symbol'].iloc[:5]:
#     api_url = f"https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}"
#     data = requests.get(api_url).json()
#     price = data['latestPrice']
#     market_cap = data['marketCap']
#     entry_data = pd.DataFrame([symbol,price,market_cap,np.nan],index=(my_col))
#     final_data = pd.concat([final_data, entry_data.T])
#     print(f'Data downloded for {symbol}')
  
  
# =============================================================================
# for batch API call
# =============================================================================

def chunks(lst,n):
    for i in range(0,len(lst),n):
        yield lst[i:i+n]

per_batch_call = 100        
symbol_groups = list(chunks(snp_500_list['Symbol'], per_batch_call))

symbol_strings = []
for i in range(len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

final_data = pd.DataFrame(columns=my_col)


for symbol_string in symbol_strings:
    batch_api_url = f"https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}"
    data = requests.get(batch_api_url).json()

    for symbol in symbol_string.split(','):
        price = data[symbol]['quote']['latestPrice']
        market_cap = data[symbol]['quote']['marketCap']
        entry_data = pd.DataFrame([symbol,price,market_cap,np.nan],index=(my_col))
        final_data = pd.concat([final_data, entry_data.T],ignore_index=True)
        # print(f'Data downloded for {symbol}')


# =============================================================================
# calculating the number of shares with equal weight
# =============================================================================
portfolio_size = input('Enter the value of your portfolio:')

try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number! \nPlease try again:")
    portfolio_size = input('Enter the value of your portfolio:')
    val = float(portfolio_size)

position_size = val/len(final_data.index)

final_data['#_Shares_to_Buy'] = (position_size/final_data['Price']).apply(np.floor)

final_data.insert(0,'Company',snp_500_list['Company'])
final_data.to_csv('equally_weighted_snp500.csv',index=False)
