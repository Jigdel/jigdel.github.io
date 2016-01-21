#libraries
from glob import glob
import os
import pandas as pd
import numpy as np
import re

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
# fileName - iterate through entire folder
file_AllAssets = 'Original_FiveAssetClasses.xlsx'
file_Poles_XY = 'Asset_XY_files/V2_LatLongPoles.xls'
file_Switches_XY = 'Asset_XY_files/V2_LatLongSwitches.xls'
file_PriOH_XY = 'Asset_XY_files/V2_LatLongPriOH.xls'
file_PriUG_XY = 'Asset_XY_files/V2_LatLongPriUG.xls'
file_Tx_XY = 'Asset_XY_files/V2_LatLongTx.xls'
file_PRID_Tx = 'V6_PRID_TX_LOOKUP.xlsx'

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

#Read xlsx file into dataframes
with pd.ExcelFile(file_AllAssets) as xlsx:
    dfTransformersV1 = pd.read_excel(xlsx, 'Transformers') # 280 rows
    dfSwitchesV1 = pd.read_excel(xlsx, 'Switches') # 239
    dfPolesV1 = pd.read_excel(xlsx, 'Poles') #239
    dfPriUGV1 = pd.read_excel(xlsx, 'UGPrimaryCables')
    dfFusesV1 = pd.read_excel(xlsx, 'Fuses') # 44
    dfUGStructuresV1 = pd.read_excel(xlsx, 'UGStructures')
    
#Reading XY coords into dataframes
with pd.ExcelFile(file_Poles_XY) as xls:
    dfPolesXY = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_Switches_XY) as xls:
    dfSwitchesXY = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_PriUG_XY) as xls:
    dfPriUGXY = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_PriOH_XY) as xls:
    dfPriOHXY = pd.read_excel(xls, 'Sheet1')
with pd.ExcelFile(file_Tx_XY) as xls:
    dfTxXY = pd.read_excel(xls, 'Sheet1')

# 17 columns dropped
dropCommonColumns = ['OBJECTID','WORKORDERID','FIELDVERIFY','COMMENTS','CREATIONUSER','DATECREATED','LASTUSER',
                     'DATEMODIFIED','WORKREQUESTID','DESIGNID','WORKLOCATIONID','WMSID','WORKFLOWSTATUS',
                     'WORKFUNCTION','GISONUMBER','GISOTYPENBR','OWNERSHIP']
					 
#Drop all common columns 
dfSwitchesV1 = drop_columns(dfSwitchesV1, dropCommonColumns)
dfTransformersV1 = drop_columns(dfTransformersV1, dropCommonColumns)
dfFusesV1 = drop_columns(dfFusesV1,dropCommonColumns)
dfPriUGV1 = drop_columns(dfPriUGV1, dropCommonColumns)
dfUGStructuresV1 = drop_columns(dfUGStructuresV1, dropCommonColumns)
dfPolesV1 = drop_columns(dfPolesV1, dropCommonColumns)

dfSwitchesV1['FEEDERID'] = dfSwitchesV1['FEEDERID'].astype(str)
dfTransformersV1['FEEDERID'] = dfTransformersV1['FEEDERID'].astype(str)
dfFusesV1['FEEDERID'] = dfFusesV1['FEEDERID'].astype(str)
dfPriUGV1['FEEDERID'] = dfPriUGV1['FEEDERID'].astype(str)

dfSwitchesV1['FEEDERID'] = dfSwitchesV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))
dfTransformersV1['FEEDERID'] = dfTransformersV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))
dfFusesV1['FEEDERID'] = dfFusesV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))
dfPriUGV1['FEEDERID'] = dfPriUGV1['FEEDERID'].apply(lambda x: re.sub('[\s+]', '', x))

# Make one copy
dfTransformers = dfTransformersV1
dfSwitches = dfSwitchesV1
dfPoles = dfPolesV1
dfPriUG = dfPriUGV1
dfFuses = dfFusesV1
dfUGStructures = dfUGStructuresV1
		 
Summary = {'Transformers:': dfTransformersV1.shape,'Switches:':dfSwitchesV1.shape, 'Fuses:': dfFusesV1.shape,
           'Poles:':dfPolesV1.shape, 'Cables:':dfPriUGV1.shape, 'UG Structures:': dfUGStructuresV1.shape}

dfSummary = pd.DataFrame(Summary)
print(dfSummary)

#************************************
# ASSET TABLES
#************************************
#***********************************
# Asset class specific dictionaries
#***********************************
# OPERATING VOLTAGE 190=8kv, 250=13.8kv, 1267 = 0kv, 1237 = 138kv
operatingVoltageDict = {'190':'8000','250':'13800','1267':'0','1237':'138000'}

# Phasing change - need to change it to 'str' type, int/float dict key lookup doesn't work
#phasingDict = {'1.0': '1Ph', '2.0':'1Ph','4.0':'1Ph','3.0':'2Ph','5.0':'2Ph','6.0':'2Ph','7.0':'3Ph'}
phasingDict = {'1': '1', '2':'1','4':'1','3':'2','5':'2','6':'2','7':'3'}

#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# TRANSFORMERS 
#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************

# dictOHTxSubclass = {'1':'Standard 1Ph','9':'Standard 3Ph','10':'Standard 2Ph'}
# dictUGTxSubclass = {'2':'Padmount 1Ph','3':'Network Submersible','5':'Submersible', '7':'Padmount 3Ph'}
dictOHTxSubclass = {'1':'POLE_TOP','9':'POLE_TOP','10':'POLE_TOP'}
dictUGTxSubclass = {'2':'PAD_MOUNTED','3':'NETWORK_SUBMERSIBLE','5':'SUBMERSIBLE', '7':'PAD_MOUNTED'}

# Drop columns
dropTxCols = ['ANCILLARYROLE', 'ENABLED', 'FEEDERID2', 'FEEDERINFO', 'ELECTRICTRACEWEIGHT', 'LOCATIONID', 'SYMBOLROTATION', 
              'GPSDATE', 'LABELTEXT', 'NOMINALVOLTAGE', 'GROUNDREACTANCE', 'GROUNDRESISTANCE', 
              'MAGNETIZINGREACTANCE', 'MAGNETIZINGRESISTANCE', 'HIGHSIDEGROUNDREACTANCE','HIGHSIDEGROUNDRESISTANCE', 
              'HIGHSIDEPROTECTION', 'LOCATIONTYPE','COOLINGTYPE', 'FEATURE_STATUS','KVA', 'DEMAND_KVA',
              'DEMAND_DATE_MM_DD_YYYY', 'STREET_LIGHT_FACILITY', 'HIGHSIDECONFIGURATION', 'LOWSIDECONFIGURATION',
              'LOWSIDEGROUNDRESISTANCE', 'LOWSIDEVOLTAGE', 'LATITUDE', 'LONGITUDE']

# drop asset columns
dfTransformers = drop_columns(dfTransformers,dropTxCols)

numTxRows = len(dfTransformers['DEVICENUMBER'])

# Rename Transformer columns
dfTransformers = dfTransformers.rename(columns={'DEVICENUMBER':'ID',
                                                'PHASEDESIGNATION':'Type',
                                                'INSTALLATIONDATE':'INSTALL_YEAR',
                                                'FEEDERID':'CIRCUIT',
                                                'RATEDKVA':'KVA'})

# Separate year
dfTransformers['INSTALL_YEAR'] = dfTransformers['INSTALL_YEAR'].apply(lambda x: x.year)
dfTransformers = dfTransformers[dfTransformers['KVA'] >= 5]

# Additional columns
dfTransformers[ASSET_CLASS] = new_columns(dfTransformers, numTxRows, ASSET_CLASS)
dfTransformers['HI'] = new_columns(dfTransformers, numTxRows,'HI')
dfTransformers['HI'] = 'NA'
dfTransformers['IN_VALLEY'] = new_columns(dfTransformers, numTxRows,'IN_VALLEY')
dfTransformers['IN_VALLEY'] = 'NA'
dfTransformers['PCB'] = new_columns(dfTransformers, numTxRows,'PCB')
dfTransformers['PCB'] = 51 #worst case scenario
dfTransformers['STATION'] = new_columns(dfTransformers, numTxRows,'STATION')
dfTransformers['STATION'] = 'NA'
dfTransformers['NEIGHBORHOOD_ID'] = new_columns(dfTransformers, numTxRows,'NEIGHBORHOOD_ID')
dfTransformers['NEIGHBORHOOD_ID'] = 'NA'
dfTransformers['CUSTOMER_COUNT'] = new_columns(dfTransformers, numTxRows,'CUSTOMER_COUNT')
dfTransformers['CUSTOMER_COUNT'] = 0
dfTransformers['DEVICE_RESIDENTIAL'] = new_columns(dfTransformers, numTxRows,'DEVICE_RESIDENTIAL')
dfTransformers['DEVICE_COMMERCIAL'] = new_columns(dfTransformers, numTxRows,'DEVICE_COMMERCIAL')
dfTransformers['DEVICE_INDUSTRIAL'] = new_columns(dfTransformers, numTxRows,'DEVICE_INDUSTRIAL')
dfTransformers['UPSTREAM_DEVICE'] = new_columns(dfTransformers, numTxRows,'UPSTREAM_DEVICE')
#dfTransformers[''] = new_columns(dfTransformers, numTxRows,'')

# Commented out as PRID table join makes these columns redundant
# dfTransformers['PRID'] = new_columns(dfTransformers, numTxRows,'PRID')
# dfTransformers['TX_RESIDENTIAL'] = new_columns(dfTransformers, numTxRows,'TX_RESIDENTIAL')
# dfTransformers['TX_COMMERCIAL'] = new_columns(dfTransformers, numTxRows,'TX_COMMERCIAL')
# dfTransformers['TX_INDUSTRIAL'] = new_columns(dfTransformers, numTxRows,'TX_INDUSTRIAL')

#******************************************************
# FILTER OUT ASSET CLASSES WITH THEIR RESPECTIVE SUBTYPES
#******************************************************
# To avoid index vs copy error: pd.DataFrame...necessary (spent 4 hours getting rid of the warning error!)
# UG Tx: 2/3/5/7 - 1Ph/Ntwk/Sub/Pad 3Ph [1436,27,4,507: 1642 counts]
dfUGTransformers = pd.DataFrame(dfTransformers[(dfTransformers.SUBTYPECD == 2) | 
                                  (dfTransformers.SUBTYPECD == 3) | 
                                  (dfTransformers.SUBTYPECD == 5) | 
                                  (dfTransformers.SUBTYPECD == 7) ])

# OH Tx: 1/9/10 - 1Ph/3Ph/2Ph [1125/510/7: 1347 counts]
dfOHTransformers = pd.DataFrame(dfTransformers[(dfTransformers.SUBTYPECD == 1) | 
                                  (dfTransformers.SUBTYPECD == 9) | 
                                  (dfTransformers.SUBTYPECD == 10)])

#******************************************************
# Replace Asset class and 'SUBTYPECD' with actual tx types
#******************************************************
numOHTxRows = len(dfOHTransformers['ID'])
numUGTxRows = len(dfUGTransformers['ID'])

dfOHTransformers['SUBTYPECD'] = dfOHTransformers['SUBTYPECD'].astype(str)
dfUGTransformers['SUBTYPECD'] = dfUGTransformers['SUBTYPECD'].astype(str)

#Try using .loc[row_indexer,col_indexer] = value instead
dfOHTransformers.loc[:,'SUBTYPECD'] = dfOHTransformers['SUBTYPECD'].apply(lambda x: dictOHTxSubclass[x])
dfUGTransformers.loc[:,'SUBTYPECD'] = dfUGTransformers['SUBTYPECD'].apply(lambda x: dictUGTxSubclass[x])

# Fill in Asset and asset subclass columns
dfOHTransformers = dfOHTransformers.rename(columns={'SUBTYPECD':ASSET_SUBCLASS})
dfUGTransformers = dfUGTransformers.rename(columns={'SUBTYPECD':ASSET_SUBCLASS})

# Remaining OH Tx and UG Tx specific columns
dfOHTransformers['BANKING'] = new_columns(dfOHTransformers, numOHTxRows,'BANKING')
dfOHTransformers['BANKING'] = dfOHTransformers['UNITS'].apply(lambda x: x)
dfUGTransformers['BANKING'] = new_columns(dfUGTransformers, numOHTxRows,'BANKING')
dfUGTransformers['BANKING'] = dfUGTransformers['UNITS'].apply(lambda x: x)

dfUGTransformers['PEDESTAL'] = new_columns(dfUGTransformers, numUGTxRows,'PEDESTAL')
dfUGTransformers['PEDESTAL'] = 'NA'
dfUGTransformers['SWITCHABLE'] = new_columns(dfUGTransformers, numUGTxRows,'SWITCHABLE')
dfUGTransformers['SWITCHABLE'] = 'NA'
dfUGTransformers['SWITCH_TYPE'] = new_columns(dfUGTransformers, numUGTxRows,'SWITCH_TYPE')
dfUGTransformers['SWITCH_TYPE'] = 'NA'

#print(numOHTxRows, numUGTxRows)
#print(dfOHTransformers.columns)

# Tx Domain code tables
with pd.ExcelFile(file_DomainCodes_Tx) as xls:
    #dfTopology = pd.read_excel(xlsx, 'Topology', index_col=None, na_values=['NA']) # IGNORE for now
    dfUGTxDomainCodes = pd.read_excel(xls, 'UGTransformers')
    dfOHTxDomainCodes = pd.read_excel(xls, 'OHTransformers')

# Convert to string for merge purposes
dfOHTransformers['COMPATIBLEUNITID'] = dfOHTransformers['COMPATIBLEUNITID'].astype(str)
dfUGTransformers['COMPATIBLEUNITID'] = dfUGTransformers['COMPATIBLEUNITID'].astype(str)
dfOHTxDomainCodes['COMPATIBLEUNITID'] = dfOHTxDomainCodes['COMPATIBLEUNITID'].astype(str)
dfUGTxDomainCodes['COMPATIBLEUNITID'] = dfUGTxDomainCodes['COMPATIBLEUNITID'].astype(str)
#print(dfUGTxDomainCodes.head())

#dfOHTransformers=pd.merge(dfOHTransformers, dfOHTxDomainCodes, how='left', on='COMPATIBLEUNITID')
dfOHTransformers=dfOHTransformers.merge(dfOHTxDomainCodes, how='left', on='COMPATIBLEUNITID')
dfUGTransformers=dfUGTransformers.merge(dfUGTxDomainCodes, how='left', on='COMPATIBLEUNITID')
#print(dfUGTransformers.head(2))

