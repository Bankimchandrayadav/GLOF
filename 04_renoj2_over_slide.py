# %% [markdown]
# # About
# This notebook extracts product 2 data over the slide area of the rishiganga slide area




# %% [markdown]
## Libs 
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
## Read and clip data to shapefile's extent
# Clipping taken from snowman's answer: https://gis.stackexchange.com/a/354798 (here x_dim, y_dim and crs were already set in the ds, hence not repeated here)
ds = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/02_Product2/prod2.nc")  
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/03_Rishiganga_slide/Rishiganga_slide_UTM44N.shp")  
dsClip = ds.rio.clip(cutLine.geometry.apply(mapping), cutLine.crs, drop=False)  # clipped




# %% [markdown]
## Get stats 
# [1] Define dataframe
df = pd.DataFrame(index=dsClip.time.values) # define dataframe
df['Slide'] = ""

# [2] Get the values into dataframe
for i in td(range(len(dsClip.time)), desc='Getting stats'):
    dsClip.prcp_renoj.isel(time=i).mean().round(3).values
    df.Slide[i] = dsClip.prcp_renoj.isel(time=i).mean().round(3).values




# %% [markdown]
## Save to csv 
df = df.astype('float32')
df.to_csv("../../004_RishiGanga/05_CSVs/04_renoj2_over_slide.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
