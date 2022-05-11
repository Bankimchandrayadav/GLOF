# %% [markdown]
# # About
# This notebook extracts CHIRPS data over the rishiganga slide area




# %% [markdown]
# Libs 
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
## Read and clip data to shapefile's extent
# [1] Read data
ds = xr.open_dataset("../../003_Dataset/3_RSData/1_Rasters/8_CHIRPS/chirps-v2.0.monthly.nc")  
ds = ds.sel(time=slice('2000-01-01', '2020-09-01'), longitude=slice(75,85), latitude=slice(25,35))
ds.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)
ds.rio.write_crs("epsg:4326", inplace=True)

# [2] Clip the data
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/03_Rishiganga_slide/Rishiganga_slide_WGS84.shp")  # shape file of slide area
dsClip = ds.rio.clip(cutLine.geometry.apply(mapping), cutLine.crs, drop=True)  # clipped 




# %% [markdown]
## Get stats 
# [1] Define dataframe 
df = pd.DataFrame(index=dsClip.time.values) # define dataframe
df['Slide'] = ""

# [2] Get stats 
for i in td(range(len(dsClip.time)), desc='Getting stats'):
    dsClip.precip.isel(time=0).mean().round(2).values
    df.Slide[i] = dsClip.precip.isel(time=i).mean().round(3).values




# %% [markdown]
## Save to csv 
df.to_csv("../../004_RishiGanga/05_CSVs/07_chirps_over_slide.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