#dropOHTxCols = ['COMPATIBLEUNITID','Description','PRIMARY_VOLTAGE','NAMEPLATE','PHASING','FAULTINDICATOR','UNITS','Tx_type_counts']
#dropUGTxCols = ['COMPATIBLEUNITID','Description','PRIMARY_VOLTAGE','NAMEPLATE','PHASING','FAULTINDICATOR','UNITS','Tx_type_counts']
dropOHTxCols = ['COMPATIBLEUNITID','Description','PRIMARY_VOLTAGE','NAMEPLATE','FAULTINDICATOR','UNITS','Tx_type_counts']
dropUGTxCols = ['COMPATIBLEUNITID','Description','PRIMARY_VOLTAGE','NAMEPLATE','FAULTINDICATOR','UNITS','Tx_type_counts']
#'Fused','UNITS',
# drop columns
dfOHTransformers = drop_columns(dfOHTransformers,dropOHTxCols)
dfUGTransformers = drop_columns(dfUGTransformers,dropUGTxCols)

# Replace 'Asset Subclass' col with actual names
# Rename proper asset nomenclature
dfOHTransformers[ASSET_CLASS] = OH_TX_ASSET_CLASS
dfUGTransformers[ASSET_CLASS] = UG_TX_ASSET_CLASS

#******************************************************
#phasingDict = {'1.0': '1Ph', '2.0':'1Ph','4.0':'1Ph','3.0':'2Ph','5.0':'2Ph','6.0':'2Ph','7.0':'3Ph'}

# OH and UG Tx - 'operational voltage'
#operatingVoltageDict = {'190':'8000','250':'13800','1267':'0','1237':'138000'}
dfOHTransformers['OPERATINGVOLTAGE'] = dfOHTransformers['OPERATINGVOLTAGE'].astype(str)
dfUGTransformers['OPERATINGVOLTAGE'] = dfUGTransformers['OPERATINGVOLTAGE'].astype(str)
dfOHTransformers['OPERATINGVOLTAGE'] = dfOHTransformers['OPERATINGVOLTAGE'].apply(lambda x: operatingVoltageDict[x])
dfUGTransformers['OPERATINGVOLTAGE'] = dfUGTransformers['OPERATINGVOLTAGE'].apply(lambda x: operatingVoltageDict[x])

dfOHTransformers['Type'] = dfOHTransformers['Type'].astype(str)
dfUGTransformers['Type'] = dfUGTransformers['Type'].astype(str)
dfOHTransformers['Type'] = dfOHTransformers['Type'].apply(lambda x: phasingDict[x])
dfUGTransformers['Type'] = dfUGTransformers['Type'].apply(lambda x: phasingDict[x])

#******************************************************
# Rename col names - is phasing and type the same? I've got phasing in Domain codes table
dfOHTransformers = dfOHTransformers.rename(columns={'OPERATINGVOLTAGE': 'primary_voltage','Type': 'dropPhasing'})
dfUGTransformers = dfUGTransformers.rename(columns={'OPERATINGVOLTAGE': 'primary_voltage','Type': 'dropPhasing'})
#Using Domain code Phasing values
dfOHTransformers = drop_columns(dfOHTransformers,'dropPhasing')
dfUGTransformers = drop_columns(dfUGTransformers,'dropPhasing')
# Lower case column names
dfOHTransformers.columns = map(str.lower, dfOHTransformers.columns)
dfUGTransformers.columns = map(str.lower, dfUGTransformers.columns)
dfUGTransformers = dfUGTransformers[dfUGTransformers['asset_subclass_code'] != 'NETWORK_SUBMERSIBLE']


#PRIDs to TX match
with pd.ExcelFile(file_PRID_Tx) as xls:
  dfPRIDtx = pd.read_excel(xls, 'prid')

#remove the column and rename it in near future
dfPRIDtx = dfPRIDtx.rename(columns={'transformerid':'id'})

dfOHTransformers = dfOHTransformers.merge(dfPRIDtx, how='left', on='id')
dfUGTransformers = dfUGTransformers.merge(dfPRIDtx, how='left', on='id')


# These next lines can be removed when PRID is calculated automatically in this same file
#PRIDdropCols = ['tx_residential','tx_commercial','tx_industrial']
PRIDdropCols = [RES_LOAD,MED_COM_LOAD,LARGE_LOAD]
dfOHTransformers = drop_columns(dfOHTransformers, PRIDdropCols)
dfUGTransformers = drop_columns(dfUGTransformers, PRIDdropCols)

# dfPRID_OHtx = dfPRID_OHtx.rename(columns={RES_LOAD:'tx_residential',
#                                           MED_COM_LOAD:'tx_med_com_load',
#                                           LARGE_LOAD:'tx_large_commercial_load',
#                                           'PRID':'prid'})

#'secondary_voltage','fused','banking'
dfOHTransformers['kva'] = dfOHTransformers['kva'].astype(float)
dfUGTransformers['kva'] = dfUGTransformers['kva'].astype(float)
dfOHTransformers['phasing'] = dfOHTransformers['phasing'].astype(float)
dfUGTransformers['phasing'] = dfUGTransformers['phasing'].astype(float)

def phasing_kva(phasing,kva,custClass):
    if((kva > 350) & (custClass=='classLarge')):
        return kva/2
    elif((phasing == 3) & (kva <=350) & (custClass=='classMed')):
        return kva/2
    elif((phasing != 3) & (kva <=150) & (custClass=='classRx')):
        return kva/2
    else:
        return 0
# def valuation_formula(x, y):
#     return x * y * 0.5
#df['price'] = df.apply(lambda row: valuation_formula(row['x'], row['y']), axis=1)

dfOHTransformers['tx_residential'] = dfOHTransformers.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classRx'), axis=1)
dfOHTransformers['tx_commercial'] = dfOHTransformers.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classMed'), axis=1)
dfOHTransformers['tx_industrial'] = dfOHTransformers.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classLarge'), axis=1)

dfUGTransformers['tx_residential'] = dfUGTransformers.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classRx'), axis=1)
dfUGTransformers['tx_commercial'] = dfUGTransformers.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classMed'), axis=1)
dfUGTransformers['tx_industrial'] = dfUGTransformers.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classLarge'), axis=1)

# for index, row in dfPRID_OHtx.iterrows():
#     row['tx_residential'] = phasing_kva(row['phasing'],row['kva'])

dfOHTransformers.index.name = 'asset_id'
dfUGTransformers.index.name = 'asset_id'

# dfPRID_OHtx = dfPRID_OHtx[['asset_class_code','id','circuit','install_year','asset_subclass_code','hi','phasing',
#                            'primary_voltage','kva','tx_residential','tx_commercial','tx_industrial','device_residential',
#                            'device_commercial','device_industrial','upstream_device','prid','in_valley','pcb','banking',
#                            'secondary_voltage','fused']]
# dfPRID_UGtx = dfPRID_UGtx[['asset_subclass_code','asset_class_code','install_year','hi','phasing','prid','circuit',
#                            'primary_voltage','kva','tx_residential','tx_commercial','tx_industrial','device_residential',
#                            'device_commercial','device_industrial','upstream_device','pcb','pedestal','switchable',
#                            'switch_type','id','secondary_voltage','fused','banking']]
#Here
#******************************************************
# REARRANGE COLUMNS
#******************************************************
# *All tables need 'asset_id' - rename index
dfOHTransformers = dfOHTransformers[['asset_class_code','id','circuit','install_year','asset_subclass_code','hi','phasing','primary_voltage','kva',
                                     'tx_residential','tx_commercial','tx_industrial','device_residential','device_commercial','device_industrial',
                                     'upstream_device','prid','in_valley','pcb','banking','secondary_voltage','fused','station','neighborhood_id',
                                     'customer_count']]
#'faultindicator','type','units','tx_type_counts','sec_voltage','fused'

dfUGTransformers = dfUGTransformers[['asset_subclass_code','asset_class_code','install_year','hi','phasing','prid','circuit','primary_voltage','kva',
                                    'in_valley','tx_residential','tx_commercial','tx_industrial','device_residential','device_commercial',
                                    'device_industrial','upstream_device','pcb','pedestal','switchable','switch_type','id','secondary_voltage','fused',
                                    'banking','station','neighborhood_id','customer_count']]

#******************************************************
# OUTPUT DATAFRAMES TO EXCEL MODEL
#******************************************************
dfOHtx_excel = dfOHTransformers
dfUGtx_excel = dfUGTransformers

# excel_dropOHtx = ['asset_subclass_code', 'fused','asset_class_code']
# dfOHtx_excel = drop_columns(dfOHtx_excel, excel_dropOHtx)
# dfUGtx_excel = drop_columns(dfUGtx_excel, excel_dropUGtx)
dfOHtx_excel['asset_class_code']='Aerial Transformer'
dfUGtx_excel['asset_class_code']='Underground Transformer'

dfOHtx_excel = dfOHtx_excel.rename(columns={'asset_class_code':'class',
                                            'asset_subclass_code':'type'})

dfUGtx_excel = dfUGtx_excel.rename(columns={'asset_class_code':'class',
                                            'asset_subclass_code':'type'})
#******************************************************
# OUTPUT DATAFRAMES TO EXCEL FILES
#******************************************************
# OH TX
dfOHtx_later = dfOHTransformers
MasterFile = pd.ExcelWriter(OH_TX_TABLE_TEMPLATE)
dfOHtx_excel.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
# UG TX
dfUGtx_later = dfUGTransformers
MasterFile = pd.ExcelWriter(UG_TX_TABLE_TEMPLATE)
dfUGtx_excel.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('OH and UG Tx data munging completed')

#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# UNDERGROUND SWITCHES
#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# 422/431/321 as SC_ELEC
# dictSGassetSubclass = {'PMH-3':'AIR_INSULATED_LIVEFRONT_PMH-9','PMH-5':'AIR_INSULATED_LIVEFRONT_PMH-9',
#                        'PMH-9':'AIR_INSULATED_LIVEFRONT_PMH-9','PMH-11':'AIR_INSULATED_LIVEFRONT_PMH-11',
#                        'PME-9':'AIR_INSULATED_DEADFRONT_PME-9','PME-10':'AIR_INSULATED_DEADFRONT_PME-9',
#                        'PME-11':'AIR_INSULATED_DEADFRONT_PME-11','VISTA-321':'SF6_INSULATED_SWITCH_VISTA-321',
#                        'VISTA-422':'SF6_INSULATED_SWITCH_VISTA-422','VISTA-431':'SF6_INSULATED_SWITCH_VISTA-431',
#                        '422':'SC_ELEC','431':'SC_ELEC','321':'SC_ELEC','G&W':'GW',
#                        'NET':'CARTE_ELEC_LTD'}
# 422/431/321 as VISTA switches
dictSGassetSubclass = {'PMH-3':'AIR_INSULATED_LIVEFRONT_PMH-9','PMH-5':'AIR_INSULATED_LIVEFRONT_PMH-9',
                       'PMH-9':'AIR_INSULATED_LIVEFRONT_PMH-9','PMH-11':'AIR_INSULATED_LIVEFRONT_PMH-11',
                       'PME-9':'AIR_INSULATED_DEADFRONT_PME-9','PME-10':'AIR_INSULATED_DEADFRONT_PME-9',
                       'PME-11':'AIR_INSULATED_DEADFRONT_PME-11','VISTA-321':'SF6_INSULATED_SWITCH_VISTA-321',
                       'VISTA-422':'SF6_INSULATED_SWITCH_VISTA-422','VISTA-431':'SF6_INSULATED_SWITCH_VISTA-431',
                       '422':'SF6_INSULATED_SWITCH_VISTA-422','431':'SF6_INSULATED_SWITCH_VISTA-431','321':'SF6_INSULATED_SWITCH_VISTA-321',
                       'G&W':'AIR_INSULATED_LIVEFRONT_PMH-11','NET':'CARTE_ELEC_LTD'}


#**************************
# Reading SwitchGears
#***************************
# Read Other Device Numbers into dataframes
with pd.ExcelFile(file_OtherDevices) as xls:
    dfSwitchGears = pd.read_excel(xls, 'SWITCHGEARS') # 280 rows

dropSGcols = ['Switch Gear', 'Adrs #','Location','City','Notes','To Type','Inst. Date','Mftr.','Catalog#','Serial#',
             'DOM','Comments']

dfSwitchGears = drop_columns(dfSwitchGears, dropSGcols)
#dfSwitchGears = dfSwitchGears.dropna() # drop all rows with NaN values

# 'Type' -> 'PMH'
# 'Loc_No' -> '149-S'
dfSwitchGears['Type'] = dfSwitchGears['Type'].fillna(method='ffill')
numSGrows = len(dfSwitchGears['Loc_No'])
dfSwitchGears['ASSET_SUBCLASS'] = new_columns(dfSwitchGears, numSGrows, 'ASSET_SUBCLASS')
dfSwitchGears =dfSwitchGears.astype(str)
#dfSwitchGears['Loc_No'] = dfSwitchGears.iloc[:,'Loc_No'].apply[s.lstrip("0") for s in listOfNum]
dfSwitchGears['Loc_No'] = [s.lstrip("0") for s in dfSwitchGears['Loc_No']]
dfSwitchGears['ASSET_SUBCLASS'] = dfSwitchGears['Type'].apply(lambda x: dictSGassetSubclass[x])

#*******************
# Drop columns
#*******************
dropSwitchesCols = ['ANCILLARYROLE','ENABLED','FEEDERINFO','ELECTRICTRACEWEIGHT','LOCATIONID','GPSDATE','LABELTEXT',
                    'OPERATINGVOLTAGE', 'NOMINALVOLTAGE', 'MAXOPERATINGVOLTAGE','MAXCONTINUOUSCURRENT','PRESENTPOSITION_R', 
                    'PRESENTPOSITION_Y', 'PRESENTPOSITION_B','NORMALPOSITION_R','NORMALPOSITION_Y','NORMALPOSITION_B', 
                    'SCADACONTROLID', 'SCADAMONITORID','PREFERREDCIRCUITSOURCE','TIESWITCHINDICATOR',
                    'GANGOPERATED', 'MANUALLYOPERATED','FEATURE_STATUS','HYPERLINK','HYPERLINK_PGDB','SYMBOLROTATION',
                    'INSULATOR_MATERIAL']

