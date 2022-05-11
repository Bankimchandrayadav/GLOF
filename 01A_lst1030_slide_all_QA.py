# %% [markdown]
# # About
# This code reports the LST time series over the slide area in all the four categories of QA see [https://www.youtube.com/watch?v=JPjkjjhj5rk] 




# %% [markdown]
## Libs 
import xarray as xr, pandas as pd, numpy as np, time 
from tqdm.notebook import tqdm as td 
start = time.time()




# %% [markdown]
## Read files and set props
# [1] Read
dsT1 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/MOD11A1.006_1km_aid0001.nc")
dsT2 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/MOD11A1.006_1km_aid0001 (1).nc")
dsT3 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/MOD11A1.006_1km_aid0001 (2).nc")
ds = xr.concat([dsT1,dsT2,dsT3], dim='time')  # all datasets concatenated

# [2] Change julian time to datetime
datetimeindex = ds.indexes['time'].to_datetimeindex()  
ds['time'] = datetimeindex

# [3] Change kelvin to celsius
ds['LST_Day_1km'] = ds['LST_Day_1km'] - 273.15  

# [4] Make 4 copies 
ds1=ds.copy(deep=True)
ds2=ds.copy(deep=True)
ds3=ds.copy(deep=True)
ds4=ds.copy(deep=True)




# %% [markdown]
## LST of error<=1K
for k in td(range(len(ds.time)), desc='LST of error<=1K'):
    for i in range(3):
        for j in range(5):
            qc = ds1.QC_Day.isel(time=k).values[i,j]  # qc value at loc (i,j) 
            if np.isnan(qc):  # qc==nan values ignored
                pass
            else:
                qc = int(qc)  # qc float to integer
                qc = '{:08b}'.format(qc)[:2]  # int to 'binary string'
                if not qc == '00':   

                    # [1] if above condition==False then convert to nan
                    ds1.LST_Day_1km.isel(time=k).values[i,j] = np.nan  




# %% [markdown]
## Get stats 
# [1] Prepare a dataframe
df1 = pd.DataFrame(index=ds1.time.values, columns=['SlideRegion'])

# [2] Get the LST time series into the dataframe
for i in td(range(len(ds.time)), desc='Getting values into dataframe'):
    df1.SlideRegion[i] = np.round((np.float32(ds1.LST_Day_1km.isel(time=i).mean().values)),2)

# [3] Save as csv
df1.to_csv("../../004_RishiGanga/05_CSVs/01A_lst_over_slide_quality=1.csv")




# %% [markdown]
# ---
## LST of error<=2K
for k in td(range(len(ds.time)), desc='LST of error<=2K'):
    for i in range(3):
        for j in range(5):
            qc = ds2.QC_Day.isel(time=k).values[i,j]  
            if np.isnan(qc):  
                pass
            else:
                qc = int(qc)  
                qc = '{:08b}'.format(qc)[:2]  
                if not qc == '01':   
                    ds2.LST_Day_1km.isel(time=k).values[i,j] = np.nan  




# %% [markdown]
## Get stats 
df2 = pd.DataFrame(index=ds2.time.values, columns=['SlideRegion'])
for i in td(range(len(df2)), desc='Getting values into dataframe'):
    df2.SlideRegion[i] = np.round((np.float32(ds2.LST_Day_1km.isel(time=i).mean().values)),2)
df2.to_csv("../../004_RishiGanga/05_CSVs/01B_lst_over_slide_quality=2.csv")




# %% [markdown]
# ---
## LST of error<=3K
for k in td(range(len(ds.time)), desc='LST of error<=3K'):
    for i in range(3):
        for j in range(5):
            qc = ds2.QC_Day.isel(time=k).values[i,j]  
            if np.isnan(qc):  
                pass
            else:
                qc = int(qc)  
                qc = '{:08b}'.format(qc)[:2]  
                if not qc == '10':   
                    ds2.LST_Day_1km.isel(time=k).values[i,j] = np.nan  




# %% [markdown]
## Get stats 
df3 = pd.DataFrame(index=ds3.time.values, columns=['SlideRegion'])
for i in td(range(len(df3)), desc='Getting values into dataframe'):
    df3.SlideRegion[i] = np.round((np.float32(ds3.LST_Day_1km.isel(time=i).mean().values)),2)
df3.to_csv("../../004_RishiGanga/05_CSVs/01C_lst_over_slide_quality=3.csv")




# %% [markdown]
# ---
## LST of error>3K
for k in td(range(len(ds.time)), desc='LST of error>3K'):
    for i in range(3):
        for j in range(5):
            qc = ds2.QC_Day.isel(time=k).values[i,j]  
            if np.isnan(qc):  
                pass
            else:
                qc = int(qc)  
                qc = '{:08b}'.format(qc)[:2]  
                if not qc == '11':   
                    ds2.LST_Day_1km.isel(time=k).values[i,j] = np.nan  




# %% [markdown]
## Get stats 
df4 = pd.DataFrame(index=ds4.time.values, columns=['SlideRegion'])
for i in td(range(len(df4)), desc='Getting values into dataframe'):
    df4.SlideRegion[i] = np.round((np.float32(ds4.LST_Day_1km.isel(time=i).mean().values)),2)
df4.to_csv("../../004_RishiGanga/05_CSVs/01D_lst_over_slide_quality=4.csv")




# %%
