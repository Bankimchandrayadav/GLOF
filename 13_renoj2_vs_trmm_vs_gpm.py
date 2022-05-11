# %% [markdown] 
## About 
# This code is for plotting comparisons of RENOJ2, TRMM and GPM data over the slide area monthwise




# %% [markdown]
## Libs 
from tqdm.notebook import tqdm as td 
import pandas as pd, matplotlib.pyplot as plt, numpy as np  




# %% [markdown]
## Read files 
# [1] RENOJ2
dfRNJ = pd.read_csv("../../004_RishiGanga/05_CSVs/12_renoj2_over_slide_monthly_grouped.csv")
dfRNJ.set_index('Unnamed: 0', inplace=True, drop=True)
dfRNJ.index.names=[None] 

# [2] GPM 
dfGPM = pd.read_csv("../../004_RishiGanga/05_CSVs/11_gpm_over_slide_monthly_grouped.csv")
dfGPM.set_index('Unnamed: 0', inplace=True, drop=True)
dfGPM.index.names=[None] 

# [3] TRMM
# [3.1] Read 
dfTRMM = pd.read_csv("../../004_RishiGanga/05_CSVs/09_trmm_over_slide_monthly_grouped.csv")
dfTRMM.set_index('Unnamed: 0', inplace=True, drop=True)
dfTRMM.index.names=[None] 

# [3.2] Change index 
indices = list(dfTRMM.index.values)  # indices got into a list 
for i in range(len(indices)):
    indices[i] = int(indices[i][:4])  # list corrected
dfTRMM.index = indices # new indices reassigned




# %% [markdown]
## Plot 
for i in td(range(len(dfRNJ.columns)), desc='Saving plots'):

    # [1] Concatenate the cols of all df belonging to same months
    dfTMP = pd.concat([dfRNJ.iloc[:,i], dfGPM.iloc[:,i], dfTRMM.iloc[:,i]], axis=1)
    dfTMP.columns = ['RNJ', 'GPM', 'TRMM']  # col names changed

    # [2] Plot the concatenated dataframes
    plt.rcParams["figure.dpi"] = 300
    dfTMP.plot(kind='bar')
    plt.xlabel('Years')
    plt.ylabel('Precipitation (mm/month)')
    plt.tight_layout()
    plt.title('Precipitation over slide for month={}'.format(dfRNJ.columns[i]))
    plt.minorticks_on()
    plt.savefig("../../004_RishiGanga/04_Images/01_Comparisons_of_RENOJ2_over_slide/{}_{}.png".format(str(i).zfill(2), dfRNJ.columns[i]), bbox_inches='tight', facecolor='w')
    plt.close()




# %%
