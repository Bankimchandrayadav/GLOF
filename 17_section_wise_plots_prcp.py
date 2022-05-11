# %% [markdown] 
## About 
# This code reports the spatial distribution of product1 over various topoclimatic zones 




# %% [markdown]
## Libs 
from operator import pos
import xarray as xr, glob, rioxarray as rx, subprocess, gdal, pandas as pd, numpy as np, rasterio as rio, geopandas as gpd, pandas as pd, time     
from tqdm.notebook import tqdm as td 
from shapely.geometry import mapping
import matplotlib.pyplot as plt 
start = time.time()




# %% [markdown]
## Read and preprocess data
def readData():
    ## Read and clip data to shapefile's extent
    # [1] read dataset
    ds = xr.open_dataset("../02_RS_data/01_Raster/02_Modelled_Precp/prod1.nc")  

    # [2] read shapefiles
    cut1 = gpd.read_file("../02_RS_data/02_Vector/07_TopoclimaticZones/02_section_1.shp")
    cut2a = gpd.read_file("../02_RS_data/02_Vector/07_TopoclimaticZones/03_section_2a.shp")
    cut2b = gpd.read_file("../02_RS_data/02_Vector/07_TopoclimaticZones/04_section_2b.shp")
    cut3 = gpd.read_file("../02_RS_data/02_Vector/07_TopoclimaticZones/05_section_3.shp")

    # [3] clip c/t shapefiles
    ds1 = ds.rio.clip(cut1.geometry.apply(mapping), cut1.crs, drop=True)  
    ds2a = ds.rio.clip(cut2a.geometry.apply(mapping), cut2a.crs, drop=False)  
    ds2b = ds.rio.clip(cut2b.geometry.apply(mapping), cut2b.crs, drop=False)  
    ds3 = ds.rio.clip(cut3.geometry.apply(mapping), cut3.crs, drop=False)  

    return ds1, ds2a, ds2b, ds3
ds1, ds2a, ds2b, ds3 = readData()




# %% [markdown]
## Get Annual reports 
def annualReports():

    # [1] Resample to annual scale
    ds1_ann = ds1.resample(time='AS').sum()
    ds2a_ann = ds2a.resample(time='AS').sum()
    ds2b_ann = ds2b.resample(time='AS').sum()
    ds3_ann = ds3.resample(time='AS').sum()

    # [2] Replace zeros outside the aoi by nan
    ds1_ann = ds1_ann.where(ds1_ann.prcp_renoj!=0)  
    ds2a_ann = ds2a_ann.where(ds2a_ann.prcp_renoj!=0)  
    ds2b_ann = ds2b_ann.where(ds2b_ann.prcp_renoj!=0)  
    ds3_ann = ds3_ann.where(ds3_ann.prcp_renoj!=0)  

    # [3] Get the spatial means into dataframe
    # [3.1] Define dataframes
    df1 = pd.DataFrame(index=ds1_ann.time.values, columns=['Sec1'])
    df2a = pd.DataFrame(index=ds2a_ann.time.values, columns=['Sec2a'])
    df2b = pd.DataFrame(index=ds2b_ann.time.values, columns=['Sec2b'])
    df3 = pd.DataFrame(index=ds3_ann.time.values, columns=['Sec3'])
    
    # [3.2] Get values into dataframes
    for i in td(range(len(df1)), desc='Fetching mean values'):
        df1.Sec1[i] = ds1_ann.prcp_renoj.isel(time=i).mean().values
        df2a.Sec2a[i] = ds2a_ann.prcp_renoj.isel(time=i).mean().values
        df2b.Sec2b[i] = ds2b_ann.prcp_renoj.isel(time=i).mean().values
        df3.Sec3[i] = ds3_ann.prcp_renoj.isel(time=i).mean().values

    # [3.3] Concatenate the dataframes
    df = pd.concat([df1, df2a, df2b, df3], axis=1)
    df=df.astype(float)
    df = df.drop(df.index[-1])

    df.round(2).to_csv("../../004_RishiGanga/05_CSVs/20_Sectionwise_precp_annual.csv")
    return df
df = annualReports()




