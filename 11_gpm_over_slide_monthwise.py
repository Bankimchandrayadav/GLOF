# %% [markdown]
# # About
# This notebook extracts GPM data over the rishiganga slide area. The data is grouped monthwise.




# %% [markdown]
# # Libs 
import pandas as pd, time, numpy as np
from tqdm.notebook import tqdm as td 
start = time.time()




# %% [markdown]
# # Read GPM data
dfIn = pd.read_csv("../../004_RishiGanga/05_CSVs/10_gpm_over_slide.csv")
dfIn.set_index('Unnamed: 0', inplace=True)
dfIn.index.names=[None] 
dfIn.index = pd.to_datetime(dfIn.index)




# %% [markdown]
# # Group by months
# Prefer this method (i.e. date operations on a dataframe) rather than grouping on xarray dataset
# [1] Group data
dc = {}  # dict to store the monthly grouped values
for i in td(range(1,13), desc='Grouping monthly'):
    dc[i] = dfIn[dfIn.index.month==i]
    dc[i].index = dc[i].index.year  # grouped monthly

# [2] Concatenate the grouped data
df = pd.concat([dc[1], dc[2], dc[3], dc[4], dc[5], dc[6], dc[7], dc[8], dc[9], dc[10], dc[11], dc[12]], axis=1)  
df.columns = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']  # all columns renamed 




# %% [markdown]
# # Save to csv
df.to_csv("../../004_RishiGanga/05_CSVs/11_gpm_over_slide_monthly_grouped.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
