# %% [markdown]
# # About
# This code reports no. of non-nan values per month in the csv file containing daily lst information over the slide region




# %% [markdown]
## Libs 
import pandas as pd, time, matplotlib.pyplot as plt, numpy as np 
from tqdm.notebook import tqdm as td 
start = time.time()




# %% [markdown]
## Read the lst csv fle
# [1] Read
df = pd.read_csv("../../004_RishiGanga/05_CSVs/01_lst_over_slide.csv")

# [2] Set index
df.set_index('Unnamed: 0', inplace=True)
df.index.names = [None]
df.index = pd.to_datetime(df.index)




# %% [markdown]
## Get the report 
# [1] Prepare a dataframe to store the report 
df1 = pd.DataFrame(index=pd.date_range('2000-01-01', '2021-12-31', freq='MS'), columns=['Count'])

# [2] Get the count of non-nan lst days per month
for i in td(range(2000, 2022), desc='Getting count'):
    for j in range(1,13):

        # [2.1] index of df1 at particular year and month grabbed
        idx = df1[(df1.index.year==i) & (df1.index.month==j)].index.values

        # [2.2] the count of non-nan lst days in that year and month stored at df1's index
        df1.loc[idx] = df[(df.index.year==i) & (df.index.month==j)].count().values

# [3] Remove extra rows 
df1 = df1.drop(pd.to_datetime('2000-01-01'), errors='ignore')  # starting ones 
df1 = df1.drop(pd.date_range('2021-01-01', '2021-12-01'), errors='ignore')  # end ones 




# %% [markdown]
## Save to csv 
df1.to_csv("../../004_RishiGanga/05_CSVs/15_day_count_in_csv_01.csv")





# %% [markdown]
## Generate a graph [optional]
plt.rcParams["figure.dpi"] = 300
df1.plot(xlabel='Years', ylabel='No. of values considered per month', title='Value Counts per month in LST Report', legend=0, color='k', alpha=0.9)
plt.tight_layout()
plt.savefig("../../004_RishiGanga/04_Images/02_MS_Images/02_day_count.png", bbox_inches='tight', facecolor='w')
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
