#libraries
from glob import glob
import os
import pandas as pd
import numpy as np
import re

## Variables
#output table names
OH_SWITCHES_TABLE = 'IN_OH_SW.xlsx'
UG_SWITCHES_TABLE = 'IN_UG_SW.xlsx'
OH_TX_TABLE = 'IN_OH_TX.xlsx'
UG_TX_TABLE = 'IN_UG_TX.xlsx'
UG_PRI_CABLE_TABLE = 'IN_CABLES.xlsx'
NTWK_TX_TABLE = 'IN_NTWK_TX.xlsx'
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
UG_PRI_CABLE_ASSET_CLASS = 'UG_CABLE'
NTWK_TX_ASSET_CLASS = 'NTWK_TX'

# other variables
ASSET_CLASS = 'asset_class_code'
ASSET_SUBCLASS = 'asset_subclass_code'
ASSET_TEMPLATE_FOLDER = 'AssetDataTemplates'

#******************************************************
# fileName - iterate through entire folder
file_AllAssets = 'Original_FiveAssetClasses.xlsx'
file_Poles_XY = 'Asset_XY_files/V2_LatLongPoles.xls'
file_Switches_XY = 'Asset_XY_files/V2_LatLongSwitches.xls'
file_PriOH_XY = 'Asset_XY_files/V2_LatLongPriOH.xls'
file_PriUG_XY = 'Asset_XY_files/V2_LatLongPriUG.xls'
file_Tx_XY = 'Asset_XY_files/V2_LatLongTx.xls'
#fileNameOtherDevices = 'Other Device Numbers.xls'
#**************************
# Reading SwitchGears
#***************************
file_OtherDevices = 'DomainCode_OtherDevices/OtherDeviceNumbers.xlsx'

# Tx Domain code tables
file_DomainCodes_Tx = 'DomainCode_OtherDevices/DomainCodes_Tx.xlsx'


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

# Nearest Neighbor algorithm
from sklearn.neighbors import KNeighborsClassifier
import random, math
from numpy.random import permutation
import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.warn = warn
#nearest_neighbor(df_filled, 'x','y','OH_FEEDERID',3,df_empty)
def nearest_neighbor(dfMain, trainX, trainY, classX, neighborCount, dfUnknown):
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
        print('With k =  ',k,',a score of: ', prediction_results.mean()*100)

    # Let's initialize a classifier
    knn = KNeighborsClassifier(n_neighbors=neighborCount)
    # knn.fit takes two parameters # First, the content we want to train on. For us it's height and weight.
    # Secondly, how we're classifying each element of the training data. We're classifying by position!
    knn.fit(dfMain_train[[trainX, trainY]], dfMain_train[classX])
    predictions = knn.predict(dfMain_test[[trainX,trainY]])
    prediction_results = dfMain_test[classX] == predictions
    print('Prediction accuracy: ',prediction_results.mean()*100) 
    # same as mse = (((prediction_results) ** 2).sum()) / len(predictions)
    predictedValues = knn.predict(dfUnknown[[trainX, trainY]])
    return predictedValues

# Split the df_filled to train and test data
#from sklearn.cross_validation import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X_wine, y_wine,test_size=0.30, random_state=123)
# Compute the mean squared error of our predictions.
# mse = (((predictions - actual) ** 2).sum()) / len(predictions)

#Read xlsx file into dataframes
with pd.ExcelFile(file_AllAssets) as xlsx:
    dfTransformersV1 = pd.read_excel(xlsx, 'Transformers') # 280 rows
    dfSwitchesV1 = pd.read_excel(xlsx, 'Switches') # 239
    dfPolesV1 = pd.read_excel(xlsx, 'Poles') #239
    dfCablesV1 = pd.read_excel(xlsx, 'UGPrimaryCables')
    dfFusesV1 = pd.read_excel(xlsx, 'Fuses') # 44
    dfUGStructuresV1 = pd.read_excel(xlsx, 'UGStructures')
    
#Reading XY coords into dataframes
with pd.ExcelFile(file_Poles_XY) as xls:
    dfPolesXY_V1 = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_Switches_XY) as xls:
    dfSwitchesXY_V1 = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_PriUG_XY) as xls:
    dfPriUGXY_V1 = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_PriOH_XY) as xls:
    dfPriOHXY_V1 = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_Tx_XY) as xls:
    dfTXXY_V1 = pd.read_excel(xls, 'Sheet1')

# 17 columns dropped
dropCommonColumns = ['OBJECTID','WORKORDERID','FIELDVERIFY','COMMENTS','CREATIONUSER','DATECREATED','LASTUSER',
                     'DATEMODIFIED','WORKREQUESTID','DESIGNID','WORKLOCATIONID','WMSID','WORKFLOWSTATUS',
                     'WORKFUNCTION','GISONUMBER','GISOTYPENBR','OWNERSHIP']
					 

#Drop all common columns 
dfSwitchesV1 = drop_columns(dfSwitchesV1, dropCommonColumns)
dfTransformersV1 = drop_columns(dfTransformersV1, dropCommonColumns)
dfFusesV1 = drop_columns(dfFusesV1,dropCommonColumns)
dfCablesV1 = drop_columns(dfCablesV1, dropCommonColumns)
dfUGStructuresV1 = drop_columns(dfUGStructuresV1, dropCommonColumns)
dfPolesV1 = drop_columns(dfPolesV1, dropCommonColumns)

dfSwitchesV1['FEEDERID'] = dfSwitchesV1['FEEDERID'].astype(str)
dfTransformersV1['FEEDERID'] = dfTransformersV1['FEEDERID'].astype(str)
dfFusesV1['FEEDERID'] = dfFusesV1['FEEDERID'].astype(str)
dfCablesV1['FEEDERID'] = dfCablesV1['FEEDERID'].astype(str)

dfSwitchesV1['FEEDERID'] = dfSwitchesV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))
dfTransformersV1['FEEDERID'] = dfTransformersV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))
dfFusesV1['FEEDERID'] = dfFusesV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))
dfCablesV1['FEEDERID'] = dfCablesV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))

# Make one copy
dfTransformers = dfTransformersV1
dfSwitches = dfSwitchesV1
dfPoles = dfPolesV1
dfCables = dfCablesV1
dfFuses = dfFusesV1
dfUGStructures = dfUGStructuresV1
		 
Summary = {'Transformers:': dfTransformersV1.shape,'Switches:':dfSwitchesV1.shape, 'Fuses:': dfFusesV1.shape,
           'Poles:':dfPolesV1.shape, 'Cables:':dfCablesV1.shape, 'UG Structures:': dfUGStructuresV1.shape}

dfSummary = pd.DataFrame(Summary)
print(dfSummary)
