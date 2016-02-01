#libraries
from glob import glob
import os
import pandas as pd
import numpy as np
import re
from collections import defaultdict

# Excel model:
# customer count as '0' 
# OH_TX to 'Aerial Transformer'
# Banking 'Single'
# S-170 '1 vs 3' phase: should be 1 (50kVA)
# 7 2 Phase OH Tx
# CompatibleUnitID - 22 of them needs to be fixed

# Feeder Table: Configuration - "Radial" -> , "Switching_Sections" -> number of switches on trunk, 


## Variables
#output table names
OH_SWITCHES_TABLE = 'IN_OH_SW.xlsx'
UG_SWITCHES_TABLE = 'IN_UG_SW.xlsx'
OH_TX_TABLE = 'IN_OH_TX.xlsx'
UG_TX_TABLE = 'IN_UG_TX.xlsx'
UG_PRI_CABLE_TABLE = 'IN_CABLES.xlsx'
NTWK_TX_TABLE = 'IN_NTWK_TX.xlsx'
POLES_TABLE = 'IN_POLES.xlsx'
#csv
OH_SWITCHES_TABLE_CSV = 'IN_OH_SW.csv'
UG_SWITCHES_TABLE_CSV = 'IN_UG_SW.csv'
OH_TX_TABLE_CSV = 'IN_OH_TX.csv'
UG_TX_TABLE_CSV = 'IN_UG_TX.csv'
UG_PRI_CABLE_TABLE_CSV = 'IN_CABLES.csv'
NTWK_TX_TABLE_CSV = 'IN_NTWK_TX.csv'
#templates for temporary storage
OH_SWITCHES_TABLE_TEMPLATE ='IN_OH_SW_TEMPLATE.xlsx'
UG_SWITCHES_TABLE_TEMPLATE ='IN_UG_SW_TEMPLATE.xls'
OH_TX_TABLE_TEMPLATE = 'IN_OH_TX_TEMPLATE.xlsx'
UG_TX_TABLE_TEMPLATE = 'IN_UG_TX_TEMPLATE.xlsx'
POLES_TABLE_TEMPLATE = 'IN_POLES_TEMPLATE.xlsx'
UG_PRI_CABLE_TABLE_TEMPLATE = 'IN_CABLES_TEMPLATE.xlsx'
NTWK_TX_TABLE_TEMPLATE = 'IN_NTWK_TX_TEMPLATE.xlsx'

# asset_class_code(ACC) names
OH_SWITCHES_ASSET_CLASS ='OH_SW'
UG_SWITCHES_ASSET_CLASS ='UG_SW'
OH_TX_ASSET_CLASS = 'OH_TX'
UG_TX_ASSET_CLASS = 'UG_TX'
POLES_ASSET_CLASS = 'POLE'
#UG_PRI_CABLE_ASSET_CLASS = 'UG_CABLE'
UG_PRI_CABLE_ASSET_CLASS = 'Underground Cable'
NTWK_TX_ASSET_CLASS = 'NTWK_TX'

# other variables
ASSET_CLASS = 'asset_class_code'
ASSET_SUBCLASS = 'asset_subclass_code'
ASSET_TEMPLATE_FOLDER = 'AssetDataTemplates'
RES_LOAD = 'feeder_residential_load'
MED_COM_LOAD = 'feeder_small_med_commercial_load'
LARGE_LOAD = 'feeder_large_commercial_load'

#******************************************************
#input directory
inputDirectory = 'Metsco_Feeder_Reports'
# fileName - iterate through entire folder
file_AllAssets = 'Original_FiveAssetClasses.xlsx'
file_Poles_XY = 'Asset_XY_files/V2_LatLongPoles.xls'
file_Switches_XY = 'Asset_XY_files/V2_LatLongSwitches.xls'
file_PriOH_XY = 'Asset_XY_files/V2_LatLongPriOH.xls'
file_PriUG_XY = 'Asset_XY_files/V2_LatLongPriUG.xls'
file_Tx_XY = 'Asset_XY_files/V2_LatLongTx.xls'
file_PRID_Tx = 'Asset_XY_files/V6_PRID_TX_LOOKUP.xlsx'
file_PRID_OHcond = 'Asset_XY_files/OH_COND_PRID.xlsx'
file_PRID_Switch = 'Asset_XY_files/SW_PRID.xlsx'
OH_COND_PRID_COMPLETE ='Asset_XY_files/OH_COND_PRID_COMPLETE.xlsx'
#**************************
# Reading SwitchGears
#***************************
file_OtherDevices = 'DomainCode_OtherDevices/OtherDeviceNumbers.xlsx'