#******************************************************
# drop asset columns
#******************************************************
dfSwitches = drop_columns(dfSwitches,dropSwitchesCols)
#******************************************************
# FILTER OUT ASSET CLASSES WITH THEIR RESPECTIVE SUBTYPES
#******************************************************
# To avoid index vs copy error: pd.DataFrame...necessary (spent 4 hours getting rid of the warning error!)
# UG Switches rows
dfUGSwitches = dfSwitches[dfSwitches.SUBTYPECD == 6]
numSwitchRows = len(dfUGSwitches['DEVICENUMBER'])

#*******************
# ADD ADDITIONAL COLUMNS AND FILL WITH NaNs
#*******************
# UG Switches
dfUGSwitches['HI'] = new_columns(dfUGSwitches,numSwitchRows, 'HI')
dfUGSwitches['HI'] ='NA'
dfUGSwitches['TX_PHASE'] = new_columns(dfUGSwitches,numSwitchRows, 'TX_PHASE')
dfUGSwitches['IN_VALLEY'] = new_columns(dfUGSwitches,numSwitchRows, 'IN_VALLEY')
dfUGSwitches['IN_VALLEY'] = 'No'
dfUGSwitches['PRID'] = new_columns(dfUGSwitches,numSwitchRows, 'PRID')
dfTransformers['STATION'] = new_columns(dfTransformers, numTxRows,'STATION')
dfTransformers['STATION'] = 'NA'
dfTransformers['NEIGHBORHOOD_ID'] = new_columns(dfTransformers, numTxRows,'NEIGHBORHOOD_ID')
dfTransformers['NEIGHBORHOOD_ID'] = 'NA'
dfTransformers['CUSTOMER_COUNT'] = new_columns(dfTransformers, numTxRows,'CUSTOMER_COUNT')
dfTransformers['CUSTOMER_COUNT'] = 0
dfUGSwitches['TIE_FEEDER_PRID'] = new_columns(dfUGSwitches,numSwitchRows, 'TIE_FEEDER_PRID')
#**************************
# RENAME ASSET COLUMNS
#**************************
# Rename Switch columns
dfUGSwitches = dfUGSwitches.rename(columns={'SUBTYPECD':ASSET_CLASS,
                                        'DEVICENUMBER':'ID',
                                        'COMPATIBLEUNITID':ASSET_SUBCLASS,
                                        'PHASEDESIGNATION':'PHASING',
                                        'FEEDERID':'CIRCUIT', 
                                        'FEEDERID2':'TIE_FEEDER',
                                        'INSTALLATIONDATE':'INSTALL_YEAR'})
# Separate year
dfUGSwitches['INSTALL_YEAR'] = dfUGSwitches['INSTALL_YEAR'].apply(lambda x: x.year)

# Replace 'Asset Subclass' col with actual names
dfUGSwitches['ID'] = dfUGSwitches['ID'].astype(str)
dfUGSwitches=pd.merge(dfUGSwitches, dfSwitchGears, how='left', left_on='ID', right_on='Loc_No')
#dfSwitches['ID'] = dfSwitchGears['Loc_No'].apply(lambda x: )
#df.merge(df1, on='sku', how='left')
# print(len(pd.unique(dfSwitchGears['Loc_No'].values.ravel()))) # 111

# drop more columns
switchesDropMoreCols = [ASSET_SUBCLASS, 'Loc_No']
dfUGSwitches = dfUGSwitches.drop(switchesDropMoreCols, axis=1)
dfUGSwitches = dfUGSwitches.rename(columns={'ASSET_SUBCLASS': ASSET_SUBCLASS})

# Rename proper asset nomenclature
dfUGSwitches[ASSET_CLASS] = UG_SWITCHES_ASSET_CLASS

# Rename proper asset nomenclature
dfUGSwitches[ASSET_CLASS] = UG_SWITCHES_ASSET_CLASS

#phasingDict = {'1.0': '1Ph', '2.0':'1Ph','4.0':'1Ph','3.0':'2Ph','5.0':'2Ph','6.0':'2Ph','7.0':'3Ph'}
dfUGSwitches['PHASING'] = dfUGSwitches['PHASING'].astype(int)
dfUGSwitches['PHASING'] = dfUGSwitches['PHASING'].astype(str)
dfUGSwitches['PHASING'] = dfUGSwitches['PHASING'].apply(lambda x: phasingDict[x])

# Lower case column names
dfUGSwitches.columns = map(str.lower, dfUGSwitches.columns)

#******************************************************
# REARRANGE COLUMNS
#******************************************************
# *All tables need 'asset_id' - rename index
# UG Switches
# UG_SWITCHES_COLS =['asset_id','id','asset_subclass_code','asset_class_code','install_year','hi',
#                    'phasing','prid','circuit','tx_phase','in_valley','tie_feeder']
dfUGSwitches =dfUGSwitches[['id','asset_subclass_code','asset_class_code','install_year','hi','phasing','prid','circuit','tx_phase','in_valley',
                            'tie_feeder','tie_feeder_prid','type']]


#******************************************************
# OUTPUT DATAFRAMES TO EXCEL MODEL
#******************************************************
dfUGsw_excel = dfUGSwitches
# excel_dropUGsw = ['asset_subclass_code', 'fused','asset_class_code']
# dfUGsw_excel = drop_columns(dfUGsw_excel, excel_dropUGtx)
dfUGsw_excel['asset_class_code']='Switch Cubicle'
dfUGsw_excel = dfUGsw_excel.rename(columns={'asset_class_code':'class',
                                            'asset_subclass_code':'type'})

#*********************
# OUTPUT DATAFRAMES TO EXCEL FILES
#*********************
dfUGsw_later = dfUGSwitches
MasterFile = pd.ExcelWriter(UG_SWITCHES_TABLE_TEMPLATE)
dfUGsw_excel.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('UG Switches data munging completed')

#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# POLES
#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# keep only distribution poles
dfPoles = dfPoles[dfPoles.SUBTYPECD == 1] #1 - Dist(47%), 5-TrafficLights(2%), 7-streetlight(51%)

dropPolesCols = ['SYMBOLROTATION','GPSDATE','SUBTYPECD','LABELTEXT','STRUCTURENUMBER','FEATURE_STATUS',
                 'STREETLIGHT_FACILITY','REPLACED_DATE_MM_DD_YYYY','CONDITION','CONDITION_STATUS','CONDITION_DATE']
dfPoles = drop_columns(dfPoles,dropPolesCols)
#df.drop_duplicates(cols='A', take_last=True)
#dfPoles = dfPoles.drop_duplicates(cols='DEVICENUMBER', take_last=True)
dfPoles = dfPoles.drop_duplicates(['DEVICENUMBER'], take_last=True)
# Add additional columns and fill with NaNs
#dfPoles[''] = new_columns(dfPoles, numPolesRows,'')
numPolesRows = len(dfPoles['DEVICENUMBER'])
dfPoles[ASSET_CLASS] = new_columns(dfPoles, numPolesRows,ASSET_CLASS)
dfPoles[ASSET_SUBCLASS] = new_columns(dfPoles, numPolesRows,ASSET_SUBCLASS)
dfPoles['HI'] = new_columns(dfPoles, numPolesRows,'HI')
dfPoles['HI'] = 'NA'
dfPoles['PHASING'] = new_columns(dfPoles, numPolesRows,'PHASING')
dfPoles['PRID'] = new_columns(dfPoles, numPolesRows,'PRID')
dfPoles['TX'] = new_columns(dfPoles, numPolesRows,'TX')
dfPoles['TX_TYPE'] = new_columns(dfPoles, numPolesRows,'TX_TYPE')
dfPoles['CIRCUIT1'] = new_columns(dfPoles, numPolesRows,'CIRCUIT1')
dfPoles['CIRCUIT2'] = new_columns(dfPoles, numPolesRows,'CIRCUIT2')
dfPoles['CIRCUIT3'] = new_columns(dfPoles, numPolesRows,'CIRCUIT3')
dfPoles['CIRCUIT4'] = new_columns(dfPoles, numPolesRows,'CIRCUIT4')
dfPoles['CIRCUIT5'] = new_columns(dfPoles, numPolesRows,'CIRCUIT5')
dfPoles['CIRCUIT6'] = new_columns(dfPoles, numPolesRows,'CIRCUIT6')
dfPoles['CIRCUIT7'] = new_columns(dfPoles, numPolesRows,'CIRCUIT7')
dfPoles['CIRCUIT8'] = new_columns(dfPoles, numPolesRows,'CIRCUIT8')
dfPoles['IN_VALLEY'] = new_columns(dfPoles, numPolesRows,'IN_VALLEY')
dfPoles['TX_RESIDENTIAL'] = new_columns(dfPoles, numPolesRows,'TX_RESIDENTIAL')
dfPoles['TX_COMMERCIAL'] = new_columns(dfPoles, numPolesRows,'TX_COMMERCIAL')
dfPoles['TX_INDUSTRIAL'] = new_columns(dfPoles, numPolesRows,'TX_INDUSTRIAL')
#dfPoles['HEIGHT'] = new_columns(dfPoles, numPolesRows,'HEIGHT')
dfPoles['NUM_CIRCUITS'] = new_columns(dfPoles, numPolesRows,'NUM_CIRCUITS')
dfPoles['DEVICE'] = new_columns(dfPoles, numPolesRows,'DEVICE')
dfPoles['TX_KVA'] = new_columns(dfPoles, numPolesRows,'TX_KVA')
dfPoles['TX_PHASING'] = new_columns(dfPoles, numPolesRows,'TX_PHASING')

# Fill with values
dfPoles[ASSET_CLASS] = POLES_ASSET_CLASS
dfPoles[ASSET_SUBCLASS] = 'WOOD'

# Read domain codes for pole table into file
with pd.ExcelFile(file_DomainCodes_Poles) as xls:
    dfPolesClassHeight = pd.read_excel(xls, 'Sheet1') # 280 rows

# Merge tables
dfPoles = dfPoles.merge(dfPolesClassHeight, how='left', on='COMPATIBLEUNITID')

# Rename Pole columns
dfPoles = dfPoles.rename(columns={'DEVICENUMBER':'ID',
                                  'TYPE':'POLE_CLASS',
                                  'INSTALLATIONDATE':'INSTALL_YEAR'})
# Separate year
dfPoles['INSTALL_YEAR'] = dfPoles['INSTALL_YEAR'].apply(lambda x: x.year)

dropPolesCols2 = ['COMPATIBLEUNITID']
dfPoles = drop_columns(dfPoles, dropPolesCols2)
dfPoles = dfPoles[dfPoles.ID.notnull()] #drop null ids

# Lower case column names
dfPoles.columns = map(str.lower, dfPoles.columns)

#******************************************************
# REARRANGE COLUMNS
#******************************************************
# POLES_COLS = ['asset_id','asset_class_code','asset_subclass_code','install_year','hi character','phasing character',
#               'prid character','pole_class','tx','tx_type','circuit1','circuit2','circuit3','circuit4','in_valley',
#               'tx_residential','tx_commercial','tx_industrial','height','num_circuits','device','tx_kva','id','prid2',
#               'prid3','prid4','tx_pcb']

#******************************************************
# OUTPUT DATAFRAMES TO EXCEL MODEL
#******************************************************
# dfPoles_excel = dfPoles
# # excel_dropUGsw = ['asset_subclass_code', 'fused','asset_class_code']
# # dfUGsw_excel = drop_columns(dfUGsw_excel, excel_dropUGtx)
# dfPoles_excel['asset_class_code']='Switch Cubicle'
# dfPoles_excel = dfPoles_excel.rename(columns={'asset_class_code':'class',
#                                             'asset_subclass_code':'type'})


#*********************
# OUTPUT DATAFRAMES TO EXCEL FILES
#*********************
dfPoles_later = dfPoles
MasterFile = pd.ExcelWriter(POLES_TABLE_TEMPLATE)
dfPoles.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('Poles data munging completed')


#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# UNDERGROUND PRIMARY CABLES # dfPriUGV1
#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# dfPolesXY
# dfSwitchesXY
# dfPriUGXY
# dfPriOHXY
# dfTxXY

# dfOHtx_XY = dfOHtx_later
# dfUGtx_XY = dfUGtx_later 
# dfUGsw_XY = dfUGsw_later
# dfPoles_XY = dfPoles_later
# dfPriUG_XY = dfPriUG_later

#**********************************************************************************
#DELETE THIS WHEN COMBINING ALL ASSETS
#**********************************************************************************
# Cables

#***FROM HERE*****#
# dropCablesCols = ['ENABLED',  'FEEDERID2', 'FEEDERINFO', 'ELECTRICTRACEWEIGHT', 'LOCATIONID',
#                   'LENGTHSOURCE',  'LENGTHUOMCODE', 'LABELTEXT', 'OPERATINGVOLTAGE', 'NOMINALVOLTAGE', 
#                   'ISFEEDERTRUNK', 'NEUTRALUSECD', 'FEATURE_STATUS', 'CONDUCTOR_REJUVENATION']
# # drop columns not related to Tx
# dfPriUG = drop_columns(dfPriUG,dropCablesCols)

# # Add additional columns and fill with NaNs
# numCablesRows = len(dfPriUG['INSTALLATIONDATE'])

# #dfCables
# dfPriUG[ASSET_CLASS] = new_columns(dfPriUG, numCablesRows, ASSET_CLASS)
# dfPriUG[ASSET_SUBCLASS] = new_columns(dfPriUG, numCablesRows, ASSET_SUBCLASS)
# dfPriUG['HI'] = new_columns(dfPriUG,numCablesRows,'HI')
# dfPriUG['HI'] = 'NA'
# dfPriUG['PRID'] = new_columns(dfPriUG, numCablesRows,'PRID')
# dfPriUG['ARRANGEMENT'] = new_columns(dfPriUG, numCablesRows,'ARRANGEMENT')
# dfPriUG['INSTALLATION'] = new_columns(dfPriUG, numCablesRows,'INSTALLATION')
# dfPriUG['CONFIG'] = new_columns(dfPriUG, numCablesRows,'CONFIG')
# dfPriUG['NUM_SPLICES'] = new_columns(dfPriUG, numCablesRows,'NUM_SPLICES')
# dfPriUG['PRID_RESIDENTIAL'] = new_columns(dfPriUG, numCablesRows,'PRID_RESIDENTIAL')
# dfPriUG['PRID_COMMERCIAL'] = new_columns(dfPriUG, numCablesRows,'PRID_COMMERCIAL')
# dfPriUG['PRID_INDUSTRIAL'] = new_columns(dfPriUG, numCablesRows,'PRID_INDUSTRIAL')
# dfPriUG['WC_CATASTROPHIC_RES'] = new_columns(dfPriUG, numCablesRows,'WC_CATASTROPHIC_RES')
# dfPriUG['WC_CATASTROPHIC_COMM'] = new_columns(dfPriUG, numCablesRows,'WC_CATASTROPHIC_COMM')
# dfPriUG['WC_CATASTROPHIC_IND'] = new_columns(dfPriUG, numCablesRows,'WC_CATASTROPHIC_IND')
# dfPriUG['WC_REPLACEMENT'] = new_columns(dfPriUG, numCablesRows,'WC_REPLACEMENT')
# #dfPriUG['CABLE_PHASE'] = new_columns(dfPriUG, numCablesRows,'CABLE_PHASE')

