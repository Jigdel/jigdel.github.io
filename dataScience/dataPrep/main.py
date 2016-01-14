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
UG_PRI_CABLE_ASSET_CLASS = 'UG_CABLE'
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
file_PRID_Tx = 'V5_PRID_TX_LOOKUP.xlsx'

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

#*****************************************************************************************************
# Cell # 2: Switches and Transformers
#*****************************************************************************************************
#******************************************************
# ASSET CLASS SPECIFIC DICTIONARIES
#******************************************************
# OPERATING VOLTAGE 190=8kv, 250=13.8kv, 1267 = 0kv, 1237 = 138kv
# Assets: Transformers,
operatingVoltageDict = {'190':'8000','250':'13800','1267':'0','1237':'138000'}

# Phasing change - need to change it to 'str' type, int/float dict key lookup doesn't work
# Assets: UG Switches, Transformers
#phasingDict = {'1.0': '1Ph', '2.0':'1Ph','4.0':'1Ph','3.0':'2Ph','5.0':'2Ph','6.0':'2Ph','7.0':'3Ph'}
phasingDict = {'1': '1', '2':'1','4':'1','3':'2','5':'2','6':'2','7':'3'}

# UG Switches
dictSGassetSubclass = {'PMH-3':'AIR_INSULATED_LIVEFRONT_PMH-9','PMH-5':'AIR_INSULATED_LIVEFRONT_PMH-9',
                       'PMH-9':'AIR_INSULATED_LIVEFRONT_PMH-9','PMH-11':'AIR_INSULATED_LIVEFRONT_PMH-11',
                       'PME-9':'AIR_INSULATED_DEADFRONT_PME-9','PME-10':'AIR_INSULATED_DEADFRONT_PME-9',
                       'PME-11':'AIR_INSULATED_DEADFRONT_PME-11','VISTA-321':'SF6_INSULATED_SWITCH_VISTA-321',
                       'VISTA-422':'SF6_INSULATED_SWITCH_VISTA-422','VISTA-431':'SF6_INSULATED_SWITCH_VISTA-431',
                       '422':'SC_ELEC','431':'SC_ELEC','321':'SC_ELEC','G&W':'GW',
                       'NET':'CARTE_ELEC_LTD'}

# Transformers
# dictOHTxSubclass = {'1':'Standard 1Ph','9':'Standard 3Ph','10':'Standard 2Ph'}
# dictUGTxSubclass = {'2':'Padmount 1Ph','3':'Network Submersible','5':'Submersible', '7':'Padmount 3Ph'}
dictOHTxSubclass = {'1':'POLE_TOP','9':'POLE_TOP','10':'POLE_TOP'}
dictUGTxSubclass = {'2':'PAD_MOUNTED','3':'NETWORK_SUBMERSIBLE','5':'SUBMERSIBLE', '7':'PAD_MOUNTED'}

#****************************************************************************
# UG Switches - Reading SwitchGears
#****************************************************************************
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
dfUGSwitches['TX_PHASE'] = new_columns(dfUGSwitches,numSwitchRows, 'TX_PHASE')
dfUGSwitches['IN_VALLEY'] = new_columns(dfUGSwitches,numSwitchRows, 'IN_VALLEY')
dfUGSwitches['PRID'] = new_columns(dfUGSwitches,numSwitchRows, 'PRID')
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

#******************************************************
switchesDropMoreCols = [ASSET_SUBCLASS, 'Loc_No']
dfUGSwitches = dfUGSwitches.drop(switchesDropMoreCols, axis=1)
dfUGSwitches = dfUGSwitches.rename(columns={'ASSET_SUBCLASS': ASSET_SUBCLASS})

#******************************************************
# Rename proper asset nomenclature
dfUGSwitches[ASSET_CLASS] = UG_SWITCHES_ASSET_CLASS

#******************************************************
# Rename proper asset nomenclature
dfUGSwitches[ASSET_CLASS] = UG_SWITCHES_ASSET_CLASS

#******************************************************
#phasingDict = {'1.0': '1Ph', '2.0':'1Ph','4.0':'1Ph','3.0':'2Ph','5.0':'2Ph','6.0':'2Ph','7.0':'3Ph'}
# UG Switches - 'phasing' col
dfUGSwitches['PHASING'] = dfUGSwitches['PHASING'].astype(int)
dfUGSwitches['PHASING'] = dfUGSwitches['PHASING'].astype(str)
dfUGSwitches['PHASING'] = dfUGSwitches['PHASING'].apply(lambda x: phasingDict[x])

