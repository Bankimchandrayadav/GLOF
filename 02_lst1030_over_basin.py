# %% [markdown]
# # About
# This code reports the LST time series over the basin area




# %% [markdown]
# Libs 
import xarray as xr, pandas as pd, numpy as np, time 
from tqdm.notebook import tqdm as td 
start = time.time()




# %% [markdown]
## Read files and set props
# [1] Read
ds1 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/02_Basin/MOD11A1.006_1km_aid0001 (3).nc")
ds2 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/02_Basin/MOD11A1.006_1km_aid0001 (4).nc")
ds = xr.concat([ds1,ds2], dim='time')  # concatened all datasets

# [2] Change julian time to datetime
datetimeindex = ds.indexes['time'].to_datetimeindex()  
ds['time'] = datetimeindex

# [3] Change kelvin to celsius
ds['LST_Day_1km'] = ds['LST_Day_1km'] - 273.15




# %% [markdown]
## Refine the LST data
# int to binary taken from: https://stackoverflow.com/a/16926357
for k in td(range(len(ds.time)), desc='Refining LST'):
    for i in range(3):
        for j in range(5):
            qc = ds.QC_Day.isel(time=k).values[i,j]  # qc value at loc (i,j) 
            if not np.isnan(qc):  # only when qc is not nan
                qc = int(qc)  # convert it to integer
                qc = '{:08b}'.format(qc)[6:]  # then convert it to 8 digit 'binary string'
                if not qc == '00':  # if first bit word of this string is not equal to '00' 
                    ds.LST_Day_1km.isel(time=k).values[i,j] = np.nan  # change LST to nan




# %% [markdown]
## Get stats 
# [1] Prepare a dataframe
df = pd.DataFrame(index=ds.time.values, columns=['RishiGangaBasin'])

# [2] Get the LST time series into the dataframe
for i in td(range(len(df)), desc='Getting values'):
    df.RishiGangaBasin[i] = np.round((np.float32(ds.LST_Day_1km.isel(time=i).mean().values)),2)




# %% [markdown]
## Save to csv 
df.to_csv("../../004_RishiGanga/05_CSVs/02_lst_over_basin.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