# # Rename Cable columns
# dfPriUG = dfPriUG.rename(columns={'SHAPE_Length':'ID',
# 								  'SUBTYPECD':'PHASING',
# 								  'INSTALLATIONDATE':'INSTALL_YEAR',
# 								  'FEEDERID':'CIRCUIT',
# 								  'MEASUREDLENGTH':'LENGTH',
# 								  'WIRECOUNT': 'NUM_CABLES',
# 								  'PHASEDESIGNATION':'CABLE_PHASE'})

# #dfPriUG = dfPriUG[dfPriUG.INSTALL_YEAR.notnull()]
# #dfPriUG['INSTALL_YEAR'] = dfPriUG['INSTALL_YEAR'].astype(int)
# #print(dfPriUG.head(3))

# dictCablesPhasing = {'1':'1','2':'1','3':'1','4':'2','5':'3','6':'Abandon'}
# dictCablesPhase = {'0.0':'', '1.0':'B','2.0':'Y','3.0':'YB','4.0':'R','6.0':'RB','7.0':'RYB','':''}
# # Separate year
# dfPriUG['INSTALL_YEAR'] = dfPriUG['INSTALL_YEAR'].apply(lambda x: x.year)

# # Dropping cable rows:
# #drop NaN rows in dfPriUG['CABLE_PHASE'] #dfPriUG = dfPriUG[pd.notnull(dfPriUG['CABLE_PHASE'])]
# print('1. UG cable: ', dfPriUG.shape)
# dfPriUG = dfPriUG[dfPriUG.CABLE_PHASE.notnull()]
# print('2. UG cable(after Cable_phase not null) : ', dfPriUG.shape)
# dfPriUG = dfPriUG[dfPriUG.COMPATIBLEUNITID != 421] # Drop compatible unit id 421
# print('3. UG cable(after Compt unit not null) : ', dfPriUG.shape)
# dfPriUG = dfPriUG[dfPriUG.PHASING != 6] # drop 'Abandon' rows
# print('4. UG cable(after Phasing abandon removed) : ', dfPriUG.shape)
# dfPriUG = dfPriUG[dfPriUG.LENGTH.notnull()] # drop empty length rows
# print('5. UG cable(after Length not null) : ', dfPriUG.shape)
# dfPriUG = dfPriUG[dfPriUG.CIRCUIT != 'nan'] # drop empty length rows
# print('6. UG cable(after circuit not null) : ', dfPriUG.shape)

# dfPriUG['PHASING'] = dfPriUG['PHASING'].astype(str)
# dfPriUG['CABLE_PHASE'] = dfPriUG['CABLE_PHASE'].astype(str)

# #Try using .loc[row_indexer,col_indexer] = value instead
# dfPriUG.loc[:,'PHASING'] = dfPriUG['PHASING'].apply(lambda x: dictCablesPhasing[x])
# dfPriUG.loc[:,'CABLE_PHASE'] = dfPriUG['CABLE_PHASE'].apply(lambda x: dictCablesPhase[x])

# # Fill in Asset and asset subclass columns
# dfPriUG[ASSET_CLASS] = UG_PRI_CABLE_ASSET_CLASS
# xlpe = 'XLPLE'
# trxlpe = 'TRXLPE'
# cutOffYr_trxlpe = 1990
# dfPriUG[ASSET_SUBCLASS] = 'XLPE'
# print(dfPriUG.shape)
# #dfPriUG[ASSET_SUBCLASS] = dfPriUG['INSTALL_YEAR'].apply(lambda x: 'TRXLPE' if x >= 1990 else 'XLPE')
# #df.loc[(df["B"] > 50) & (df["C"] == 900), "A"]
# #dfPriUG.loc[(dfPriUG['INSTALL_YEAR'] >= 1990),'ASSET_SUBCLASS'] = 'TRXLPE'
# # Replace Asset class and 'SUBTYPECD' with actual tx types

# # Cables Domain code tables

# # Read Other Device Numbers into dataframes
# with pd.ExcelFile(file_DomainCodes_PriUG) as xls:
#     #dfTopology = pd.read_excel(xlsx, 'Topology', index_col=None, na_values=['NA']) # IGNORE for now
#     dfPriUGDomainCodes = pd.read_excel(xls, 'Sheet1')

# dfPriUG = dfPriUG.merge(dfPriUGDomainCodes, how='left', on='COMPATIBLEUNITID')
# #print(dfUGTransformers.head(2))
# dropCablesCols2 = ['COMPATIBLEUNITID','Description','Percent']
# dfPriUG = drop_columns(dfPriUG,dropCablesCols2)

# # Lower case column names
# dfPriUG.columns = map(str.lower, dfPriUG.columns)
# print('7. UG cable(template final) : ', dfPriUG.shape)
# MasterFile = pd.ExcelWriter(UG_PRI_CABLE_TABLE_TEMPLATE)
# dfPriUG.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# print('UG Primary Cable data munging completed')

#***FROM HERE*****#
#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# MACHINE LEARNING TO MAP INSTALLATION YEARS FOR UNDERGROWUND SWITCHES AND CABLES, POLES
#**************************************************************************************************************************************************************
#**************************************************************************************************************************************************************
# XY asset data
# dfPolesXY
# dfSwitchesXY
# dfPriUGXY
# dfPriOHXY
# dfTxXY

# dfOHtx_XY = dfOHtx_later
# dfUGtx_XY = dfUGtx_later 
# dfUGsw_XY = dfUGsw_later
# dfPoles_XY = dfPoles_later
# dfPriUG_XY = dfPriUG_later

#****************
# Transformers
#****************
#UG Tx: 2/3/5/7 - 1Ph/Ntwk/Sub/Pad 3Ph [1436,27,4,507: 1642 counts]
dfUGtx_XY = pd.DataFrame(dfTxXY[(dfTxXY.SUBTYPECD == 2) | 
                               (dfTxXY.SUBTYPECD == 3) |
                               (dfTxXY.SUBTYPECD == 5) |
                               (dfTxXY.SUBTYPECD == 7) ])

# OH Tx: 1/9/10 - 1Ph/3Ph/2Ph [1125/510/7: 1347 counts]
dfOHtx_XY = pd.DataFrame(dfTxXY[(dfTxXY.SUBTYPECD == 1) |
                       (dfTxXY.SUBTYPECD == 9) |
                       (dfTxXY.SUBTYPECD == 10)])

txXYDropCols = ['FID', 'OBJECTID', 'ANCILLARYR', 'ENABLED', 'WORKORDERI','FEEDERID','FIELDVERIF', 'COMMENTS','CREATIONUS', 'DATECREATE', 'LASTUSER',
                'DATEMODIFI','WORKREQUES', 'DESIGNID', 'WORKLOCATI', 'WMSID','WORKFLOWST', 'WORKFUNCTI', 'FEEDERINFO','ELECTRICTR', 'LOCATIONID', 'SYMBOLROTA', 
                'GPSDATE','GISONUMBER','GISOTYPENB', 'SUBTYPECD', 'LABELTEXT', 'COMPATIBLE', 'OWNERSHIP','PHASEDESIG','OPERATINGV', 'NOMINALVOL', 'GROUNDREAC', 
                'GROUNDRESI','MAGNETIZIN', 'MAGNETIZ_1', 'HIGHSIDEGR','HIGHSIDE_1', 'HIGHSIDEPR','LOCATIONTY', 'FAULTINDIC', 'COOLINGTYP', 'FEATURE_ST','KVA', 
                'UNITS','DEMAND_KVA', 'DEMAND_DAT', 'STREET_LIG', 'HIGHSIDECO','LOWSIDECON', 'LOWSIDEGRO', 'LOWSIDEVOL','LATITUDE', 'LONGITUDE','RATEDKVA', 
                'FeederID_1', 'EnergizedP', 'SourceCoun', 'Loop','FEEDERID2']
#Drop columns
dfOHtx_XY = drop_columns(dfOHtx_XY, txXYDropCols)
dfUGtx_XY = drop_columns(dfUGtx_XY, txXYDropCols)

#print(dfSwitchesXY.columns) # 'INSTALLATI','DEVICENUMB', 'x', 'y']
#print(dfTxXY.columns) # 'INSTALLATI','DEVICENUMB', 'x', 'y']
dfUGtx_XY = dfUGtx_XY.rename(columns={'INSTALLATI':'install_year', 'DEVICENUMB':'id'})
dfUGtx_XY['install_year'] = dfUGtx_XY['install_year'].apply(lambda x: x.year)


#******************************************************
# UG Tx - 1 tx missing installation years - use k-NN
#******************************************************
# separate empty and non-empty 'install_year' values
dfUGtx_XY_Train = dfUGtx_XY[dfUGtx_XY['install_year'].notnull()] 
dfUGtx_XY_Empty = dfUGtx_XY[dfUGtx_XY['install_year'].isnull()] 
#print(dfUGTxXY_Empty.shape)

# train the model
print('*****UG Transformer*****')
print('kNN coefficient: ',3)
print('Training number of rows: ',len(dfUGtx_XY_Train['install_year']))
print('Wrong installation year rows: ',len(dfUGtx_XY_Empty['install_year']))
dfUGtx_XY_Empty.loc[:,'install_year'] = nearest_neighbor(dfUGtx_XY_Train, 'x','y','install_year',3,dfUGtx_XY_Empty,'UG Tx')
dfUGtx_XY_new = pd.concat([dfUGtx_XY_Train,dfUGtx_XY_Empty])
# fill in empty values

# merge with original df
dfUGtx_later = drop_columns(dfUGtx_later,'install_year')
dfUGtx_later = dfUGtx_later.merge(dfUGtx_XY_new, how='left', on='id')
dfUGtx_later = drop_columns(dfUGtx_later,['x','y'])

dfUGtx_later = dfUGtx_later[dfUGtx_later['prid'].notnull()]
#
# There are about eight ug tx without prids, need to find the upstream device.
#
# Overwrite original UG Tx file
#dfOHTxLater = dfOHTransformers
MasterFile = pd.ExcelWriter(UG_TX_TABLE)
dfUGtx_later.to_excel(MasterFile, 'Sheet1')
MasterFile.save()

#****************
# UG Switches
#****************
# select only UG switches
dfUGsw_XY = dfSwitchesXY[dfSwitchesXY.SUBTYPECD == 6]

switchXYDropCols = ['FID', 'OBJECTID', 'ANCILLARYR', 'ENABLED', 'WORKORDERI','FIELDVERIF', 'COMMENTS', 'CREATIONUS', 'DATECREATE', 'LASTUSER','DATEMODIFI', 
                    'WORKREQUES', 'DESIGNID', 'WORKLOCATI','WMSID','WORKFLOWST', 'WORKFUNCTI',  'FEEDERINFO','ELECTRICTR', 'LOCATIONID', 'GPSDATE',
                    'GISONUMBER','GISOTYPENB','LABELTEXT', 'OWNERSHIP', 'PHASEDESIG','OPERATINGV', 'NOMINALVOL', 'MAXOPERATI', 'MAXCONTINU', 'PRESENTPOS', 
                    'PRESENTP_1','PRESENTP_2', 'NORMALPOSI', 'NORMALPO_1','NORMALPO_2','SCADACONTR', 'SCADAMONIT', 'PREFERREDC', 'TIESWITCHI', 'GANGOPERAT',
                    'MANUALLYOP','SourceCoun','Loop', 'Tie','COMPATIBLE','SUBTYPECD','FEEDERID', 'FEEDERID2','HYPERLINK','HYPERLINK_','INSULATOR_','SYMBOLROTA',
                    'FEATURE_ST', 'EnergizedP']

dfUGsw_XY = drop_columns(dfUGsw_XY, switchXYDropCols)
dfUGsw_XY = dfUGsw_XY.rename(columns={'INSTALLATI':'install_year','DEVICENUMB':'id'})
dfUGsw_XY['install_year'] = dfUGsw_XY['install_year'].apply(lambda x: x.year)

# make sure to have UG Switches only
# Machine Learning: empty and filled
#def nearest_neighbor(dfMain, trainX, trainY, classX, neighborCount, dfUnknown):
dfUGsw_XY_Unknown = dfUGsw_XY.loc[dfUGsw_XY['install_year'] == 1900]
dfUGsw_XY_Train = dfUGsw_XY.loc[dfUGsw_XY['install_year'] != 1900]

# combining UG Tx and UG SW with relatively correct installation years
# check prediction accuracy with UG tx removed
dfUGsw_XY_Train = pd.concat([dfUGtx_XY_new,dfUGsw_XY_Train]) #4093 rows
dfUGsw_XY_Train = dfUGsw_XY_Train[np.isfinite(dfUGsw_XY_Train['install_year'])] # drop NaNs
print('SW UG Tx train cols: ', dfUGsw_XY_Train.columns)
#********************************************

print('*****UG Switches*****')
print('kNN coefficient: ',1)
print('Training number of rows: ',len(dfUGsw_XY_Train['install_year']))
print('Wrong installation year rows: ',len(dfUGsw_XY_Unknown['install_year']))
dfUGsw_XY_Unknown.loc[:,'install_year'] = nearest_neighbor(dfUGsw_XY_Train, 'x','y','install_year',1, dfUGsw_XY_Unknown, 'UG Switches')
# 60% accuracy
dfUGsw_XY_Unknown = drop_columns(dfUGsw_XY_Unknown, ['x','y'])
dfUGsw_XY_Train = drop_columns(dfUGsw_XY_Train, ['x','y'])
dfSwitches_XY = pd.concat([dfUGsw_XY_Unknown,dfUGsw_XY_Train])