# %% [markdown] 
## Plot annual report
def plotAnnual():
    plt.rcParams["figure.dpi"] = 300
    plt.plot(df.Sec1, label='Section1', color='limegreen')
    plt.plot(df.Sec2a, label='Section2a', color='blue')
    plt.plot(df.Sec2b, label='Section2b', color='deepskyblue')
    plt.plot(df.Sec3, label='Section3', color='red')
    plt.title("Annual precipitation for each section") 
    plt.xlabel("Years ")  
    plt.ylabel("mm/year")
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
    plt.legend(loc=1, prop={"size":6})
    plt.tight_layout()
    plt.savefig("../../004_RishiGanga/04_Images/04_SectionWise/01_Annual.png", facecolor='w', bbox_inches='tight')
    plt.close()
plotAnnual()




# %% [markdown]
## Get DJF reports 
def DJFReports():

    # [1] Resample to monthly scale
    ds1_mon = ds1.resample(time='MS').sum()
    ds2a_mon = ds2a.resample(time='MS').sum()
    ds2b_mon = ds2b.resample(time='MS').sum()
    ds3_mon = ds3.resample(time='MS').sum()

    # [2] Resample to quartely frequency 
    ds1_Q = ds1_mon.resample(time='QS-Dec').sum()
    ds2a_Q = ds2a_mon.resample(time='QS-Dec').sum()
    ds2b_Q = ds2b_mon.resample(time='QS-Dec').sum()
    ds3_Q = ds3_mon.resample(time='QS-Dec').sum() 

    # [3] Pick out DJF sums only 
    ds1_DJF = ds1_Q.where(ds1_Q['time.month'] == 12, drop=True)
    ds2a_DJF = ds2a_Q.where(ds2a_Q['time.month'] == 12, drop=True)
    ds2b_DJF = ds2b_Q.where(ds2b_Q['time.month'] == 12, drop=True)
    ds3_DJF = ds3_Q.where(ds3_Q['time.month'] == 12, drop=True)

    # [4] Replace zeros outside the aoi by nan
    ds1_DJF = ds1_DJF.where(ds1_DJF.prcp_renoj!=0)  
    ds2a_DJF = ds2a_DJF.where(ds2a_DJF.prcp_renoj!=0)  
    ds2b_DJF = ds2b_DJF.where(ds2b_DJF.prcp_renoj!=0)  
    ds3_DJF = ds3_DJF.where(ds3_DJF.prcp_renoj!=0)  

    # [5] Get the spatial means into dataframe
    # [5.1] Define dataframes
    df1 = pd.DataFrame(index=ds1_DJF.time.values, columns=['Sec1'])
    df2a = pd.DataFrame(index=ds2a_DJF.time.values, columns=['Sec2a'])
    df2b = pd.DataFrame(index=ds2b_DJF.time.values, columns=['Sec2b'])
    df3 = pd.DataFrame(index=ds3_DJF.time.values, columns=['Sec3'])

    # [5.2] Get values into dataframes
    for i in td(range(len(df1)), desc='Fetching mean values'):
        df1.Sec1[i] = ds1_DJF.prcp_renoj.isel(time=i).mean().values
        df2a.Sec2a[i] = ds2a_DJF.prcp_renoj.isel(time=i).mean().values
        df2b.Sec2b[i] = ds2b_DJF.prcp_renoj.isel(time=i).mean().values
        df3.Sec3[i] = ds3_DJF.prcp_renoj.isel(time=i).mean().values

    # [5.3] Concatenate the dataframes
    df = pd.concat([df1, df2a, df2b, df3], axis=1)
    df=df.astype(float)
    df = df.drop(df.index[-1])

    df.round(2).to_csv("../../004_RishiGanga/05_CSVs/21_Sectionwise_precp_DJF.csv")
    return df
df_DJF = DJFReports()




# %% [markdown]
## Plot DJF reports 
def plotDJF():
    plt.rcParams["figure.dpi"] = 300
    plt.plot(df_DJF.Sec1, label='Section1', color='limegreen')
    plt.plot(df_DJF.Sec2a, label='Section2a', color='blue')
    plt.plot(df_DJF.Sec2b, label='Section2b', color='deepskyblue')
    plt.plot(df_DJF.Sec3, label='Section3', color='red')
    plt.title("DJF precipitation for each section") 
    plt.xlabel("Years ")  
    plt.ylabel("mm/year")
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
    plt.legend(loc=1, prop={"size":6})
    plt.tight_layout()
    plt.savefig("../../004_RishiGanga/04_Images/04_SectionWise/02_DJF.png", facecolor='w', bbox_inches='tight')
    plt.close()
