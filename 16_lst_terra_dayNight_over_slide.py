# %% [markdown]
# # About
# This code reports the LST data over the slide area in all the four grades of QA [https://www.youtube.com/watch?v=JPjkjjhj5rk] for the day and night of MOD11A1 and MYD11A1.




# %% [markdown]
## Libs 
import xarray as xr, pandas as pd, numpy as np, time, glob
from tqdm.notebook import tqdm as td 
import matplotlib.pyplot as plt 
start = time.time()




# %% [markdown]
## [1] Function to extract LST of different grades
def LSTExtraction(dsIn,hour,quality):
    
    # [1.1] Extract LST values of specific quality
    dsTemp = dsIn.copy(deep=True)
    for k in td(range(len(dsTemp.time)), desc='{} LST of quality={}'.format(hour, quality)):
        for i in range(3):
            for j in range(5):
                qc = dsTemp['QC_{}'.format(hour)].isel(time=k).values[i,j]  # qc value at loc (i,j) 
                if np.isnan(qc):  # qc==nan values ignored
                    pass
                else:
                    qc = int(qc)  # qc float to integer
                    qc = '{:08b}'.format(qc)[:2]  # int to 'binary string'
                    if qc == quality:   

                        # [1.1.1] if above condition==False then convert to nan
                        dsTemp['LST_{}_1km'.format(hour)].isel(time=k).values[i,j] = np.nan  

    # [1.2] Get extracted values' mean into a dataframe 
    # [1.2.1] Prepare a dataframe
    dfTemp = pd.DataFrame(index=dsTemp.time.values, columns=['Quality_{}'.format(quality)])

    # [1.2.2] Get the LST time series into the dataframe
    for i in range(len(dsTemp.time)):
        dfTemp['Quality_{}'.format(quality)][i] = np.round((np.float32(dsTemp['LST_{}_1km'.format(hour)].isel(time=i).mean().values)),2)

    return dfTemp




# %% [markdown]
## [2] Read Terra LST
def readTerraLST():

    # [2.1] Read
    dsT1 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/01_Terra/File1.nc")
    dsT2 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/01_Terra/File2.nc")
    dsT3 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/01_Terra/File3.nc")
    dsT4 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/01_Terra/File4.nc")
    dsTerra = xr.concat([dsT1,dsT2,dsT3, dsT4], dim='time')  # all datasets concatenated

    # [2.2] Change julian time to datetime
    datetimeindex = dsTerra.indexes['time'].to_datetimeindex()  
    dsTerra['time'] = datetimeindex

    # [2.3] Change kelvin to celsius
    dsTerra['LST_Day_1km'] = dsTerra['LST_Day_1km'] - 273.15  
    dsTerra['LST_Night_1km'] = dsTerra['LST_Night_1km'] - 273.15

    return dsTerra
dsTerra=readTerraLST()




# %% [markdown]
## [3] Get the day and night time Terra LST
def getTerraLST():
    # [3.1] Get the day time LST data of 4 grades 
    dfDay1 = LSTExtraction(dsIn=dsTerra, hour='Day', quality='00')
    dfDay2 = LSTExtraction(dsIn=dsTerra, hour='Day', quality='01')
    dfDay3 = LSTExtraction(dsIn=dsTerra, hour='Day', quality='10')
    dfDay4 = LSTExtraction(dsIn=dsTerra, hour='Day', quality='11')

    # [3.2] Combine it 
    dfDayT = pd.concat([dfDay1, dfDay2, dfDay3, dfDay4], axis=1)

    # [3.3] Get the night time LST data of 4 grades 
    dfNight1 = LSTExtraction(dsIn=dsTerra, hour='Night', quality='00')
    dfNight2 = LSTExtraction(dsIn=dsTerra, hour='Night', quality='01')
    dfNight3 = LSTExtraction(dsIn=dsTerra, hour='Night', quality='10')
    dfNight4 = LSTExtraction(dsIn=dsTerra, hour='Night', quality='11')

    # [3.4] Combine it 
    dfNightT = pd.concat([dfNight1, dfNight2, dfNight3, dfNight4], axis=1)

    return dfDayT, dfNightT
dfDayT, dfNightT = getTerraLST()



#%% [markdown]
## [4] Read Aqua LST
def readAquaLST():
    
    # [4.1] Read
    dsT1 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/02_Aqua/File1.nc")
    dsT2 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/02_Aqua/File2.nc")
    dsT3 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/02_Aqua/File3.nc")
    dsT4 = xr.open_dataset("../../004_RishiGanga/02_RS_data/01_Raster/01_LST/01_Slide/01_AllTimes/02_Aqua/File4.nc")
    dsAqua = xr.concat([dsT1,dsT2,dsT3, dsT4], dim='time')  # all datasets concatenated

    # [4.2] Change julian time to datetime
    datetimeindex = dsAqua.indexes['time'].to_datetimeindex()  
    dsAqua['time'] = datetimeindex

    # [4.3] Change kelvin to celsius
    dsAqua['LST_Day_1km'] = dsAqua['LST_Day_1km'] - 273.15  
    dsAqua['LST_Night_1km'] = dsAqua['LST_Night_1km'] - 273.15

    return dsAqua
dsAqua=readAquaLST()




# %% [markdown]
## [5] Get the day and night time Aqua LST
def getAquaLST():

    # [5.1] Get the day time LST data of 4 grades 
    dfDay1 = LSTExtraction(dsIn=dsAqua, hour='Day', quality='00')
    dfDay2 = LSTExtraction(dsIn=dsAqua, hour='Day', quality='01')
    dfDay3 = LSTExtraction(dsIn=dsAqua, hour='Day', quality='10')
    dfDay4 = LSTExtraction(dsIn=dsAqua, hour='Day', quality='11')

    # [5.2] Combine it 
    dfDayA = pd.concat([dfDay1, dfDay2, dfDay3, dfDay4], axis=1)

    # [5.3] Get the night time LST data of 4 grades 
    dfNight1 = LSTExtraction(dsIn=dsAqua, hour='Night', quality='00')
    dfNight2 = LSTExtraction(dsIn=dsAqua, hour='Night', quality='01')
    dfNight3 = LSTExtraction(dsIn=dsAqua, hour='Night', quality='10')
    dfNight4 = LSTExtraction(dsIn=dsAqua, hour='Night', quality='11')

    # [5.4] Combine it 
    dfNightA = pd.concat([dfNight1, dfNight2, dfNight3, dfNight4], axis=1)

    return dfDayA, dfNightA
dfDayA, dfNightA = getAquaLST()




# %% [markdown]
## [6] Merge all 4 LST data
def toCSV():
    df = pd.concat([dfDayT,dfNightT,dfDayA, dfNightA], axis=1)
    df.columns = ['TerraDayQ1', 'TerraDayQ2', 'TerraDayQ3', 'TerraDayQ4',
                'TerraNightQ1', 'TerraNightQ2', 'TerraNightQ3', 'TerraNightQ4',
                'AquaDayQ1', 'AquaDayQ2', 'AquaDayQ3', 'AquaDayQ4',
                'AquaNightQ1', 'AquaNightQ2', 'AquaNightQ3', 'AquaNightQ4',
                ]
    df.to_csv("../../004_RishiGanga/05_CSVs/19_SlideRegion_Terra_Aqua.csv")
toCSV()
print('Time elapsed: {} mins'.format(np.round((time.time()-start)/60, 2)))





# %%
