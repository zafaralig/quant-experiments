"""
Problem Statement :
You have 17 coins and I have 16 coins, we flip all coins at the same time. 
If you have more heads then you win, if we have the same number of heads or if you have less then I win. 
What's your probability of winning?

@author: zafar.ahmed
"""
import time
import numpy as np
import pandas as pd

start_time = time.time()
df = pd.DataFrame()

df_17= pd.DataFrame(np.random.randint(2,size=(17,1000000)))
df_16 = pd.DataFrame(np.random.randint(2,size=(16,1000000)))

df["No_of_heads_17"] = df_17.sum()
df["No_of_heads_16"] = df_16.sum()

    
df['17_win'] = np.where(df["No_of_heads_17"]>df["No_of_heads_16"],'win','losse')

losse, win = df['17_win'].value_counts().sort_index(ascending=True)

prob_win = 100*(win/(win+losse))

print(f'Probability of winning : {round(prob_win,2)}%\n')

print('It is expected to have 50% probability of winning.\
      \nEverything is same upto 16th coin i.e. winning or loosing completely depends on the last coin (17th) only\n')

end_time = time.time()
Simulation_time = end_time-start_time
print(f'Time taken in the simulation is: {round(Simulation_time,2)} sec')
