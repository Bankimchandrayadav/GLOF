# %% [markdown]
# # About
# This code extracts GPM data over the rishiganga slide area




# %% [markdown]
# # Libs
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping




# %% [markdown]
# # Read data
# (takes time)
start = time.time()
rasters = sorted(glob.glob("../../003_Dataset/3_RSData/1_Rasters/1_GPM/daily/*.nc4"))
ds = xr.open_mfdataset(rasters)
da = ds.precipitationCal.sel(lon=slice(79,80), lat=slice(30,31))
print('Time elapsed in reading data: ', np.round((time.time()-start)/60, 2), 'mins')




# %% [markdown]
# # Clip data
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/03_Rishiganga_slide/Rishiganga_slide_WGS84_centroid.shp")  # shape file of slide area
da = da.sel(lon=cutLine.X.values, lat=cutLine.Y.values, method='nearest')
da = da.resample(time='MS').sum()




# %% [markdown]
# # Get stats
df = pd.DataFrame(index=da.time.values) # define dataframe
df['Slide'] = ""
for i in td(range(len(da.time)), desc='Getting stats'):  # get stats into df
    da.isel(time=0).mean().round(2).values
    df.Slide[i] = da.isel(time=i).mean().round(3).values




# %% [markdown]
# # Save to csv
df.to_csv("../../004_RishiGanga/05_CSVs/10_gpm_over_slide.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')



