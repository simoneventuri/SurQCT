import time
import os
import shutil
import sys
import h5py
import tensorflow                             as tf
import numpy                                  as np
import seaborn                                as sns
import pandas                                 as pd
import numpy.random                           as random
from sklearn.utils                        import shuffle
from sklearn.model_selection              import train_test_split
from tqdm                                 import tqdm
from os                                   import path
import pysftp                                 as sftp
import random                                 as rnd
from matplotlib                 import pyplot as plt 

print("="*50)
print(" TensorFlow version: {}".format(tf.__version__))
print(" Eager execution: {}".format(tf.executing_eagerly()))

#=======================================================================================================================================
def write_predictiondata(ExcitType, KineticFile, csvkinetics, iFlg, Molecules, Atoms, iLevel, jLevelVec, KVec):
    
    if (iFlg == 0):
        for i in range(len(jLevelVec)): 
            ProcName = Molecules[0] + '(' + str(iLevel+1) + ')+' + Atoms[0] + '=' + Molecules[1] + '(' + str(jLevelVec[i]+1) + ')+' + Atoms[1]
            if (KVec[i] >= MinValueTrain):
                if (ExcitType == 'KInel'):
                    Line     = ProcName + ':%.4e,+0.0000E+00,+0.0000E+00,5\n' % KVec[i]
                else:
                    Line     = ProcName + ':%.4e,+0.0000E+00,+0.0000E+00,6\n' % KVec[i]
                csvkinetics.write(Line)

    elif (iFlg == -1):
        print('[SurQCT]:   Writing Kinetics in File: ' + KineticFile )
        csvkinetics  = open(KineticFile, 'w')

    elif (iFlg == -2):
        print('[SurQCT]:   Closing Kinetics File: ' + KineticFile )
        csvkinetics.close()


    return csvkinetics

#=======================================================================================================================================
WORKSPACE_PATH      = os.environ['WORKSPACE_PATH']
SurQCTFldr          = WORKSPACE_PATH + '/SurQCT/surqct/'

RatesType           = 'KExcit'
Dimension           = 'nondim_N3'
#Dimension           = 'transfer'
LevelFileType       = 'bottom'

ExcitType           = 'KInel'
NNRunIdx            = 8
#ExcitType           = 'KExch'
#NNRunIdx            = 2

if(Dimension == 'nondim'):
    PathToRunFld        = SurQCTFldr + '/../' + RatesType + '/all_temperatures_nondim/' + ExcitType + '/'
elif (Dimension == 'nondim_N3'):
    PathToRunFld        = SurQCTFldr + '/../' + RatesType + '_N3_QCTLearn/all_temperatures_nondim/' + ExcitType + '/'
else:
    PathToRunFld        = SurQCTFldr + '/../' + RatesType + '_N3_TransLearn/all_temperatures_nondim/' + ExcitType + '/'

TTranVec            = [8750,12500.0]

Molecules           = ['N2','N2']
Atoms               = ['N','N']
System = 'N3_NASA'

ZeroDRunIdx         = NNRunIdx

MinValueTrain       = 1.e-15

#===================================================================================================================================
print("\n[SurQCT]: Loading Modules and Functions ...")

sys.path.insert(0, SurQCTFldr  + '/src/Reading/')
from Reading  import read_levelsdata, read_diatdata

InputFld = PathToRunFld + '/Run_' + str(NNRunIdx) + '/'
sys.path.insert(0, InputFld)
#===================================================================================================================================


print("\n[SurQCT]: Keep Loading Modules and Functions...")
from SurQCT_Input import inputdata

print("\n[SurQCT]: Initializing Input ...")
InputData    = inputdata(WORKSPACE_PATH, SurQCTFldr)

Prefix                    = 'Run_'
InputData.NNRunIdx        = NNRunIdx
InputData.PathToRunFld    = InputData.PathToRunFld+'/'+Prefix+str(InputData.NNRunIdx)
InputData.PathToFigFld    = InputData.PathToRunFld+'/'+InputData.PathToFigFld 
InputData.PathToParamsFld = InputData.PathToRunFld+'/'+InputData.PathToParamsFld
InputData.PathToDataFld   = InputData.PathToRunFld+'/Data/'                                                               
InputData.PathToParamsFld = InputData.PathToRunFld+'/Params/' 
InputData.KineticFldr     = InputData.WORKSPACE_PATH+'/Air_Database/Run_0D_surQCT/database/kinetics/'+Dimension+'_'+System+'_Active_Run'+str(ZeroDRunIdx)+'/'