# Domain code tables
file_DomainCodes_Tx = 'DomainCode_OtherDevices/DomainCodes_Tx.xlsx'
file_DomainCodes_Poles = 'DomainCode_OtherDevices/DomainCodes_PolesClassHeight.xlsx'
file_DomainCodes_PriUG = 'DomainCode_OtherDevices/DomainCodes_PriUG.xlsx'

#******************************************************
# FUNCTIONS
#******************************************************
def warn(*args, **kwargs):
    pass
#import warnings
#warnings.warn = warn

def drop_columns(dfAssetClass, dropColumns):
    dfAssetClass = dfAssetClass.drop(dropColumns, axis=1)
    return dfAssetClass

def new_columns(dfAssetClass, numAssetRows, columnID):
    dfAssetClass[columnID] = pd.DataFrame(np.empty([numAssetRows,1]).cumsum(axis=1))
    dfAssetClass.loc[:,columnID] = np.nan
    return dfAssetClass[columnID]

def concat(*args):
  strs = [str(arg) for arg in args if not pd.isnull(arg)]
  return '_'.join(strs) if strs else np.nan
np_concat = np.vectorize(concat)


# Nearest Neighbor algorithm
from sklearn.neighbors import KNeighborsClassifier
import random, math
from numpy.random import permutation
import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.warn = warn
#nearest_neighbor(df_filled, 'x','y','OH_FEEDERID',3,df_empty)
def nearest_neighbor(dfMain, trainX, trainY, classX, neighborCount, dfUnknown, AssetClass):
    #https://www.dataquest.io/blog/k-nearest-neighbors/
    # Randomly shuffle the index of df_filled.
    random_indices = permutation(dfMain.index)
    # Set a cutoff for how many items we want in the test set (in this case 1/3 of the items)
    test_cutoff = math.floor(len(dfMain)/3)
    # Generate the test set by taking the first 1/3 of the randomly shuffled indices.
    dfMain_test = dfMain.loc[random_indices[1:test_cutoff]]
    # Generate the train set with the rest of the data.
    dfMain_train = dfMain.loc[random_indices[test_cutoff:]]

    for k in [1, 2, 3, 5, 10, 20]:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(dfMain_train[[trainX, trainY]], dfMain_train[classX])

        predictions = knn.predict(dfMain_test[[trainX,trainY]])
        prediction_results = dfMain_test[classX] == predictions
        #print('With k =  ',k,',a score of: ', prediction_results.mean()*100)

    # Let's initialize a classifier
    knn = KNeighborsClassifier(n_neighbors=neighborCount)
    # knn.fit takes two parameters # First, the content we want to train on. For us it's height and weight.
    # Secondly, how we're classifying each element of the training data. We're classifying by position!
    knn.fit(dfMain_train[[trainX, trainY]], dfMain_train[classX])
    predictions = knn.predict(dfMain_test[[trainX,trainY]])
    prediction_results = dfMain_test[classX] == predictions
    print(AssetClass, ' prediction accuracy: ',prediction_results.mean()*100) 
    # same as mse = (((prediction_results) ** 2).sum()) / len(predictions)
    predictedValues = knn.predict(dfUnknown[[trainX, trainY]])
    return predictedValues