# # overwrite template file: Merge with NGN dfSwitches on Device
dfUGsw_later = dfUGSwitches
#print('dfUGSwLater: ', dfUGSwLater.columns)
dfUGsw_later = drop_columns(dfUGsw_later,['install_year'])
dfUGsw_later = dfUGsw_later.merge(dfSwitches_XY, how='left', on='id')

# Drop network switch rows and few more columns
dfUGsw_later = dfUGsw_later[dfUGsw_later.asset_subclass_code.notnull()]
dfUGsw_later = dfUGsw_later[dfUGsw_later.asset_subclass_code != 'CARTE_ELEC_LTD']
dfUGsw_later = drop_columns(dfUGsw_later, ['FeederID_1','type'])

MasterFile = pd.ExcelWriter(UG_SWITCHES_TABLE)
dfUGsw_later.to_excel(MasterFile, 'Sheet1')
MasterFile.save()


# Pole data hack
# with pd.ExcelFile('IN_POLES_TEMPLATE_former.xlsx') as xls:
#     #dfTopology = pd.read_excel(xlsx, 'Topology', index_col=None, na_values=['NA']) # IGNORE for now
#     dfPoles_hack = pd.read_excel(xls, 'Sheet1')

# dfPoles_hack = dfPoles_hack.drop_duplicates(subset='id')
# MasterFile = pd.ExcelWriter('POLES_JAN20.xlsx')
# dfPoles_hack.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()

#**********************************************************************
# UG Cables
#**********************************************************************
# dfCables age need to be fixed
# 60% cables installed in 1900 and 1998
# match with other 80%
#**********************************************************************
dropUGcableCols = ['FID', 'OBJECTID', 'ENABLED', 'WORKORDERI',  'FIELDVERIF','COMMENTS', 'CREATIONUS', 'DATECREATE','LASTUSER', 'DATEMODIFI','WORKREQUES', 
           'DESIGNID', 'WORKLOCATI', 'WMSID', 'WORKFLOWST','WORKFUNCTI','FEEDERID2', 'FEEDERINFO', 'ELECTRICTR','LOCATIONID', 'LENGTHSOUR','LENGTHUOMC',
           'GISONUMBER', 'GISOTYPENB', 'LABELTEXT','OWNERSHIP','OPERATINGV','NOMINALVOL', 'ISFEEDERTR','NEUTRALUSE', 'FEATURE_ST',
           'CONDUCTOR_','FeederID_1','EnergizedP', 'SourceCoun', 'Loop']

# drop columns not related to Tx
#print(dfPriUGXY.columns)
dfPriUG_XY = drop_columns(dfPriUGXY, dropUGcableCols)
# Add additional columns and fill with NaNs
numCablesRows = len(dfPriUGXY['INSTALLATI'])

#dfCables
#*************************
# dfPriUG_XY[ASSET_CLASS] = new_columns(dfPriUG_XY, numCablesRows, ASSET_CLASS)
# dfPriUG_XY[ASSET_SUBCLASS] = new_columns(dfPriUG_XY, numCablesRows, ASSET_SUBCLASS)
# dfPriUG_XY['HI'] = new_columns(dfPriUG_XY,numCablesRows,'HI')
# dfPriUG_XY['HI'] = 'NA'
# dfPriUG_XY['PRID'] = new_columns(dfPriUG_XY, numCablesRows,'PRID')
# dfPriUG_XY['ARRANGEMENT'] = new_columns(dfPriUG_XY, numCablesRows,'ARRANGEMENT')
# dfPriUG_XY['ARRANGEMENT'] = 'DB'
# dfPriUG_XY['INSTALLATION'] = new_columns(dfPriUG_XY, numCablesRows,'INSTALLATION')
# dfPriUG_XY['INSTALLATION'] = 'DB'
# dfPriUG_XY['CONFIG'] = new_columns(dfPriUG_XY, numCablesRows,'CONFIG')
# dfPriUG_XY['NUM_SPLICES'] = new_columns(dfPriUG_XY, numCablesRows,'NUM_SPLICES')
# dfPriUG_XY['PRID_RESIDENTIAL'] = new_columns(dfPriUG_XY, numCablesRows,'PRID_RESIDENTIAL')
# dfPriUG_XY['PRID_COMMERCIAL'] = new_columns(dfPriUG_XY, numCablesRows,'PRID_COMMERCIAL')
# dfPriUG_XY['PRID_INDUSTRIAL'] = new_columns(dfPriUG_XY, numCablesRows,'PRID_INDUSTRIAL')
# dfPriUG_XY['WC_CATASTROPHIC_RES'] = new_columns(dfPriUG_XY, numCablesRows,'WC_CATASTROPHIC_RES')
# dfPriUG_XY['WC_CATASTROPHIC_COMM'] = new_columns(dfPriUG_XY, numCablesRows,'WC_CATASTROPHIC_COMM')
# dfPriUG_XY['WC_CATASTROPHIC_IND'] = new_columns(dfPriUG_XY, numCablesRows,'WC_CATASTROPHIC_IND')
# dfPriUG_XY['WC_REPLACEMENT'] = new_columns(dfPriUG_XY, numCablesRows,'WC_REPLACEMENT')
#dfPriUG_XY['CABLE_PHASE'] = new_columns(dfPriUG_XY, numCablesRows,'CABLE_PHASE')
#*************************


#*******EXCEL MODEL******************
dfPriUG_XY[ASSET_CLASS] = new_columns(dfPriUG_XY, numCablesRows, ASSET_CLASS)
dfPriUG_XY[ASSET_SUBCLASS] = new_columns(dfPriUG_XY, numCablesRows, ASSET_SUBCLASS)
dfPriUG_XY['HI'] = new_columns(dfPriUG_XY,numCablesRows,'HI')
dfPriUG_XY['HI'] = 'N/A'
dfPriUG_XY['PRID'] = new_columns(dfPriUG_XY, numCablesRows,'PRID')
dfPriUG_XY['ARRANGEMENT'] = new_columns(dfPriUG_XY, numCablesRows,'ARRANGEMENT')
dfPriUG_XY['ARRANGEMENT'] = 'DB'
dfPriUG_XY['INSTALLATION'] = new_columns(dfPriUG_XY, numCablesRows,'INSTALLATION')
dfPriUG_XY['INSTALLATION'] = 'DB'
dfPriUG_XY['CONFIG'] = new_columns(dfPriUG_XY, numCablesRows,'CONFIG')
dfPriUG_XY['CONFIG'] = 'Radial'
dfPriUG_XY['NUM_SPLICES'] = new_columns(dfPriUG_XY, numCablesRows,'NUM_SPLICES')
dfPriUG_XY['NUM_SPLICES'] = 0
dfPriUG_XY['WC_REPLACEMENT'] = new_columns(dfPriUG_XY, numCablesRows,'WC_REPLACEMENT')
dfPriUG_XY['WC_REPLACEMENT'] = 0
#*new cols for excel model ***
#dfPriUG_XY['NOMINAL_VOLTAGE'] = new_columns(dfPriUG_XY, numCablesRows,'NOMINAL_VOLTAGE') #domain pri_ug table
dfPriUG_XY['WC_PRID_CATASTROPHIC_RES'] = new_columns(dfPriUG_XY, numCablesRows,'WC_PRID_CATASTROPHIC_RES')
dfPriUG_XY['WC_PRID_CATASTROPHIC_RES'] = 0
dfPriUG_XY['WC_PRID_CATASTROPHIC_IND'] = new_columns(dfPriUG_XY, numCablesRows,'WC_PRID_CATASTROPHIC_IND')
dfPriUG_XY['WC_PRID_CATASTROPHIC_IND'] = 0
dfPriUG_XY['WC_PRID_CATASTROPHIC_COMM'] = new_columns(dfPriUG_XY, numCablesRows,'WC_PRID_CATASTROPHIC_COMM')
dfPriUG_XY['WC_PRID_CATASTROPHIC_COMM'] = 0
dfPriUG_XY['WC_SWITCHING_RES'] = new_columns(dfPriUG_XY, numCablesRows,'WC_SWITCHING_RES')
dfPriUG_XY['WC_SWITCHING_RES'] = 0
dfPriUG_XY['WC_SWITCHING_COMM'] = new_columns(dfPriUG_XY, numCablesRows,'WC_SWITCHING_COMM')
dfPriUG_XY['WC_SWITCHING_COMM'] = 0
dfPriUG_XY['WC_SWITCHING_IND'] = new_columns(dfPriUG_XY, numCablesRows,'WC_SWITCHING_IND')
dfPriUG_XY['WC_SWITCHING_IND'] = 0
dfPriUG_XY['WC_SWITCHING_DURATION'] = new_columns(dfPriUG_XY, numCablesRows,'WC_SWITCHING_DURATION')
dfPriUG_XY['WC_SWITCHING_DURATION'] = 0
dfPriUG_XY['CABLE_TO_NETWORK'] = new_columns(dfPriUG_XY, numCablesRows,'CABLE_TO_NETWORK')
dfPriUG_XY['CABLE_TO_NETWORK'] = 'No'
dfPriUG_XY['INJECT_TYPE'] = new_columns(dfPriUG_XY, numCablesRows,'INJECT_TYPE')
dfPriUG_XY['INJECT_TYPE'] = 'N/A'
dfPriUG_XY['INJECTION_YEAR'] = new_columns(dfPriUG_XY, numCablesRows,'INJECTION_YEAR')
dfPriUG_XY['INJECTION_YEAR'] = 'N/A'
dfPriUG_XY['STATION'] = new_columns(dfPriUG_XY, numCablesRows,'STATION')
dfPriUG_XY['STATION'] = 'N/A'
dfPriUG_XY['NEIGHBORHOOD_ID'] = new_columns(dfPriUG_XY, numCablesRows,'NEIGHBORHOOD_ID')
dfPriUG_XY['NEIGHBORHOOD_ID'] = 'N/A'
dfPriUG_XY['INJECTABILITY'] = new_columns(dfPriUG_XY, numCablesRows,'INJECTABILITY')
dfPriUG_XY['INJECTABILITY'] = 'N/A'
dfPriUG_XY['CUSTOMER_COUNT'] = new_columns(dfPriUG_XY, numCablesRows,'CUSTOMER_COUNT')
dfPriUG_XY['CUSTOMER_COUNT'] = 0

#*********************ENDS

# Rename Cable columns
dfPriUG_XY = dfPriUG_XY.rename(columns={'SHAPE_LEN':'ID',
                                        'SUBTYPECD':'PHASING',
                                        'INSTALLATI':'INSTALL_YEAR',
                                        'FEEDERID':'CIRCUIT',
                                        'MEASUREDLE':'LENGTH',
                                        'WIRECOUNT': 'NUM_CABLES',
                                        'PHASEDESIG':'CABLE_PHASE',
                                        'COMPATIBLE':'COMPATIBLEUNITID'})

dictCablesPhasing = {'1':'1','2':'1','3':'1','4':'2','5':'3','6':'Abandon'}
#dictCablesPhase = {'0.0':'', '1.0':'B','2.0':'Y','3.0':'YB','4.0':'R','6.0':'RB','7.0':'RYB','':''}
dictCablesPhase_XY = {'0':'', '1':'B','2':'Y','3':'YB','4':'R','6':'RB','7':'RYB','':''}
# Separate year
dfPriUG_XY['INSTALL_YEAR'] = dfPriUG_XY['INSTALL_YEAR'].apply(lambda x: x.year)

# Dropping cable rows:
#drop NaN rows in dfPriUG_XY['CABLE_PHASE'] #dfPriUG_XY = dfPriUG_XY[pd.notnull(dfPriUG_XY['CABLE_PHASE'])]
dfPriUG_XY = dfPriUG_XY[dfPriUG_XY.CABLE_PHASE.notnull()]
dfPriUG_XY = dfPriUG_XY[dfPriUG_XY.COMPATIBLEUNITID != 421] # Drop compatible unit id 421
dfPriUG_XY = dfPriUG_XY[dfPriUG_XY.PHASING != 6] # drop 'Abandon' rows
dfPriUG_XY = dfPriUG_XY[dfPriUG_XY.LENGTH.notnull()] # drop empty length rows
dfPriUG_XY = dfPriUG_XY[dfPriUG_XY.CIRCUIT != 'nan'] # drop empty length rows

dfPriUG_XY['PHASING'] = dfPriUG_XY['PHASING'].astype(str)
dfPriUG_XY['CABLE_PHASE'] = dfPriUG_XY['CABLE_PHASE'].astype(str)

#Try using .loc[row_indexer,col_indexer] = value instead
dfPriUG_XY.loc[:,'PHASING'] = dfPriUG_XY['PHASING'].apply(lambda x: dictCablesPhasing[x])
dfPriUG_XY.loc[:,'CABLE_PHASE'] = dfPriUG_XY['CABLE_PHASE'].apply(lambda x: dictCablesPhase_XY[x])

# Fill in Asset and asset subclass columns
dfPriUG_XY[ASSET_CLASS] = UG_PRI_CABLE_ASSET_CLASS
xlpe = 'XLPLE'
trxlpe = 'TRXLPE'
cutOffYr_trxlpe = 1990
dfPriUG_XY[ASSET_SUBCLASS] = 'XLPE'
# dfPriUG_XY.loc[:, ASSET_SUBCLASS] = dfPriUG_XY['INSTALL_YEAR'].apply(lambda x: 'TRXLPE' if x >= 1990 else 'XLPE')

# Lower case column names
dfPriUG_XY.columns = map(str.lower, dfPriUG_XY.columns)
dfPriUG_XY = dfPriUG_XY.rename(columns ={'xstart': 'x', 'ystart':'y'})

#dfPriUG_XY_write = dfPriUG_XY
#dfPriUG_XY_write = drop_columns(dfPriUG_XY_write, ['x','y','xmid','ymid','xend','yend'])
# MasterFile = pd.ExcelWriter(UG_PRI_CABLE_TABLE_TEMPLATE)
# dfPriUG_XY.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# print('UG Primary Cable data munging completed')
# cableCutoffYr = 2002

# Machine Learning: empty and filled
#def nearest_neighbor(dfMain, trainX, trainY, classX, neighborCount, dfUnknown):
#print('Shape of dfCablesXY: ', dfCablesXY.shape)# (3888, 9)


