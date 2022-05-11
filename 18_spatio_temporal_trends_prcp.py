#%% [markdown]
## About 
# This code reports the spatio temporal trend of modelled precipitation over the UKD region 




# %% [markdown]
## Libs
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time, matplotlib.pyplot as plt, gdal      
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
start = time.time()




# %% [markdown]
## Read and preprocess data
def readData():

    # [1] Read data 
    ds = xr.open_dataset("../02_RS_data/01_Raster/02_Modelled_Precp/prod1.nc") 

    # [2] Resample to annual scale 
    dsAnnual = ds.resample(time='AS').sum()  
    dsAnnual = dsAnnual.squeeze()  # extra dims removed

    # [3] Resample to monthly scale 
    dsMonthly  = ds.resample(time='MS').sum()
    dsMonthly = dsMonthly.squeeze()

    # [4] Resample to DJF frequency
    dsQuartely = dsMonthly.resample(time = 'QS-Dec').mean()
    dsDJF = dsQuartely.where(dsQuartely['time.month'] ==12, drop=True) 

    # [5] Resample to JJA frequency 
    dsQuartely1 = dsMonthly.resample(time = 'QS-Jun').mean()
    dsJJA = dsQuartely1.where(dsQuartely1['time.month'] ==6, drop=True) 

    # [*] selecting by particular months
    # dsMonthly.where((dsMonthly['time.month'] == 12) | (dsMonthly['time.month'] == 1) | (dsMonthly['time.month'] == 2), drop=True)
    
    return dsAnnual, dsMonthly, dsDJF, dsJJA 
dsAnnual, dsMonthly, dsDJF, dsJJA = readData()




# %% [markdown]
## Find trend - annual
# Help from: http://atedstone.github.io/rate-of-change-maps/
def trendAnnual():

    # [1] Get the values
    vals = dsAnnual.prcp_renoj.values 
    years = np.arange(start=1972, stop=2019)

    # [2] Reshape to an array with as many rows as years and as many columns as pixels
    vals2 = vals.reshape(len(years), -1)

    # [3] Do a first-degree polyfit
    regressions = np.polyfit(years, vals2, 1)

    # [4] Get the coefficients 
    trends = regressions[0,:].reshape(vals.shape[1], vals.shape[2])
    goodness = regressions[1,:].reshape(vals.shape[1], vals.shape[2])

    return trends, goodness
trends, goodness = trendAnnual()




# %% [markdown]
## Convert to tiff 
def trendAnnual_toTiff():
    inRas = gdal.Open("../../003_Dataset/3_RSData/1_Rasters/GeneratedRasters/01_Daily/06_1972_2018_GPM_APHRO/1972-01-01.tif")
    ## Create the raster
    driver = gdal.GetDriverByName("GTiff")  ## driver to create the raster 
    newRas = driver.Create("../02_RS_data/01_Raster/03_Trends/01_Prcp/01_Annual.tif", xsize=inRas.RasterXSize, ysize=inRas.RasterYSize, bands=1, eType=gdal.GDT_Float32)
    newRas.SetGeoTransform(inRas.GetGeoTransform())
    newRas.SetProjection(inRas.GetProjection())
    newRas.GetRasterBand(1).WriteArray(trends)
    newRas = None
trendAnnual_toTiff()




# %% [markdown]
## Find trend - seasonal (DJF)
def trendDJF():

    # [1] Get the values
    vals = dsDJF.prcp_renoj.values 
    years = np.arange(start=1971, stop=2018)

    # [2] Reshape to an array with as many rows as years and as many columns as pixels
    vals2 = vals.reshape(len(years), -1)

    # [3] Do a first-degree polyfit
    regressions = np.polyfit(years, vals2, 1)

    # [4] Get the coefficients 
    trends = regressions[0,:].reshape(vals.shape[1], vals.shape[2])
    goodness = regressions[1,:].reshape(vals.shape[1], vals.shape[2])

    return trends, goodness
trends1, goodness1 = trendDJF()




# %% [markdown]
## Convert to tiff (DJF)
def trendDJF_toTiff():
    inRas = gdal.Open("../../003_Dataset/3_RSData/1_Rasters/GeneratedRasters/01_Daily/06_1972_2018_GPM_APHRO/1972-01-01.tif")
    ## Create the raster
    driver = gdal.GetDriverByName("GTiff")  ## driver to create the raster 
    newRas = driver.Create("../02_RS_data/01_Raster/03_Trends/01_Prcp/02_DJF.tif", xsize=inRas.RasterXSize, ysize=inRas.RasterYSize, bands=1, eType=gdal.GDT_Float32)
    newRas.SetGeoTransform(inRas.GetGeoTransform())
    newRas.SetProjection(inRas.GetProjection())
    newRas.GetRasterBand(1).WriteArray(trends1)
    newRas = None
trendDJF_toTiff()




# %% [markdown]
## Find trend - seasonal (JJA)
def trendJJA():

    # [1] Get the values
    vals = dsJJA.prcp_renoj.values 
    years = np.arange(start=1972, stop=2018)

    # [2] Reshape to an array with as many rows as years and as many columns as pixels
    vals2 = vals.reshape(len(years), -1)

    # [3] Do a first-degree polyfit
    regressions = np.polyfit(years, vals2, 1)

    # [4] Get the coefficients 
    trends = regressions[0,:].reshape(vals.shape[1], vals.shape[2])
    goodness = regressions[1,:].reshape(vals.shape[1], vals.shape[2])

    return trends, goodness
trends2, goodness2 = trendJJA()




# %% [markdown]
## Convert to tiff (JJA)
def trendJJA_toTiff():
    inRas = gdal.Open("../../003_Dataset/3_RSData/1_Rasters/GeneratedRasters/01_Daily/06_1972_2018_GPM_APHRO/1972-01-01.tif")
    ## Create the raster
    driver = gdal.GetDriverByName("GTiff")  ## driver to create the raster 
    newRas = driver.Create("../02_RS_data/01_Raster/03_Trends/01_Prcp/03_JJA.tif", xsize=inRas.RasterXSize, ysize=inRas.RasterYSize, bands=1, eType=gdal.GDT_Float32)
    newRas.SetGeoTransform(inRas.GetGeoTransform())
    newRas.SetProjection(inRas.GetProjection())
    newRas.GetRasterBand(1).WriteArray(trends2)
    newRas = None
trendJJA_toTiff()




# %%
