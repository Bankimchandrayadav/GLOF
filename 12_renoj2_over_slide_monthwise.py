# %% [markdown]
# # About
# This code extracts RENOJ2 data over the rishiganga slide area. The data is grouped monthwise.




# %% [markdown]
# # Libs
from operator import index
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
## Read and clip file
ds = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/02_Product2/prod2.nc") 
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/03_Rishiganga_slide/Rishiganga_slide_UTM44N.shp")  # shapefile of slide area
dsClip = ds.rio.clip(cutLine.geometry.apply(mapping), cutLine.crs, drop=False)  # clipped




# %% [markdown]
## Get stats 
df = pd.DataFrame(index=dsClip.time.values, columns=['Slide'])
for i in td(range(len(df)), desc='Daily stats'):
    df.Slide[i] = dsClip.prcp_renoj.isel(time=i).mean().round(4).values




# %% [markdown]
# # Group by months
# Prefer this method i.e. operations on a dataframe rather than that on xarray dataset
# [1] Group data
dc = {}  
dfMon = df.resample('MS').sum()
for i in td(range(1,13), desc='Grouping monthly'):
    dc[i] = dfMon[dfMon.index.month==i]  # grouped monthly
    dc[i].index = dc[i].index.year  # index renamed

# [2] Concatenate the grouped data
df = pd.concat([dc[1], dc[2], dc[3], dc[4], dc[5], dc[6], dc[7], dc[8], dc[9], dc[10], dc[11], dc[12]], axis=1)  
df.columns = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']  # all columns renamed 




# %% [markdown]
## Save to csv 
df.to_csv("../../004_RishiGanga/05_CSVs/12_renoj2_over_slide_monthly_grouped.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