# *********
# only four input training variables
# *********
# dfPriUG_XY_train = dfPriUG_XY[dfPriUG_XY.install_year.notnull()]
# dfPriUG_XY_train['install_year'] = dfPriUG_XY_train['install_year'].astype(int)
# dfPriUG_XY_unknown = dfPriUG_XY[dfPriUG_XY.install_year.isnull()]
# print('***************************************************')
# print('*****UG Cable: Install Year Prediction*****')
# print('kNN coefficient: ',3)
# print('Training number of rows: ',len(dfPriUG_XY_train['id']))
# print('Unknown number of install_year rows: ',len(dfPriUG_XY_unknown['id']))
#dfPriUG_XY_unknown.loc[:,'install_year'] = cable_nearest_neighbor(dfPriUG_XY_train, 'x','y','xend', 'yend', 'install_year',3,dfPriUG_XY_unknown,'UG Primary Cable')
# ends
# *********

# *********
# only two input training variables
# *********
cableCutoffYr = 2002
dfPriUG_XY_twoInputs = dfPriUG_XY[['x','y','install_year','id']]
dfPriUG_XY_unknown = dfPriUG_XY_twoInputs.loc[dfPriUG_XY_twoInputs['install_year'] < cableCutoffYr]
dfPriUG_XY_2002 = dfPriUG_XY_twoInputs.loc[dfPriUG_XY_twoInputs['install_year'] >= cableCutoffYr]
#print('Shape of dfCablesXY Unknown: ', dfCablesXY_Unknown.shape) #(3853, 9)
# combine both UG tx and cable installed after 2002
# earlier only UG tx was considered (hmm..)
dfPriUG_XY_train = pd.concat([dfUGtx_XY_new, dfPriUG_XY_2002])
#print('Shape of dfCablesXY_Train: ', dfCablesXY_Train.shape) #(1975, 4)
dfPriUG_XY_train = dfPriUG_XY_train[np.isfinite(dfPriUG_XY_train['install_year'])] #one NaN value
dfPriUG_XY_train['install_year'] = dfPriUG_XY_train['install_year'].astype(int)

print('**************************************** ***********')
print('*****UG Cable: Install Year Prediction*****')
print('kNN coefficient: ',3)
print('Training number of rows: ',len(dfPriUG_XY_train['id']))
print('Unknown number of install_year rows: ',len(dfPriUG_XY_unknown['id']))
dfPriUG_XY_unknown.loc[:,'install_year'] = nearest_neighbor(dfPriUG_XY_train, 'x','y','install_year',3,dfPriUG_XY_unknown,'UG Primary Cable')
# ends
# *********

# 4 input training variables
#dfPriUG_XY_install_year = pd.concat([dfPriUG_XY_train,dfPriUG_XY_unknown])
# 2 input training variables
dfPriUG_XY_ugTX_ugPRI = pd.concat([dfPriUG_XY_train,dfPriUG_XY_unknown])
print(dfPriUG_XY_ugTX_ugPRI.columns)
dfPriUG_XY = drop_columns(dfPriUG_XY, ['x','y','install_year'])
dfPriUG_XY_install_year = dfPriUG_XY.merge(dfPriUG_XY_ugTX_ugPRI, how='left', on='id')
print('NA in install_year? ',dfPriUG_XY_install_year['install_year'].isnull().values.any())
#print(dfPriUG_XY_install_year.columns)

with pd.ExcelFile(file_DomainCodes_PriUG) as xls:
    #dfTopology = pd.read_excel(xlsx, 'Topology', index_col=None, na_values=['NA']) # IGNORE for now
    dfPriUG_XYDomainCodes = pd.read_excel(xls, 'Sheet1')

#print(dfPriUG_XYDomainCodes.head())
#print(dfPriUG_XYDomainCodes.dtypes)

dfPriUG_XY_install_year['compatibleunitid'] = dfPriUG_XY_install_year['compatibleunitid'].astype(str)
dfPriUG_XYDomainCodes['compatibleunitid'] = dfPriUG_XYDomainCodes['compatibleunitid'].astype(str)

dfPriUG_XY_new = pd.merge(dfPriUG_XY_install_year, dfPriUG_XYDomainCodes, how='left', on='compatibleunitid')
#print(dfPriUG_XY_new.head())
#print(dfPriUG_XY_new.dtypes)

dropCablesCols2 = ['compatibleunitid','Percent', 'CNSHLD','Description']
dfPriUG_XY_new = drop_columns(dfPriUG_XY_new,dropCablesCols2)
#print(dfPriUG_XY_new.head())

dfPriUG_XY_new['x'] = dfPriUG_XY_new['x'].astype(str)
dfPriUG_XY_new['y'] = dfPriUG_XY_new['y'].astype(str)
dfPriUG_XY_new['xend'] = dfPriUG_XY_new['xend'].astype(str)
dfPriUG_XY_new['yend'] = dfPriUG_XY_new['yend'].astype(str)
dfPriUG_XY_new['id_xy1'] = dfPriUG_XY_new[['x','y']].apply(lambda x: '_'.join(x), axis=1)
dfPriUG_XY_new['id_xyEnd'] = dfPriUG_XY_new[['xend','yend']].apply(lambda x: '_'.join(x), axis=1)
dfPriUG_XY_new['id_xy'] = dfPriUG_XY_new[['id_xy1','id_xyEnd']].apply(lambda x: '-'.join(x), axis=1)

# TRXLPE
dfPriUG_XY_new = dfPriUG_XY_new[dfPriUG_XY_new.install_year.notnull()]
dfPriUG_XY_new['install_year'] = dfPriUG_XY_new['install_year'].astype(int)
dfPriUG_XY_new.loc[:, ASSET_SUBCLASS] = dfPriUG_XY_new['install_year'].apply(lambda x: 'TRXLPE' if x >= 1990 else 'XLPE')

dfPriUG_XY_write = dfPriUG_XY_new
dfPriUG_XY_write = drop_columns(dfPriUG_XY_write, ['x','y','xmid','ymid','xend','yend','id','id_xy1','id_xyEnd','id_xy'])

MasterFile = pd.ExcelWriter(UG_PRI_CABLE_TABLE_TEMPLATE)
dfPriUG_XY_write.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('UG Cable: Install Year prediction complete')

file_priUGcable_prid = 'Asset_XY_files/UG_CABLE_PRID.xlsx'
#Read xlsx file into dataframes
with pd.ExcelFile(file_priUGcable_prid) as xlsx:
    dfPriUGcablePRID = pd.read_excel(xlsx, 'Sheet1')
#print(dfPriUGcablePRID.head())
dfPriUGcablePRID.columns = map(str.lower, dfPriUGcablePRID.columns)
#print(dfPriUGcablePRID.dtypes)

dfPriUGcablePRID_train = dfPriUGcablePRID[dfPriUGcablePRID.prid.notnull()]
dfPriUGcablePRID_unknown = dfPriUGcablePRID[dfPriUGcablePRID.prid.isnull()]

# train the model
print('***************************************************')
print('*****UG Cable: PRID Prediction*****')
print('kNN coefficient: ',3)
print('Training number of rows: ',len(dfPriUGcablePRID_train['id']))
print('Unknown number of PRID rows: ',len(dfPriUGcablePRID_unknown['id']))
dfPriUGcablePRID_unknown.loc[:,'prid'] = cable_nearest_neighbor(
                                          dfPriUGcablePRID_train, 'x','y','xend', 'yend', 'prid',3,dfPriUGcablePRID_unknown,'UG Primary Cable')
dfPriUGcablePRID_new = pd.concat([dfPriUGcablePRID_train,dfPriUGcablePRID_unknown])
# Write into the UG cable asset table
dfPriUGcablePRID_new = drop_columns(dfPriUGcablePRID_new, ['x', 'y','xend','yend'])
dfPriUG_XY_new = drop_columns(dfPriUG_XY_new, ['prid','id'])

# dfPriUG_XY_new['x'] = dfPriUG_XY_new['x'].astype(str)
# dfPriUG_XY_new['y'] = dfPriUG_XY_new['y'].astype(str)
# dfPriUG_XY_new['id_xy'] = dfPriUG_XY_new[['x','y']].apply(lambda x: '_'.join(x), axis=1)

dfPriUG_XY_new = pd.merge(dfPriUG_XY_new,dfPriUGcablePRID_new, how='left', left_on='id_xy', right_on='id')

dfPriUG_XY_new = drop_columns(dfPriUG_XY_new, ['x','y','xmid','ymid','xend','yend','id_xy','id','id_xy1','id_xyEnd'])

MasterFile = pd.ExcelWriter(UG_PRI_CABLE_TABLE)
dfPriUG_XY_new.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('UG Cable: Install Year prediction complete')

#ID  INSTALL_YEAR  HI  INSULATION  CLASS PHASING PRID  CIRCUIT ARRANGEMENT INSTALLATION  MATERIAL  CABLE_SIZE  CONFIG  LENGTH  NUM_SPLICES NUM_CABLES  NOMINAL_VOLTAGE WC_PRID_CATASTROPHIC_RES  WC_PRID_CATASTROPHIC_COMM WC_PRID_CATASTROPHIC_IND  CABLE_PHASE WC_REPLACEMENT  WC_SWITCHING_RES  WC_SWITCHING_COMM WC_SWITCHING_IND  WC_SWITCHING_DURATION CABLE_TO_NETWORK  INJECT_TYPE INJECTION_YEAR  STATION NEIGHBORHOOD_ID INJECTABILITY CUSTOMER_COUNT

# config  num_splices  cable_size  material  cnshld  nominal_voltage

#*****************************************************************************************************
# ML to resolve UG Primary Cable unknown PRID
#*****************************************************************************************************
#nearest_neighbor(df_filled, 'x','y','OH_FEEDERID',3,df_empty)

# file_priUGcable_prid = 'Asset_XY_files/UG_CABLE_PRID.xlsx'
# #Read xlsx file into dataframes
# with pd.ExcelFile(file_priUGcable_prid) as xlsx:
#     dfPriUGcablePRID = pd.read_excel(xlsx, 'Sheet1')

# dfPriUGcablePRID.columns = map(str.lower, dfPriUGcablePRID.columns)

# dfPriUGcablePRID_train = dfPriUGcablePRID[dfPriUGcablePRID.prid.notnull()]
# dfPriUGcablePRID_unknown = dfPriUGcablePRID[dfPriUGcablePRID.prid.isnull()]

# # train the model
# print('***************************************************')
# print('*****UG Cable: PRID Prediction*****')
# print('kNN coefficient: ',3)
# print('Training number of rows: ',len(dfPriUGcablePRID_train['id']))
# print('Unknown number of PRID rows: ',len(dfPriUGcablePRID_unknown['id']))
# dfPriUGcablePRID_unknown.loc[:,'prid'] = cable_nearest_neighbor(
#                                           dfPriUGcablePRID_train, 'x','y','xend', 'yend', 'prid',3,dfPriUGcablePRID_unknown,'UG Primary Cable')
# dfPriUGcablePRID_new = pd.concat([dfPriUGcablePRID_train,dfPriUGcablePRID_unknown])
# # Write into the UG cable asset table
# dfPriUGcablePRID_new = drop_columns(dfPriUGcablePRID_new, ['x', 'y','xend','yend'])
# dfPriUG_XY = drop_columns(dfPriUG_XY, 'prid')
# dfPriUG_XY = pd.merge(dfPriUG_XY,dfPriUGcablePRID_new, how='left', on='id')

# MasterFile = pd.ExcelWriter(UG_PRI_CABLE_TABLE_TEMPLATE)
# dfPriUG_XY.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
print('ML Cables analysis for PRIDs completed')

#*****************************************************************************************************
# ML to resolve UG Primary Cable unknown PRID
#*****************************************************************************************************

# PriUGXYDropCols = ['FID', 'OBJECTID', 'ENABLED', 'WORKORDERI',  'FIELDVERIF','COMMENTS', 'CREATIONUS', 'DATECREATE','LASTUSER', 'DATEMODIFI','WORKREQUES', 
# 				   'DESIGNID', 'WORKLOCATI', 'WMSID', 'WORKFLOWST','WORKFUNCTI','FEEDERID2', 'FEEDERINFO', 'ELECTRICTR','LOCATIONID', 'LENGTHSOUR', 
# 				   'MEASUREDLE', 'LENGTHUOMC','WIRECOUNT','GISONUMBER', 'GISOTYPENB', 'LABELTEXT', 'COMPATIBLE','OWNERSHIP','PHASEDESIG', 'OPERATINGV', 
# 				   'NOMINALVOL', 'ISFEEDERTR','NEUTRALUSE', 'FEATURE_ST', 'CONDUCTOR_','SHAPE_LEN', 'FeederID_1','EnergizedP', 'SourceCoun', 'Loop']

# dfPriUG_XY = drop_columns(dfPriUG_XY, PriUGXYDropCols)
# dfPriUG_XY = dfPriUG_XY.rename(columns={'xStart': 'x','yStart': 'y','INSTALLATI':'install_year'})

# # use UG tx to train and test, fill cable where years <=2002
# cableCutoffYr = 2002

# #df[~df.C.str.contains("XYZ")] # Remove all 'abandon' phasing
# #dfCablesXY = dfCablesXY[dfCablesXY.SUBTYPECD != 6]
# dfPriUG_XY['install_year'] = dfPriUG_XY['install_year'].apply(lambda x: x.year)

# # Machine Learning: empty and filled
# #def nearest_neighbor(dfMain, trainX, trainY, classX, neighborCount, dfUnknown):
# #print('Shape of dfCablesXY: ', dfCablesXY.shape)# (3888, 9)
# dfPriUG_XY_Unknown = dfPriUG_XY.loc[dfPriUG_XY['install_year'] < cableCutoffYr]
# dfPriUG_XY_2002 = dfPriUG_XY.loc[dfPriUG_XY['install_year'] >= cableCutoffYr]
# #print('Shape of dfCablesXY Unknown: ', dfCablesXY_Unknown.shape) #(3853, 9)

# # combine both UG tx and cable installed after 2002
# # earlier only UG tx was considered (hmm..)
# dfPriUG_XY_Train = pd.concat([dfUGtx_XY_new, dfPriUG_XY_2002])
# #print('Shape of dfCablesXY_Train: ', dfCablesXY_Train.shape) #(1975, 4)
# # print('Before Year NaNs: ', dfCablesXY_Train.shape)
# dfPriUG_XY_Train = dfPriUG_XY_Train[np.isfinite(dfPriUG_XY_Train['install_year'])] #one NaN value
# # print('After Year NaNs: ', dfCablesXY_Train.shape)

