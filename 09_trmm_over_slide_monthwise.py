# %% [markdown]
# # About
# This code extracts TRMM data over the rishiganga slide area. The data is grouped monthwise.




# %% [markdown]
# # Libs
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
# # Read files
rasters = sorted(glob.glob("../../003_Dataset/3_RSData/1_Rasters/5_TRMM/with_time_dim/*.nc"))
ds = xr.open_mfdataset(rasters)




# %% [markdown]
# # Clip values to shapefile region
cutLine = gpd.read_file("../../004_RishiGanga/02_RS_data/02_Vector/03_Rishiganga_slide/Rishiganga_slide_WGS84_centroid.shp")  # shape file of slide area
da = ds.precipitation.sel(nlon=cutLine.X.values, nlat=cutLine.Y.values, method='nearest')




# %% [markdown]
# # Group by months
# Help taken from this answer: https://stackoverflow.com/a/60793478/13422705
dc = {}
monthGroups = da.groupby('time.month').groups
for i in td(range(1,13), desc='Grouping monthwise'):
    dc[i] = da.isel(time=monthGroups[i])




# %% [markdown]
# # Get stats
daAnnual = da.resample(time='AS').sum()  # only required for the index of dataframe
df = pd.DataFrame(index=daAnnual.time.values, columns=['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'])
for i in td(range(1,13), desc='Getting values'):
    for j in range(len(df)):
        df.iloc[j,i-1] = dc[i].isel(time=j).mean().values



# %% [markdown]
## Save to csv
df = df*24*30
df.to_csv("../../004_RishiGanga/05_CSVs/09_trmm_over_slide_monthly_grouped.csv")
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
