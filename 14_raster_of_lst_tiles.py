# %% [markdown]
# # About
# This code prepares the raster c/t the MODIS LST tiles over the slide region 




# %% [markdown]
# %% [markdown]
## Libs 
import xarray as xr, pandas as pd, numpy as np, time, rioxarray as rx 
from tqdm.notebook import tqdm as td 
start = time.time()




# %% [markdown]
## Read file 
ds = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/MOD11A1.006_1km_aid0001.nc")
datetimeindex = ds.indexes['time'].to_datetimeindex()  
ds['time'] = datetimeindex



# %% [markdown]
## Testing 
ds.rio.crs
ds.rio.write_crs("epsg:4326", inplace=True)
ds.QC_Day.isel(time=10).rio.to_raster("../../004_RishiGanga/02_RS_data/02_Vector/05_LST_shapefile/01_LST_raster.tif")




# %%