# # if combined both UGtx and UGCable > 2002 ~ 45-50% prediction accuracy
# # dfCablesXY_Train = dfCablesXY.loc[dfCablesXY['install_year'] == cableCutoffYr]
# # dfCablesXY_Train = pd.concat([dfUGTxXY,dfCablesXY_Train]) #4093 rows
# # dfCablesXY_Train = dfCablesXY_Train[np.isfinite(dfCablesXY_Train['install_year'])] # drop NaNs
# #dfCablesXY_Train = dfCablesXY_Train[np.isfinite(dfCablesXY_Train['FEEDERID'])] # drop NaNs, mostly 'Abandon' phasing

# print('*****Primary Cable*****')
# print('kNN coefficient: ',3)
# print('Training number of rows: ',len(dfPriUG_XY_Train['install_year']))
# print('Wrong installation year rows: ',len(dfPriUG_XY_Unknown['install_year']))
# dfPriUG_XY_Unknown.loc[:,'install_year'] = nearest_neighbor(dfPriUG_XY_Train, 'x','y','install_year',3,dfPriUG_XY_Unknown, 'UG Primary Cable')
# # 60% accuracy

# # cablesXYdropCol = ['xEnd','yEnd','xMid','yMid','SUBTYPECD']
# # dfCablesXY_Unknown = drop_columns(dfCablesXY_Unknown, cablesXYdropCol)
# # MasterFile = pd.ExcelWriter('V6.1Cables_test.xlsx')
# # dfCablesXY_Unknown.to_excel(MasterFile, 'Sheet1')
# # MasterFile.save()
# # uncomment if UGCable included in training set
# # dfCablesXY_Train = drop_columns(dfCablesXY_Train, cablesXYdropCol)

# dfPriUG_XY_all = pd.concat([dfPriUG_XY_Unknown,dfPriUG_XY_2002])
# print(dfPriUG_XY_all.shape)
# print(dfPriUG_XY_all.columns)
# #print(dfCablesXY_all.head(4)) # FEEDERID   id  install_year          x   y

# #dfPriUG_XY_uniqueX = pd.DataFrame(pd.unique(dfPriUG_XY_all[['x']].values.ravel()))
# #print("all: ",dfCablesXY_all.shape)

# dfPriUG_later_XY = dfPriUG

# #dfPriUG_later_XY['x'] = new_columns(dfPriUG_later_XY,numCablesRows,'x')
# #print('After: ',dfCablesLater.columns)

# #print('1:',dfCablesLater.shape) #(3865, 27) | (7869, 50) only if both UGTx and UG cable joined - not recommended
# # print(dfCablesXY.shape) # (3888, 8) (3750, 9)
# #dfPriUG_later_XY['x']= dfPriUG_XY_uniqueX[0].apply(lambda x: x)
# #'install_year', 'FEEDERID', 'SUBTYPECD', 'x', 'y', 'xMid', 'yMid', 'xEnd', 'yEnd'

# #******
# # comment out for Excel model purposes
# #******
# #dfPriUG_XY_all = drop_columns(dfPriUG_XY_all, ['xMid', 'yMid', 'xEnd', 'yEnd','SUBTYPECD'])
# dfPriUG_XY_all = drop_columns(dfPriUG_XY_all, ['xMid', 'yMid', 'SUBTYPECD'])
# #******
# dfPriUG_later_XY = dfPriUG_later_XY.merge(dfPriUG_XY_all, how='left', on='x')
# #dfPriUG_later_XY = dfPriUG_later_XY.drop_duplicates(['x'], take_last=True)

# #used for finding cable installation years with poles in CYME node
# # dfPriUG_later_XY = dfPriUG_later
# # dfPriUG_later_XY = drop_columns(dfPriUG_later_XY,['install_year_x', 'x','FEEDERID','y'])
# # dfPriUG_later_XY = dfPriUG_later_XY.rename(columns = {'install_year_y': 'install_year'})

# #Final cleanup
# #Final data cleanup
# dfPriUG_later_XY = dfPriUG_later_XY[dfPriUG_later_XY.phasing != 'Abandon']
# dfPriUG_later_XY = dfPriUG_later_XY[dfPriUG_later_XY.circuit != 'nan']
# dfPriUG_later_XY = dfPriUG_later_XY[dfPriUG_later_XY.length.notnull()]
# dfPriUG_later_XY = dfPriUG_later_XY[dfPriUG_later_XY.install_year.notnull()]
# #******
# # comment out for Excel model purposes
# #*******
# #dfPriUG_later_XY = drop_columns(dfPriUG_later_XY,['install_year_x', 'x','FEEDERID','y'])
# dfPriUG_later_XY = drop_columns(dfPriUG_later_XY,['install_year_x','FEEDERID'])

# dfPriUG_later_XY['id'] = np_concat(dfPriUG_later_XY['x'],dfPriUG_later_XY['y'],dfPriUG_later_XY['xEnd'],dfPriUG_later_XY['yEnd'])

# #******
# dfPriUG_later_XY = dfPriUG_later_XY.rename(columns = {'install_year_y': 'install_year'})


# #print(dfPriUG_later_XY.columns)

# # dfPriUG_later = dfPriUG_later[np.isfinite(dfPriUG_later['install_year'])] #one blank value
# #print('After duplicate:',dfCablesLater.shape)
# #print(dfCablesXY.columns)
# MasterFile = pd.ExcelWriter(UG_PRI_CABLE_TABLE)
# dfPriUG_later_XY.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# print('ML Cables analysis completed')
# # print('Before:', dfCablesLatLongV1.shape) # Before: (3888, 50)
# # dfCablesLatLongV1 = dfCablesLatLongV1.drop_duplicates(['xStart'], take_last=True)
# # print('After:', dfCablesLatLongV1.shape) # After: (3188, 50)

# # **********************************************************************
# # Poles Match with installation years - over 54% installed 97-2000
# #**********************************************************************

# #******************************************************
# # OH Tx - 3 tx missing installation years - use k-NN
# #******************************************************
# # separate empty and non-empty 'install_year' values
# dfOHtx_XY = dfOHtx_XY.rename(columns={'INSTALLATI':'install_year', 'DEVICENUMB':'id'})
# dfOHtx_XY['install_year'] = dfOHtx_XY['install_year'].apply(lambda x: x.year)
# dfOHtx_XY_Train = dfOHtx_XY[dfOHtx_XY['install_year'].notnull()] 
# dfOHtx_XY_Empty = dfOHtx_XY[dfOHtx_XY['install_year'].isnull()] 

# print('*****OH Tx*****')
# print('kNN coefficient: ',3)
# print('Training OH Tx rows: ',len(dfOHtx_XY_Train['install_year']))
# print('Null OH Tx rows: ',len(dfOHtx_XY_Empty['install_year']))
# # train the model

# dfOHtx_XY_Empty.loc[:,'install_year'] = nearest_neighbor(dfOHtx_XY_Train, 'x','y','install_year',3,dfOHtx_XY_Empty,'OH Tx')
# dfOHtx_XY_New = pd.concat([dfOHtx_XY_Train,dfOHtx_XY_Empty])
# # fill in empty values

# # merge with original df
# dfOHtx_later = drop_columns(dfOHtx_later,'install_year')
# dfOHtx_later = dfOHtx_later.merge(dfOHtx_XY_New, how='left', on='id')
# dfOHtx_later = drop_columns(dfOHtx_later,['x','y'])

# #**********************************************************************
# # Match poles with OH Tx
# #**********************************************************************
# polesXYDropCols = ['FID', 'OBJECTID', 'WORKORDERI','FIELDVERIF', 'COMMENTS','CREATIONUS', 'DATECREATE', 'LASTUSER', 'DATEMODIFI', 'WORKREQUES','DESIGNID', 
# 				   'WORKLOCATI', 'WMSID','WORKFLOWST', 'WORKFUNCTI','SYMBOLROTA', 'GPSDATE', 'GISONUMBER', 'GISOTYPENB', 'SUBTYPECD','LABELTEXT', 'OWNERSHIP', 
# 				   'COMPATIBLE', 'STRUCTUREN', 'FEATURE_ST','STREETLIGH', 'REPLACED_D','CONDITION', 'CONDITION_','CONDITION1']

# dfPolesXY = drop_columns(dfPolesXY, polesXYDropCols)
# dfPolesXY = dfPolesXY.rename(columns={'DEVICENUMB': 'id','INSTALLATI':'install_year'})
# #dfOHTxXY = dfOHTxXY.rename(columns={'DEVICENUMB': 'tx','INSTALLATI':'install_year'})
# dfPolesXY = dfPolesXY.drop_duplicates(['id'], take_last=True)
# dfPolesXY_later = dfPolesXY

# dfPolesXY = dfPolesXY[dfPolesXY.id.notnull()]
# dfPolesXY['install_year'] = dfPolesXY['install_year'].apply(lambda x: x.year)

# #df = df[(df.one > 0) | (df.two > 0) | (df.three > 0) & (df.four < 1)]
# dfPolesXY_Unknown = dfPolesXY.loc[(dfPolesXY.install_year == 1997) |
#                                   (dfPolesXY.install_year == 1998) |
#                                   (dfPolesXY.install_year == 1999) |
#                                   (dfPolesXY.install_year == 2000) |
#                                   (dfPolesXY.install_year.isnull())]

# #print(dfPolesXY_Unknown.shape) #4771, 4

# dfPolesXY_Train = dfOHtx_XY_New

# # check why NaNs exist here
# dfPolesXY_Train = dfPolesXY_Train[np.isfinite(dfPolesXY_Train['install_year'])] # drop NaNs

# print('*****POLES*****')
# print('kNN coefficient: ',3)
# print('Training Poles rows: ',len(dfPolesXY_Train['install_year']))
# print('Wrong Poles rows: ',len(dfPolesXY_Unknown['install_year']))
# dfPolesXY_Unknown.loc[:,'install_year'] = nearest_neighbor(dfPolesXY_Train, 'x','y','install_year',3, dfPolesXY_Unknown, 'Poles')

# dfPolesXY_Unknown = drop_columns(dfPolesXY_Unknown, ['x','y'])
# dfPolesXY_All = dfPoles.merge(dfPolesXY_Unknown, how='left', on='id', suffixes=('_all', '_uk'))
# dfPolesXY_All['install_year'] = dfPolesXY_All['install_year_uk'].where(dfPolesXY_All['install_year_uk']> 0,
#                                                                      dfPolesXY_All['install_year_all'])
# dfPolesXY_All = drop_columns(dfPolesXY_All, ['install_year_uk','install_year_all'])
# # # 40% accuracy

# # Overwrite original OH Tx file
# #dfOHTxLater = dfOHTransformers
# MasterFile = pd.ExcelWriter(OH_TX_TABLE_TEMPLATE)
# dfOHtx_later.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()

# #dfPolesXY_YY = dfPolesXY_All
# # Overwrite original pole template file?
# OH_trained_Poles = 'V1_OH_trained_Poles.xlsx'
# MasterFile = pd.ExcelWriter(OH_trained_Poles)
# dfPolesXY_All.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# print('Pole installation year matching analysis with OH Tx completed')




#*****************************************************************************************************
# January 19 2016: ML to find first circuit for Poles
#*****************************************************************************************************

# PriOHXY_dropCols = ['FID','OBJECTID','ENABLED','WORKORDERI','INSTALLATI','FIELDVERIF','COMMENTS','CREATIONUS','DATECREATE','LASTUSER','DATEMODIFI',
# 					'WORKREQUES','DESIGNID','WORKLOCATI','WMSID','WORKFLOWST','WORKFUNCTI','FEEDERID2','FEEDERINFO','ELECTRICTR','LOCATIONID','LENGTHSOUR',
# 					'MEASUREDLE','LENGTHUOMC','WIRECOUNT','GISONUMBER','GISOTYPENB','SUBTYPECD','LABELTEXT','COMPATIBLE','OWNERSHIP','PHASEDESIG','OPERATINGV',
# 					'NOMINALVOL','ISFEEDERTR','NEUTRALUSE','PHASECONFI','CLEARANCE','FEATURE_ST','TL_DESIGNA','SHAPE_LEN','FeederID_1','EnergizedP',
# 					'SourceCoun','Loop', 'xMid','yMid']

# dfPriOHXY = drop_columns(dfPriOHXY, PriOHXY_dropCols)

# # might be an overkill - used dropna :)
# def drop_nan(nan_col):
# 	# return nan_col.notnull()
# 	return np.isfinite(nan_col)

# # FEEDERID xStart xEnd	yStart yEnd
# # Take xStart, yStart; xMid, yMid, xEnd, yEnd
# #dfPriOHXY= drop_nan(dfPriOHXY['xStart'])
# dfPriOHXY.dropna()

# dfPriOHXY = dfPriOHXY[dfPriOHXY['xStart'].notnull()]
# dfPriOHXY = dfPriOHXY[dfPriOHXY['yStart'].notnull()]
# dfPriOHXY = dfPriOHXY[dfPriOHXY['xEnd'].notnull()]
# dfPriOHXY = dfPriOHXY[dfPriOHXY['yEnd'].notnull()]
# dfPriOHXY = dfPriOHXY[dfPriOHXY['FEEDERID'].notnull()]

# dfPriOHXY['xyStart'] = np_concat(dfPriOHXY['xStart'], dfPriOHXY['yStart'])
# dfPriOHXY['xyEnd'] = np_concat(dfPriOHXY['xEnd'], dfPriOHXY['yEnd'])
# # print('dfPriOHXY cols: ', dfPriOHXY.columns)
# dfPoles_XY_OHcond = dfPolesXY_later
# # print(dfPoles_XY_OHcond.columns) #['install_year', 'id', 'x', 'y']
# dfPoles_XY_OHcond['xy'] = np_concat(dfPoles_XY_OHcond['x'],dfPoles_XY_OHcond['y'])

# #dfPoles_XY_OHcond['x'] = dfPoles_XY_OHcond['x'].astype(str)
# #dfPoles_XY_OHcond['y'] = dfPoles_XY_OHcond['y'].astype(str)
# #dfPoles_XY_OHcond['xy'] = dfPoles_XY_OHcond[['x','y']].apply(lambda x: '_'.join(x), axis=1)