#******************************************************
# Lower case column names
dfUGSwitches.columns = map(str.lower, dfUGSwitches.columns)

#******************************************************
# REARRANGE COLUMNS
#******************************************************
# *All tables need 'asset_id' - rename index
# UG Switches
# UG_SWITCHES_COLS =['asset_id','id','asset_subclass_code','asset_class_code','install_year','hi',
#                    'phasing','prid','circuit','tx_phase','in_valley','tie_feeder']
dfUGSwitches =dfUGSwitches[['id','asset_subclass_code','asset_class_code','install_year','hi','phasing','prid','circuit','tx_phase','in_valley','tie_feeder','type']]

#*********************
# OUTPUT DATAFRAMES TO EXCEL FILES
#*********************
# Output table/file names
# UG SWITCH
dfUGSwLater = dfSwitches
MasterFile = pd.ExcelWriter(UG_SWITCHES_TABLE_TEMPLATE)
dfUGSwitches.to_excel(MasterFile, 'Sheet1')
MasterFile.save()

#********************
# Drop columns
#*******************

dropTxCols = ['ANCILLARYROLE', 'ENABLED', 'FEEDERID2', 'FEEDERINFO', 'ELECTRICTRACEWEIGHT', 'LOCATIONID', 'SYMBOLROTATION', 
              'GPSDATE', 'LABELTEXT', 'NOMINALVOLTAGE', 'GROUNDREACTANCE', 'GROUNDRESISTANCE', 
              'MAGNETIZINGREACTANCE', 'MAGNETIZINGRESISTANCE', 'HIGHSIDEGROUNDREACTANCE','HIGHSIDEGROUNDRESISTANCE', 
              'HIGHSIDEPROTECTION', 'LOCATIONTYPE','COOLINGTYPE', 'FEATURE_STATUS','KVA', 'DEMAND_KVA',
              'DEMAND_DATE_MM_DD_YYYY', 'STREET_LIGHT_FACILITY', 'HIGHSIDECONFIGURATION', 'LOWSIDECONFIGURATION',
              'LOWSIDEGROUNDRESISTANCE', 'LOWSIDEVOLTAGE', 'LATITUDE', 'LONGITUDE']

#******************************************************
# drop asset columns
#******************************************************
dfTransformers = drop_columns(dfTransformers,dropTxCols)

#******************************************************
# FILTER OUT ASSET CLASSES WITH THEIR RESPECTIVE SUBTYPES
#******************************************************
# To avoid index vs copy error: pd.DataFrame...necessary (spent 4 hours getting rid of the warning error!)
# number of rows/observations 
numTxRows = len(dfTransformers['DEVICENUMBER'])

#******************************************************
# RENAME ASSET COLUMNS
#******************************************************

# Rename Transformer columns
dfTransformers = dfTransformers.rename(columns={'DEVICENUMBER':'ID',
                                                'PHASEDESIGNATION':'Type',
                                                'INSTALLATIONDATE':'INSTALL_YEAR',
                                                'FEEDERID':'CIRCUIT',
                                                'RATEDKVA':'KVA'})

# Separate year
dfTransformers['INSTALL_YEAR'] = dfTransformers['INSTALL_YEAR'].apply(lambda x: x.year)
dfTransformers = dfTransformers[dfTransformers['KVA'] >= 5]
#******************************************************
# ADD ADDITIONAL COLUMNS AND FILL WITH NaNs
#******************************************************