plotDJF()




# %% [markdown]
## Get JJA reports 
def JJAReports():

    # [1] Resample to monthly scale
    ds1_mon = ds1.resample(time='MS').sum()
    ds2a_mon = ds2a.resample(time='MS').sum()
    ds2b_mon = ds2b.resample(time='MS').sum()
    ds3_mon = ds3.resample(time='MS').sum()

    # [2] Resample to quartely frequency 
    ds1_Q = ds1_mon.resample(time='QS-Jun').sum()
    ds2a_Q = ds2a_mon.resample(time='QS-Jun').sum()
    ds2b_Q = ds2b_mon.resample(time='QS-Jun').sum()
    ds3_Q = ds3_mon.resample(time='QS-Jun').sum() 

    # [3] Pick out DJF sums only 
    ds1_JJA = ds1_Q.where(ds1_Q['time.month'] == 6, drop=True)
    ds2a_JJA = ds2a_Q.where(ds2a_Q['time.month'] == 6, drop=True)
    ds2b_JJA = ds2b_Q.where(ds2b_Q['time.month'] == 6, drop=True)
    ds3_JJA = ds3_Q.where(ds3_Q['time.month'] == 6, drop=True)

    # [4] Replace zeros outside the aoi by nan
    ds1_JJA = ds1_JJA.where(ds1_JJA.prcp_renoj!=0)  
    ds2a_JJA = ds2a_JJA.where(ds2a_JJA.prcp_renoj!=0)  
    ds2b_JJA = ds2b_JJA.where(ds2b_JJA.prcp_renoj!=0)  
    ds3_JJA = ds3_JJA.where(ds3_JJA.prcp_renoj!=0)  

    # [5] Get the spatial means into dataframe
    # [5.1] Define dataframes
    df1 = pd.DataFrame(index=ds1_JJA.time.values, columns=['Sec1'])
    df2a = pd.DataFrame(index=ds2a_JJA.time.values, columns=['Sec2a'])
    df2b = pd.DataFrame(index=ds2b_JJA.time.values, columns=['Sec2b'])
    df3 = pd.DataFrame(index=ds3_JJA.time.values, columns=['Sec3'])

    # [5.2] Get values into dataframes
    for i in td(range(len(df1)), desc='Fetching mean values'):
        df1.Sec1[i] = ds1_JJA.prcp_renoj.isel(time=i).mean().values
        df2a.Sec2a[i] = ds2a_JJA.prcp_renoj.isel(time=i).mean().values
        df2b.Sec2b[i] = ds2b_JJA.prcp_renoj.isel(time=i).mean().values
        df3.Sec3[i] = ds3_JJA.prcp_renoj.isel(time=i).mean().values

    # [5.3] Concatenate the dataframes
    df = pd.concat([df1, df2a, df2b, df3], axis=1)
    df=df.astype(float)
    df = df.drop(df.index[-1])

    df.round(2).to_csv("../../004_RishiGanga/05_CSVs/22_Sectionwise_precp_JJA.csv")
    return df
df_JJA = JJAReports()




# %% [markdown]
## Plot JJA reports 
def plotJJA():
    plt.rcParams["figure.dpi"] = 300
    plt.plot(df_JJA.Sec1, label='Section1', color='limegreen')
    plt.plot(df_JJA.Sec2a, label='Section2a', color='blue')
    plt.plot(df_JJA.Sec2b, label='Section2b', color='deepskyblue')
    plt.plot(df_JJA.Sec3, label='Section3', color='red')
    plt.title("JJA precipitation for each section") 
    plt.xlabel("Years ")  
    plt.ylabel("mm/year")
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
    plt.legend(loc=1, prop={"size":6})
    plt.tight_layout()
    plt.savefig("../../004_RishiGanga/04_Images/04_SectionWise/03_JJA.png", facecolor='w', bbox_inches='tight')
    plt.close()
plotJJA()
print('Time elapsed: ', np.round(time.time()-start,2), 'secs')




# %%