# dfPoles_XY_OHcond = drop_columns(dfPoles_XY_OHcond, ['install_year','x','y'])
# # 1. Match just xStart_yStart with Poles
# # print('dfPoles_XY_OHcond cols 1 :', dfPoles_XY_OHcond.columns)
# dfPolesOHcond = dfPoles_XY_OHcond.merge(dfPriOHXY, how='left', left_on='xy', right_on='xyStart')

# # print('dfPolesOHcond cols: 2', dfPolesOHcond.columns)
# dfPoles_XY_OHcond_matched_xyStart = dfPolesOHcond[dfPolesOHcond.FEEDERID.notnull()]
# # print('dfPoles_XY_OHcond_matched_xyStart cols: 1', dfPoles_XY_OHcond_matched_xyStart.columns)
# # 2. Isolate remaining unmatched ones to match with xEnd_yEnd
# dfPoles_XY_OHcond_xyEnd = dfPolesOHcond[dfPolesOHcond.FEEDERID.isnull()]
# # print('dfPoles_XY_OHcond_xyEnd cols: 1', dfPoles_XY_OHcond_xyEnd.columns)
# # drop cols
# OHcond_XY_dropCols = ['xStart', 'yStart','xEnd', 'yEnd','FEEDERID','xyStart']
# dfPoles_XY_OHcond_xyEnd = drop_columns(dfPoles_XY_OHcond_xyEnd, OHcond_XY_dropCols)
# # print('dfPoles_XY_OHcond_xyEnd cols: 2', dfPoles_XY_OHcond_xyEnd.columns)
# # print('dfPolesOHcond cols:', dfPolesOHcond.columns)
# print('dfPoles_XY_OHcond_xyEnd cols:', dfPoles_XY_OHcond_xyEnd.columns)

# # 3. Use ML for remaining unmatched ones
# dfPoles_XY_OHcond_xyEnd = dfPoles_XY_OHcond_xyEnd.merge(dfPriOHXY, how='left', left_on='xy', right_on='xyEnd')
# dfPoles_XY_OHcond_xyEnd = drop_columns(dfPoles_XY_OHcond_xyEnd, ['xyEnd_x','xyEnd_y','xStart', 'yStart'])
# # dfPoles_XY_OHcond_xyEnd = dfPoles_XY_OHcond_xyEnd.rename(columns={'xyEnd_y':'xyEnd'})
# print('dfPoles_XY_OHcond_xyEnd cols (after merge):', dfPoles_XY_OHcond_xyEnd.columns)
# dfPoles_XY_OHcond_matched_xyEnd = dfPoles_XY_OHcond_xyEnd[dfPoles_XY_OHcond_xyEnd.FEEDERID.notnull()]

# # df.drop_duplicates(cols='A', take_last=True)
# # df.drop_duplicates(subset=['A', 'C'], keep=False) # False removes all duplicates
# # 4. Concat two completed df. Becomes training set
# dfPoles_XY_OHcond_train = pd.concat([dfPoles_XY_OHcond_matched_xyStart, dfPoles_XY_OHcond_matched_xyEnd])
# dfPoles_XY_OHcond_train = dfPoles_XY_OHcond_train.drop_duplicates('id')
# dfPoles_XY_OHcond_unMatched = dfPoles_XY_OHcond_xyEnd[dfPoles_XY_OHcond_xyEnd.FEEDERID.isnull()]
# dfPoles_XY_OHcond_unMatched = dfPoles_XY_OHcond_unMatched.drop_duplicates('id')

# dfPoles_XY_OHcond_unMatched['xStart'], dfPoles_XY_OHcond_unMatched['yStart'] = zip(*dfPoles_XY_OHcond_unMatched['xy'].apply(lambda x: x.split('_')))
# dfPoles_XY_OHcond_unMatched['xStart'] = dfPoles_XY_OHcond_unMatched['xStart'].astype(float)
# dfPoles_XY_OHcond_unMatched['yStart'] = dfPoles_XY_OHcond_unMatched['yStart'].astype(float)
# dfPoles_XY_OHcond_train['FEEDERID'] = dfPoles_XY_OHcond_train['FEEDERID'].astype(str)
# dfPoles_XY_OHcond_unMatched['FEEDERID'] = dfPoles_XY_OHcond_unMatched['FEEDERID'].astype(str)

# # dfAllNodes_list['NodeID_x'], dfAllNodes_list['NodeID_y'] = zip(*dfAllNodes_list['xy'].
# #                                                                apply(lambda x: x.split('_') if '_' in x else (x, np.nan)))
# # 5. kNN to complete other missing set
# dfPoles_XY_OHcond_unMatched
# print('*****POLES*****')
# print('kNN coefficient: ',3)
# print('Training number of rows: ',len(dfPoles_XY_OHcond_train['xy']))
# print('Unknown number of PRID rows: ',len(dfPoles_XY_OHcond_unMatched['xy']))
# #print(dfPoles_XY_OHcond_train.dtypes)
# #print(dfPoles_XY_OHcond_unMatched.dtypes)
# print(dfPoles_XY_OHcond_train.shape) # 6781,9
# print(dfPoles_XY_OHcond_unMatched.shape) # 2024,8
# dfPoles_XY_OHcond_train = drop_columns(dfPoles_XY_OHcond_train, ['xEnd', 'xy', 'yEnd', 'xyStart', 'xyEnd'])
# dfPoles_XY_OHcond_unMatched = drop_columns(dfPoles_XY_OHcond_unMatched, ['xEnd', 'xy', 'yEnd', 'xyStart'])
# dfPoles_XY_OHcond_unMatched['FEEDERID'] = ''
# # remaining cols: 'FEEDERID', 'id', 'xStart','yStart'
# print(dfPoles_XY_OHcond_train.shape) # 6781,4
# print(dfPoles_XY_OHcond_unMatched.shape) # 2024,4
# dfPoles_XY_OHcond_unMatched.loc[:,'FEEDERID'] = nearest_neighbor(dfPoles_XY_OHcond_train,'xStart','yStart','FEEDERID',3,dfPoles_XY_OHcond_unMatched,'Poles')
# #nearest_neighbor(df_filled, 'x','y','OH_FEEDERID',3,df_empty)
# #def nearest_neighbor(dfMain, trainX, trainY, classX, neighborCount, dfUnknown, AssetClass):
# dfPoles_XY_OHcond_completed = pd.concat([dfPoles_XY_OHcond_train,dfPoles_XY_OHcond_unMatched])
# #dfPoles_XY_OHcond_completed = dfPoles_XY_OHcond_completed.drop_duplicates('id')
# print(dfPoles_XY_OHcond_completed.shape)

# MasterFile = pd.ExcelWriter('POLES_TABLE_FINAL_ML.xlsx')
# #dfPoles_XY_OHcond_completed.to_excel(MasterFile,'Sheet1')
# dfPoles_XY_OHcond_train.to_excel(MasterFile,'Sheet1')
# dfPoles_XY_OHcond_unMatched.to_excel(MasterFile,'Sheet2')
# dfPoles_XY_OHcond_completed.to_excel(MasterFile,'Sheet3')
# MasterFile.save()
# print('Here we go!')

# #*****************************************************************************************************
# # Cell # 6 : Read all CYME feeders to populate dfAllNodes df - tie Poles with respective feeder ids
# #*****************************************************************************************************
# # fileName - iterate through entire folder :)
# #fileName = '3S3-1_Crestwood_Feeder_Details.xlsx'
# #input directory
# inputDirectory = 'Metsco_Feeder_Reports'

# # define filepath and sort the file list
# filesList = glob(os.path.join(inputDirectory, '*.xlsx'))
# numFiles = len(filesList)
# sortedFileList = sorted(filesList)

# # variables
# dictFeeders = {}
# dfAllNodes_list = pd.DataFrame()

# # read text files in tweet_input directory
# for f in sortedFileList:

#     fileName = os.path.basename(f).split('_')
#     FeederKey = fileName[0]
#     #print(FeederKey)
    
#     if ('$' not in FeederKey):
#         # Read CYME Feeder xlsx file into dataframes
#         with pd.ExcelFile(f) as xlsx:
#             #dfTopology = pd.read_excel(xlsx, 'Topology', index_col=None, na_values=['NA']) # IGNORE for now
#             dfTopology = pd.read_excel(xlsx, 'Topology') # 280 rows
#             dfSpotLoads = pd.read_excel(xlsx, 'Spot Loads') # Tot:239 - R/Y/B: 116/108/103 values; based on phases
#             dfLoads = pd.read_excel(xlsx, 'Loads') # 239 rows; 'Spot Number\n' col contains unique tx ids
#             dfCables = pd.read_excel(xlsx, 'Cables')
#             dfSwitches = pd.read_excel(xlsx, 'Switches') # 41 items
#             dfNodes = pd.read_excel(xlsx, 'Nodes') # 249 items
#             dfOHlines = pd.read_excel(xlsx, 'OverheadLinesByPhase') #Neutral - 94, Section Id - 381
#             dfFuses = pd.read_excel(xlsx, 'Fuses') # 44 items

#             # # Strip '\n' from column headers
#             dfTopology.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfSpotLoads.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfLoads.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfCables.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfSwitches.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfNodes.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfOHlines.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             dfFuses.rename(columns=lambda x: x.replace('\n',''), inplace=True)
#             #print(dfNodes.columns)
#             #dfAllNodes_list = dfAllNodes_list.append(dfOHlines)
#             dfAllNodes_list = dfAllNodes_list.append(dfNodes)

# print('Number of Feeders: ', numFiles)


# #*****************************************************************************************************
# # Cell # 7: Finding circuits: For both poles and UG Cables by matching with all nodes 
# #*****************************************************************************************************
# # dfOHtx_XY
# # dfOHtx_later
# # dfUGtx_later
# # dfOHtx_XY
# # dfPoles_later = dfPoles

# from collections import defaultdict

# #line 1092
# dfPoles_XY = dfPolesXY_later

# dfAllNodes_list = dfAllNodes_list.rename(columns={'Network Id': 'CIRCUIT',
#                                                   'Node Id': 'xy'})

# dfAllNodes_list['NodeID_x'], dfAllNodes_list['NodeID_y'] = zip(*dfAllNodes_list['xy'].
#                                                                apply(lambda x: x.split('_') if '_' in x else (x, np.nan)))

# # Convert circuit ids, fuse ids, switch ids and/or drop them
# #dfAllNodes_list['NodeID_x'] = dfAllNodes_list['NodeID_x'].astype(float)
# dfAllNodes_list.loc[:,'NodeID_x'] = dfAllNodes_list.loc[:,'NodeID_x'].convert_objects(convert_numeric=True)
# dfAllNodes_list.loc[:,'NodeID_y'] = dfAllNodes_list.loc[:,'NodeID_y'].convert_objects(convert_numeric=True)

# dfAllNodes_list = dfAllNodes_list[dfAllNodes_list.NodeID_x.notnull()]
# #print(dfAllNodes_XY_remain.isnull().sum())
# dfAllNodes_list = dfAllNodes_list[dfAllNodes_list.NodeID_y.notnull()]

# # dfPoles.columns = map(str.lower, dfPoles.columns)
# # polesLatLongDropCols = ['FID', 'OBJECTID', 'WORKORDERI', 'INSTALLATI', 'FIELDVERIF', 'COMMENTS','CREATIONUS', 
# #                         'DATECREATE', 'LASTUSER', 'DATEMODIFI', 'WORKREQUES','DESIGNID', 'WORKLOCATI', 'WMSID', 
# #                         'WORKFLOWST', 'WORKFUNCTI','SYMBOLROTA', 'GPSDATE', 'GISONUMBER', 'GISOTYPENB', 'SUBTYPECD',
# #                         'LABELTEXT', 'OWNERSHIP', 'COMPATIBLE', 'STRUCTUREN', 'FEATURE_ST','STREETLIGH', 'REPLACED_D', 
# #                         'CONDITION', 'CONDITION_','CONDITION1']
# # dfPoles_XY = drop_columns(dfPoles_XY, polesLatLongDropCols)
# # dfPoles_XY = dfPoles_XY.rename(columns={'DEVICENUMB': 'POLE_ID'})
# # dropMoreLatLongCols =['x','y']
# # dropMoreWireLatLongCols =['xStart','yStart','xMid','yMid','xEnd', 'yEnd']

# dfPoleIDs = dfPoles_XY['id']
# dictPoleIDs = defaultdict(list)

# xDelta = 5
# yDelta = 5

# for poleID, Px, Py in zip(dfPoles_XY['id'],dfPoles_XY['x'],dfPoles_XY['y']):
#     for circuitID, Nx, Ny in zip(dfAllNodes_list['CIRCUIT'],dfAllNodes_list['NodeID_x'],dfAllNodes_list['NodeID_y']):
#         if(abs(Px-Nx) < xDelta and abs(Py-Ny) < yDelta):
#             if circuitID not in dictPoleIDs[poleID]:
#                 dictPoleIDs[poleID].append(circuitID)

# dfPolesNodes = pd.DataFrame.from_dict(dictPoleIDs, orient='index')

# #df.reset_index(level=0, inplace=True)
# dfPolesNodes.reset_index(level=0, inplace=True)
# dfPolesNodes = dfPolesNodes.rename(columns={0:'CIRCUIT1', 
#                                             1:'CIRCUIT2',
#                                             2:'CIRCUIT3',
#                                             'index':'POLE_ID'})
# #print(dfPolesNodes.columns) #['POLE_ID', 'CIRCUIT1', 'CIRCUIT2', 'CIRCUIT3']

# MasterFile = pd.ExcelWriter('V1_PolesNodes.xlsx')
# dfPolesNodes.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# #print('Pole Nodes')

# #dfPolesXY_All = dfPolesXY_All.merge(dfPolesNodes, how='left', left_on='id', right_on='POLE_ID')
# dfPolesXY_All = dfPolesXY_All.merge(dfPolesNodes, how='left', left_on='id', right_on='POLE_ID')
# #print(dfPolesXY_All.columns)

# #MasterFile = pd.ExcelWriter(POLES_TABLE_TEMPLATE)
# Poles_XY_All_Nodes = 'V1_Poles_XY_All_Nodes.xlsx'
# MasterFile = pd.ExcelWriter(Poles_XY_All_Nodes)
# dfPolesXY_All.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# print('Pole installation year matching analysis with nodes completed')



# # *******************************************************************************************************************************************************
# # *******************************************************************************************************************************************************
# # *******************************************************************************************************************************************************