# Transformers
dfTransformers[ASSET_CLASS] = new_columns(dfTransformers, numTxRows, ASSET_CLASS)
dfTransformers['DEVICE_RESIDENTIAL'] = new_columns(dfTransformers, numTxRows,'DEVICE_RESIDENTIAL')
dfTransformers['DEVICE_COMMERCIAL'] = new_columns(dfTransformers, numTxRows,'DEVICE_COMMERCIAL')
dfTransformers['DEVICE_INDUSTRIAL'] = new_columns(dfTransformers, numTxRows,'DEVICE_INDUSTRIAL')
dfTransformers['UPSTREAM_DEVICE'] = new_columns(dfTransformers, numTxRows,'UPSTREAM_DEVICE')
dfTransformers['HI'] = new_columns(dfTransformers, numTxRows,'HI')
dfTransformers['HI'] = 'NA'
dfTransformers['PRID'] = new_columns(dfTransformers, numTxRows,'PRID')
dfTransformers['IN_VALLEY'] = new_columns(dfTransformers, numTxRows,'IN_VALLEY')
dfTransformers['IN_VALLEY'] = 'NA'
dfTransformers['PCB'] = new_columns(dfTransformers, numTxRows,'PCB')
dfTransformers['PCB'] = 51 #worst case scenario
dfTransformers['TX_RESIDENTIAL'] = new_columns(dfTransformers, numTxRows,'TX_RESIDENTIAL')
dfTransformers['TX_COMMERCIAL'] = new_columns(dfTransformers, numTxRows,'TX_COMMERCIAL')
dfTransformers['TX_INDUSTRIAL'] = new_columns(dfTransformers, numTxRows,'TX_INDUSTRIAL')

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

#******************************************************
# TRANSFORMERS
#******************************************************
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



#PRID Tx

# with pd.ExcelFile(file_PRID_Tx) as xls:
#     dfPRIDtx = pd.read_excel(xls, 'Sheet1')

# #remove the column and rename it in near future
# dfPRIDtx = dfPRIDtx.rename(columns={'transformerid':'id'})
# #dfPRIDtx = drop_columns(dfPRIDtx, ['TransformerID_x', 'TransformerID_y'])

# dfPRID_OHtx = dfOHTxLater
# dfPRID_UGtx = dfUGTxLater
# dfPRID_OHtx = drop_columns(dfPRID_OHtx,['prid'])
# dfPRID_UGtx = drop_columns(dfPRID_UGtx,['prid'])

# dfPRID_OHtx = dfPRID_OHtx.merge(dfPRIDtx, how='left', on='id')
# dfPRID_UGtx = dfPRID_UGtx.merge(dfPRIDtx, how='left', on='id')

# #PRIDdropCols = ['tx_residential','tx_commercial','tx_industrial']
# PRIDdropCols = [RES_LOAD,MED_COM_LOAD,LARGE_LOAD]

# dfPRID_OHtx = drop_columns(dfPRID_OHtx, PRIDdropCols)

# # dfPRID_OHtx = dfPRID_OHtx.rename(columns={RES_LOAD:'tx_residential',
# #                                           MED_COM_LOAD:'tx_med_com_load',
# #                                           LARGE_LOAD:'tx_large_commercial_load',
# #                                           'PRID':'prid'})

# #'secondary_voltage','fused','banking'

# dfPRID_OHtx['kva'] = dfPRID_OHtx['kva'].astype(float)
# dfPRID_UGtx['kva'] = dfPRID_UGtx['kva'].astype(float)
# dfPRID_OHtx['phasing'] = dfPRID_OHtx['phasing'].astype(float)
# dfPRID_UGtx['phasing'] = dfPRID_UGtx['phasing'].astype(float)

# def phasing_kva(phasing,kva,custClass):
#     if((kva > 350) & (custClass=='classLarge')):
#         return kva/2
#     elif((phasing == 3) & (kva <=350) & (custClass=='classMed')):
#         return kva/2
#     elif((phasing != 3) & (kva <=150) & (custClass=='classRx')):
#         return kva/2
#     else:
#         return 0
# # def valuation_formula(x, y):
# #     return x * y * 0.5
# #df['price'] = df.apply(lambda row: valuation_formula(row['x'], row['y']), axis=1)

# dfPRID_OHtx['tx_residential'] = dfPRID_OHtx.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classRx'), axis=1)
# dfPRID_OHtx['tx_commercial'] = dfPRID_OHtx.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classMed'), axis=1)
# dfPRID_OHtx['tx_industrial'] = dfPRID_OHtx.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classLarge'), axis=1)

# dfPRID_UGtx['tx_residential'] = dfPRID_UGtx.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classRx'), axis=1)
# dfPRID_UGtx['tx_commercial'] = dfPRID_UGtx.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classMed'), axis=1)
# dfPRID_UGtx['tx_industrial'] = dfPRID_UGtx.apply(lambda row: phasing_kva( row['phasing'],row['kva'], 'classLarge'), axis=1)