# Split the df_filled to train and test data
#from sklearn.cross_validation import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X_wine, y_wine,test_size=0.30, random_state=123)
# Compute the mean squared error of our predictions.
# mse = (((predictions - actual) ** 2).sum()) / len(predictions)
def cable_nearest_neighbor(dfMain, trainX, trainY, trainXend, trainYend, classX, neighborCount, dfUnknown, AssetClass):
    #https://www.dataquest.io/blog/k-nearest-neighbors/
    # Randomly shuffle the index of df_filled.
    random_indices = permutation(dfMain.index)
    # Set a cutoff for how many items we want in the test set (in this case 1/3 of the items)
    test_cutoff = math.floor(len(dfMain)/3)
    # Generate the test set by taking the first 1/3 of the randomly shuffled indices.
    dfMain_test = dfMain.loc[random_indices[1:test_cutoff]]
    # Generate the train set with the rest of the data.
    dfMain_train = dfMain.loc[random_indices[test_cutoff:]]

    for k in [1, 2, 3, 5, 10, 20]:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(dfMain_train[[trainX, trainY, trainXend, trainYend]], dfMain_train[classX])

        predictions = knn.predict(dfMain_test[[trainX,trainY, trainXend, trainYend]])
        prediction_results = dfMain_test[classX] == predictions
        #print('With k =  ',k,',a score of: ', prediction_results.mean()*100)

    # Let's initialize a classifier
    knn = KNeighborsClassifier(n_neighbors=neighborCount)
    # knn.fit takes two parameters # First, the content we want to train on. For us it's height and weight.
    # Secondly, how we're classifying each element of the training data. We're classifying by position!
    knn.fit(dfMain_train[[trainX, trainY, trainXend, trainYend]], dfMain_train[classX])
    predictions = knn.predict(dfMain_test[[trainX,trainY, trainXend, trainYend]])
    prediction_results = dfMain_test[classX] == predictions
    print(AssetClass, ' prediction accuracy: ',prediction_results.mean()*100) 
    # same as mse = (((prediction_results) ** 2).sum()) / len(predictions)
    predictedValues = knn.predict(dfUnknown[[trainX, trainY, trainXend, trainYend]])
    return predictedValues


# define filepath and sort the file list
filesList = glob(os.path.join(inputDirectory, '*.xlsx'))
numFiles = len(filesList)
sortedFileList = sorted(filesList)

# variables
dictFeeders = {}
dfAllNodes_list = pd.DataFrame()
dfAllReclosers = pd.DataFrame()

# read text files in tweet_input directory
for f in sortedFileList:

    fileName = os.path.basename(f).split('_')
    FeederKey = fileName[0]
    #print(FeederKey)
    
    if ('$' not in FeederKey):
        # Read CYME Feeder xlsx file into dataframes
        with pd.ExcelFile(f) as xlsx:
            #dfTopology = pd.read_excel(xlsx, 'Topology', index_col=None, na_values=['NA']) # IGNORE for now
            dfTopology = pd.read_excel(xlsx, 'Topology') # 280 rows
            dfSpotLoads = pd.read_excel(xlsx, 'Spot Loads') # Tot:239 - R/Y/B: 116/108/103 values; based on phases
            dfLoads = pd.read_excel(xlsx, 'Loads') # 239 rows; 'Spot Number\n' col contains unique tx ids
            dfCables = pd.read_excel(xlsx, 'Cables')
            dfSwitches = pd.read_excel(xlsx, 'Switches') # 41 items
            dfNodes = pd.read_excel(xlsx, 'Nodes') # 249 items
            dfOHlines = pd.read_excel(xlsx, 'OverheadLinesByPhase') #Neutral - 94, Section Id - 381
            dfFuses = pd.read_excel(xlsx, 'Fuses') # 44 items
            dfReclosers = pd.read_excel(xlsx, 'Reclosers')

            # # Strip '\n' from column headers
            dfTopology.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfSpotLoads.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfLoads.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfCables.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfSwitches.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfNodes.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfOHlines.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfFuses.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            dfReclosers.rename(columns=lambda x: x.replace('\n',''), inplace=True)
            #print(dfNodes.columns)
            #dfAllNodes_list = dfAllNodes_list.append(dfOHlines)
            #dfAllNodes_list = dfAllNodes_list.append(dfNodes)
            dfAllReclosers = dfAllReclosers.append(dfReclosers)

print('Number of Feeders: ', numFiles)

dropReclosers = ['Section Id', 'Status', 'State', 'From Node','Manufacturer']
dfAllReclosers = drop_columns(dfAllReclosers, dropReclosers)
dfAllReclosers = dfAllReclosers.rename(columns={'To Node':'id'})
#*****************************************************************************************************
# Cell # 7: Finding circuits for poles by matching with all nodes 
#*****************************************************************************************************
MasterFile = pd.ExcelWriter('Reclosers.xlsx')
dfAllReclosers.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('*****RECLOSER TABLE YES! ****')
