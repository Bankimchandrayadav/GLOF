# %% [markdown]
# # About
# This notebook extracts product 2 data over the slide area of the rishiganga basin area




# %% [markdown]
## Libs 
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
## Read and clip data to the shapefile's extent 
# Clipping taken from snowman's answer: https://gis.stackexchange.com/a/354798    
# (Here x_dim, y_dim and crs were already set in the ds read, and hence not repeated here)
ds = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/02_Product2/RENOJ2.nc")  
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/02_Rishiganga_basin/basin.shp")  
dsClip = ds.rio.clip(cutLine.geometry.apply(mapping), cutLine.crs, drop=False)  # clipped 




# %% [markdown]
## Get stats 
# [1] Prepare dataframe 
df = pd.DataFrame(index=dsClip.time.values) # define dataframe
df['Basin'] = ""

# [2] Getting stats into dataframe 
for i in td(range(len(dsClip.time)), desc='Getting stats'):
    dsClip.prcp_renoj.isel(time=0).mean().round(2).values
    df.Basin[i] = dsClip.prcp_renoj.isel(time=i).mean().round(3).values




# %% [markdown]
## Save to csv 
df.to_csv("../../004_RishiGanga/05_CSVs/05_renoj2_over_basin.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