# # for index, row in dfPRID_OHtx.iterrows():
# #     row['tx_residential'] = phasing_kva(row['phasing'],row['kva'])

# #device_residential-device_commercial-device_industrial upstream_device prid
# dfPRID_OHtx['in_valley'] = 'No'
# dfPRID_OHtx['pcb'] ='refer Eval data'
# dfPRID_OHtx['hi'] = 'NA'
# dfPRID_OHtx.index.name = 'asset_id'
# dfPRID_OHtx = dfPRID_OHtx[['asset_class_code','id','circuit','install_year','asset_subclass_code','hi','phasing',
#                            'primary_voltage','kva','tx_residential','tx_commercial','tx_industrial','device_residential',
#                            'device_commercial','device_industrial','upstream_device','prid','in_valley','pcb','banking',
#                            'secondary_voltage','fused']]

# MasterFile = pd.ExcelWriter(OH_TX_TABLE_TEMPLATE)
# dfPRID_OHtx.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()

# dfPRID_UGtx = drop_columns(dfPRID_UGtx, PRIDdropCols)

# #device_residential-device_commercial-device_industrial upstream_device prid
# dfPRID_UGtx['pedestal'] = 'NA'
# dfPRID_UGtx['pcb'] ='refer Eval data'
# dfPRID_UGtx['switch_type'] = 'NA'
# dfPRID_UGtx['hi'] = 'NA'
# dfPRID_UGtx['switch_type'] = 'NA'
# dfPRID_UGtx['switchable'] = 'NA'
# dfPRID_UGtx.index.name = 'asset_id'

# dfPRID_UGtx = dfPRID_UGtx[['asset_subclass_code','asset_class_code','install_year','hi','phasing','prid','circuit',
#                            'primary_voltage','kva','tx_residential','tx_commercial','tx_industrial','device_residential',
#                            'device_commercial','device_industrial','upstream_device','pcb','pedestal','switchable',
#                            'switch_type','id','secondary_voltage','fused','banking']]

# dfPRID_UGtx = dfPRID_UGtx[dfPRID_UGtx['asset_subclass_code'] !='NETWORK_SUBMERSIBLE']

# dfUGTransformers = dfUGTransformers[dfUGTransformers['asset_subclass_code'] != 'NETWORK_SUBMERSIBLE']

# dfOHTransformers.index.name = 'asset_id'
# dfUGTransformers.index.name = 'asset_id'

# MasterFile = pd.ExcelWriter(UG_TX_TABLE_TEMPLATE)
# dfPRID_UGtx.to_excel(MasterFile, 'Sheet1')
# MasterFile.save()
# print('UG and OH Tx PRIDs matched and loading types classified')


# #Here

#******************************************************
# REARRANGE COLUMNS
#******************************************************
# *All tables need 'asset_id' - rename index
dfOHTransformers = dfOHTransformers[['asset_class_code','id','circuit','install_year','asset_subclass_code','hi','phasing',
                                     'primary_voltage','kva','tx_residential','tx_commercial','tx_industrial',
                                     'device_residential','device_commercial','device_industrial','upstream_device',
                                     'prid','in_valley','pcb','banking','secondary_voltage','fused']]
#'faultindicator','type','units','tx_type_counts','sec_voltage','fused'

dfUGTransformers = dfUGTransformers[['asset_subclass_code','asset_class_code','install_year','hi','phasing','prid','circuit',
                                     'primary_voltage','kva','in_valley','tx_residential','tx_commercial','tx_industrial',
                                     'device_residential','device_commercial','device_industrial','upstream_device','pcb',
                                     'pedestal','switchable','switch_type','id','secondary_voltage','fused','banking']]

#******************************************************
# OUTPUT DATAFRAMES TO EXCEL FILES
#******************************************************
# OH TX
dfOHTxLater = dfOHTransformers
MasterFile = pd.ExcelWriter(OH_TX_TABLE_TEMPLATE)
dfOHTransformers.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
# UG TX
dfUGTxLater = dfUGTransformers
MasterFile = pd.ExcelWriter(UG_TX_TABLE_TEMPLATE)
dfUGTransformers.to_excel(MasterFile, 'Sheet1')
MasterFile.save()
print('OH and UG Tx, UG Switches analyses completed')