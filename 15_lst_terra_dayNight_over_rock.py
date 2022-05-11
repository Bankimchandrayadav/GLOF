# %% [markdown]
# # About
# This code reports the LST time series over a rock site in Ladakh in all the four categories of QA see [https://www.youtube.com/watch?v=JPjkjjhj5rk] 




# %% [markdown]
## Libs 
import xarray as xr, pandas as pd, numpy as np, time 
from tqdm.notebook import tqdm as td 
start = time.time()




# %% [markdown]
## Read files 
df1 = pd.read_csv("../../004_RishiGanga/05_CSVs/16_Rock-Terra-MOD11A1-006-results.csv")
df2 = pd.read_csv("../../004_RishiGanga/05_CSVs/17_Rock-Aqua-MYD11A1-006-results.csv")


# %% [markdown]
## List of cols to be chosen
cols1 = ['Latitude', 'Longitude', 'Date','MOD11A1_006_LST_Day_1km','MOD11A1_006_QC_Day_LST_Error_Flag_Description', 'MOD11A1_006_LST_Night_1km','MOD11A1_006_QC_Night_LST_Error_Flag_Description']
cols2 = ['Date', 'MYD11A1_006_LST_Day_1km', 'MYD11A1_006_QC_Day_LST_Error_Flag_Description', 'MYD11A1_006_LST_Night_1km','MYD11A1_006_QC_Night_LST_Error_Flag_Description']




# %% [markdown]
## Subset cols as per above list
df1 = df1[cols1]
df2 = df2[cols2]




# %% [markdown]
## Merge
# [1] Set dates as index in df1
df1.set_index('Date', inplace=True)
df1.index.names = [None]
df1.index = pd.to_datetime(df1.index)  # data type of date chanegd

# [2] Set dates as index in df2
df2.set_index('Date', inplace=True)
df2.index.names = [None]
df2.index = pd.to_datetime(df2.index)  

# [3] Merge 
df = pd.concat([df1, df2],axis=1)

# [4] Shorten the column names 
cols = ['Latitude', 'Longitude', 'Terra_Day', 'Terra_Day_Error','Terra_Night_Error','Terra_Night_Error', 'Aqua_Day', 'Aqua_Day_Error', 'Aqua_Night', 'Aqua_Night_Error']
df.columns = cols




# %% [markdown]
## Save to csv 
df.to_csv("../../004_RishiGanga/05_CSVs/18_Rock_Terra_Aqua.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
