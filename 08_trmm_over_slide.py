# %% [markdown]
# # About
# This notebook extracts TRMM data over the rishiganga slide area




# %% [markdown]
# # Libs
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
# # Read data
rasters = sorted(glob.glob("../../003_Dataset/3_RSData/1_Rasters/5_TRMM/with_time_dim/*.nc"))
ds = xr.open_mfdataset(rasters)




# %% [markdown]
# # Clip values
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/03_Rishiganga_slide/Rishiganga_slide_WGS84_centroid.shp")  # shape file of slide area
da = ds.precipitation.sel(nlon=cutLine.X.values, nlat=cutLine.Y.values, method='nearest')




# %% [markdown]
# # Get stats
df = pd.DataFrame(index=da.time.values) # define dataframe
df['Slide'] = ""
for i in td(range(len(da.time)), desc='Getting stats'):
    da.isel(time=0).mean().round(2).values
    df.Slide[i] = da.isel(time=i).mean().round(3).values




# %% [markdown]
# # Save to csv
df = df*24*30
df.to_csv("../../004_RishiGanga/05_CSVs/08_trmm_over_slide.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