if(Dimension=='nondim'):
    InputData.DefineModelIntFlg = 0
    InputData.TrainIntFlg       = 0
    InputData.Molecules       = ['N2','N2'] 
    InputData.PathToDiatFile  = [WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/LeRoy/MyLeroy_FromRobyn.inp',
                                 WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/LeRoy/MyLeroy_FromRobyn.inp']   
    InputData.PathToHDF5File  = InputData.WORKSPACE_PATH  + '/Air_Database/HDF5_Database_semiClassicalApprox/N3_NASA.hdf5'

    if(LevelFileType == 'bottom'):
        # Bottom Ref
        InputData.PathToLevelsFile = [WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_log_nd.csv',
                                      WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_log_nd.csv']

    elif(LevelFileType == 'ground'):
        # Ground State Ref
        InputData.PathToLevelsFile = [WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_GroundState_log_nd.csv',
                                      WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_GroundState_log_nd.csv']
        InputData.PathToHDF5File  = InputData.WORKSPACE_PATH  + '/Air_Database/HDF5_Database/N3_NASA.hdf5'
    elif(LevelFileType == 'we_normalized'):
        # we normalized
        InputData.PathToLevelsFile = [WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_Bottom_Vib_we_nd.csv',
                                      WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_Bottom_Vib_we_nd.csv']

    else:
        print('Error: Levels File type not found!')

elif(Dimension == 'nondim_N3'):
    InputData.DefineModelIntFlg = 0
    InputData.TrainIntFlg       = 0
    
elif(Dimension == 'transfer'):
    InputData.DefineModelIntFlg = 1
    InputData.TrainIntFlg       = 0
    
#===================================================================================================================================
print("\n[SurQCT]: Loading Final Modules ... ")

sys.path.insert(0, SurQCTFldr  + '/src/Model/' + InputData.ApproxModel + '/')
from Model_old import model

NN_KExcit                    = model(InputData, InputData.PathToRunFld, None, None)
NN_KExcit.load_params(InputData.PathToParamsFld)


#===================================================================================================================================
OtherVar           = InputData.OtherVar
xVarsVec_i         = InputData.xVarsVec_i + ['vqn','jqn']
xVarsVec_Delta     = InputData.xVarsVec_Delta
xVarsVec           = list(set(xVarsVec_i) | set(xVarsVec_Delta))
print('[SurQCT]:   Reading Variables: ', xVarsVec)

InputData.MultFact = 1.e+9

NMolecules         = len(InputData.PathToLevelsFile)

InputData.iLevelsVecTest = list(np.array(InputData.iLevelsVecTest) - 1)

#===================================================================================================================================
### Reading Levels Info of Initial and Final Molecules
LevelsData = []
DiatData   = []
NLevels    = []
for iMol in range(NMolecules):

    LevelsDataTemp = read_levelsdata(InputData.PathToLevelsFile[iMol], xVarsVec, '')
    LevelsData.append(LevelsDataTemp)

    DiatDataTemp = read_diatdata(InputData.PathToDiatFile[iMol], InputData.Molecules[iMol], np.array(TTranVec), np.array(TTranVec))
    DiatData.append(DiatDataTemp)

    NLevelsTemp    = LevelsDataTemp.shape[0]
    NLevels.append(NLevelsTemp)


try:
    os.makedirs(InputData.KineticFldr)
except OSError as e:
    pass

for TTran in TTranVec:
    print('[SurQCT]:    TTran = ', TTran)

    ### Opening Files
    PathToKineticFldr = InputData.KineticFldr + '/T' + str(int(TTran)) + 'K'
    try:
        os.makedirs(PathToKineticFldr)
    except OSError as e:
        pass

    if(ExcitType == 'KInel'):   
        KineticFile_KInel = PathToKineticFldr + '/Inel.dat'
        csvkinetics_KInel = write_predictiondata(ExcitType, KineticFile_KInel, None, -1, Molecules, Atoms, None, None, None)
    elif(ExcitType == 'KExch'):   
        KineticFile_KExch = PathToKineticFldr + '/Exch_Type1.dat'
        csvkinetics_KExch = write_predictiondata(ExcitType, KineticFile_KExch, None, -1, Molecules, Atoms, None, None, None)

    ### Loop on Initial States
    Str = 'q_'+str(int(TTran))
    for iIdx in tqdm(range(NLevels[0]), desc='[SurQCT]:     Generating Inelastic and Exchange Rate Matrixes'):
        time.sleep(0.001)
        
        if (InputData.ExoEndoFlg):
            jIdxVec           = [jIdx for jIdx in np.arange(NLevels[1]) if (DiatData[1]['EInt'].to_numpy()[jIdx] < DiatData[0]['EInt'].to_numpy()[iIdx])]
            jIdxVecNo         = [jIdx for jIdx in np.arange(NLevels[1]) if (DiatData[1]['EInt'].to_numpy()[jIdx] >= DiatData[0]['EInt'].to_numpy()[iIdx])]
            RatioNo           = [DiatData[0][Str].to_numpy()[iIdx]/DiatData[1][Str].to_numpy()[jIdx] for jIdx in np.arange(NLevels[1]) if (DiatData[1]['EInt'].to_numpy()[jIdx] >= DiatData[0]['EInt'].to_numpy()[iIdx])]
        else:
            jIdxVec           = [jIdx for jIdx in np.arange(NLevels[1]) if (DiatData[1][Str].to_numpy()[jIdx]    > DiatData[0][Str].to_numpy()[iIdx])]
            jIdxVecNo         = [jIdx for jIdx in np.arange(NLevels[1]) if (DiatData[1][Str].to_numpy()[jIdx]    <= DiatData[0][Str].to_numpy()[iIdx])]
            RatioNo           = [DiatData[0][Str].to_numpy()[iIdx]/DiatData[1][Str].to_numpy()[jIdx] for jIdx in np.arange(NLevels[1]) if (DiatData[1][Str].to_numpy()[jIdx]    <= DiatData[0][Str].to_numpy()[iIdx])]
        jNLevels              = len(jIdxVec)
        jNLevelsNo            = len(jIdxVecNo)
        
        ### FWD Rates
        iiIdxVec              = [iIdx]*jNLevels
        
        TTranVecTemp          = np.ones((jNLevels))*TTran
        TTranDataTemp         = pd.DataFrame({'TTran': TTranVecTemp})
        TTranDataTemp.index   = jIdxVec

        
        iLevelsDataTemp       = LevelsData[0].iloc[iiIdxVec,:].copy()
        iLevelsDataTemp.index = jIdxVec

        jLevelsDataTemp       = LevelsData[1].iloc[jIdxVec,:].copy()        
        if (OtherVar == '_Delta'):
            jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
        else:
            jLevelsDataTemp   = jLevelsDataTemp
        jLevelsDataTemp.index = jIdxVec
        
        kLevelsDataTemp       = LevelsData[1].iloc[jIdxVec,:].copy()        
        kLevelsDataTemp.index = jIdxVec

        
        iLevelsData           = pd.concat([iLevelsDataTemp[xVarsVec_i], TTranDataTemp], axis=1)
        iLevelsData.columns   = [(VarName + '_i') for VarName in iLevelsData.columns]
        
        jLevelsData           = pd.concat([jLevelsDataTemp[xVarsVec_Delta], TTranDataTemp], axis=1)
        jLevelsData.columns   = [(VarName + OtherVar) for VarName in jLevelsData.columns]

        kLevelsData           = pd.concat([kLevelsDataTemp[xVarsVec_i], TTranDataTemp], axis=1)
        kLevelsData.columns   = [(VarName + '_j') for VarName in kLevelsData.columns]
        
        xTemp_FWD             = pd.concat([iLevelsData, jLevelsData, kLevelsData], axis=1)
                
        if (len(xTemp_FWD[NN_KExcit.xTrainingVar]) > 0):
            if(ExcitType == 'KInel'):
                KInel_NN_FWD      = np.exp( NN_KExcit.Model.predict(xTemp_FWD[NN_KExcit.xTrainingVar]) ) / InputData.MultFact
                csvkinetics_KInel = write_predictiondata(ExcitType, KineticFile_KInel, csvkinetics_KInel, 0, Molecules, Atoms, iIdx, jIdxVec, KInel_NN_FWD)
                
            elif(ExcitType == 'KExch'):
                KExch_NN_FWD      = np.exp( NN_KExcit.Model.predict(xTemp_FWD[NN_KExcit.xTrainingVar]) ) / InputData.MultFact
                csvkinetics_KExch = write_predictiondata(ExcitType, KineticFile_KExch, csvkinetics_KExch, 0, Molecules, Atoms, iIdx, jIdxVec, KExch_NN_FWD)
                
    if(ExcitType == 'KInel'): 
        csvkinetics_KInel = write_predictiondata(ExcitType, KineticFile_KInel, csvkinetics_KInel, -2, None, None, None, None, None)
    elif(ExcitType == 'KExch'):
        csvkinetics_KExch = write_predictiondata(ExcitType, KineticFile_KExch, csvkinetics_KExch, -2, None, None, None, None, None)
