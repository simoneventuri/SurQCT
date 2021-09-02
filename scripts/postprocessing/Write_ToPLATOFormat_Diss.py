import time
import os
import shutil
import sys
import h5py
import tensorflow                             as tf
import numpy                                  as np
import seaborn                                as sns
import pandas                                 as pd
import matplotlib.pyplot                      as plt
import numpy.random                           as random
from sklearn.utils                        import shuffle
from sklearn.model_selection              import train_test_split
from os                                   import path

#=======================================================================================================================================
def write_predictiondata(KineticFile, csvkinetics, iFlg, Molecules, Atoms, jLevelVec, KVec):

    if (iFlg == 0):
        for i in range(len(jLevelVec)): 
            ProcName = Molecules[0] + '(' + str(i+1) + ')+' + Atoms[0] + '=' + Atoms[1]+'+'+Atoms[1]+'+'+Atoms[1]
            Line     = ProcName + ':%.4e,+0.0000E+00,+0.0000E+00,5\n' % KVec[i]
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

RatesType           = 'KDiss'

NNRunIdx            = 4      

PathToRunFld        = SurQCTFldr + '/../' + RatesType + '/all_temperatures/'  

#TTranVec            = [1500.0, 2500.0, 5000.0, 6000.0, 8000.0, 10000.0, 12000.0, 15000.0, 20000.0]
TTranVec            = [1500.0]

Molecules           = ['O2','O2']
Atoms               = ['O','O']

ODRunIdx            = 1


#===================================================================================================================================
print("\n[SurQCT]: Loading Modules and Functions ...")

sys.path.insert(0, SurQCTFldr  + '/src/Reading/')
from Reading  import read_levelsdata, read_diatdata

InputFld = PathToRunFld + '/Run_' + str(NNRunIdx) + '/'
sys.path.insert(0, InputFld)
#===================================================================================================================================



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
InputData.KineticFldr     = InputData.WORKSPACE_PATH+'/Air_Database/Run_0D_surQCT/database/kinetics/O3_UMN_Run'+str(ODRunIdx)+'/'

#===================================================================================================================================
print("\n[SurQCT]: Loading Final Modules ... ")

sys.path.insert(0, SurQCTFldr  + '/src/Model/' + InputData.ApproxModel + '/')
from Model import model


InputData.DefineModelIntFlg = 0
InputData.TrainIntFlg       = 0
NN_KDiss                    = model(InputData, InputData.PathToRunFld, None, None)
NN_KDiss.load_params(InputData.PathToParamsFld)
#===================================================================================================================================


#===================================================================================================================================
OtherVar           = InputData.OtherVar
xVarsVec_i         = InputData.xVarsVec_i + ['vqn','jqn']
xVarsVec_Delta     = InputData.xVarsVec_Delta
xVarsVec           = list(set(xVarsVec_i) | set(xVarsVec_Delta))
print('[SurQCT]:   Reading Variables: ', xVarsVec)

InputData.MultFact = 1.e+08
MinValueTrain      = 1.e-18 * InputData.MultFact
MinValueTest       = 1.e-18 * InputData.MultFact
NoiseSD            = 1.e-17 * InputData.MultFact
InputData.DissCorrFactor   = 16.0/3.0

NMolecules         = len(InputData.PathToLevelsFile)

#InputData.iLevelsVecTest = list(np.array(InputData.iLevelsVecTest) - 1)


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


try:
    os.makedirs(InputData.KineticFldr)
except OSError as e:
    pass

### Initializing Rates Matrix
KDissVec = None #np.zeros((NLevels))


#===================================================================================================================================
### Opening Files for Writing Rates 
for TTran in TTranVec:
    print('[SurQCT]:    TTran = ', TTran)


    ### Opening Files
    PathToKineticFldr = InputData.KineticFldr + '/T' + str(int(TTran)) + 'K'
    try:
        os.makedirs(PathToKineticFldr)
    except OSError as e:
        pass

    FileName     = '/Diss.dat'
    if (InputData.DissCorrFactor != 0.0):
        FileName = '/Diss_Corrected.dat' 

    KineticFile_KDiss = PathToKineticFldr + FileName
    csvkinetics_KDiss = write_predictiondata(KineticFile_KDiss, None, -1, Molecules, Atoms, None, None)


    print('[SurQCT]:     Generating Dissociation Rate Vector')

    iIdxVec                  = np.arange(NLevels[1])

    TTranVec                 = np.ones((NLevels[1]))*TTran
    TTranDataTemp            = pd.DataFrame({'TTran': TTranVec})
    TTranDataTemp.index      = iIdxVec

    iLevelsDataTemp          = LevelsData[0].copy()
    iLevelsDataTemp.index    = iIdxVec

    xTemp                    = pd.concat([iLevelsDataTemp, TTranDataTemp], axis=1)
    xTemp.columns            = [(VarName + '_i') for VarName in xTemp.columns]

    KDiss                    = np.exp( NN_KDiss.Model.predict(xTemp[NN_KDiss.xTrainingVar]) ) / InputData.MultFact * InputData.DissCorrFactor
    iIdxVec                  = [i for i in range(NLevels[1]) if (KDiss[i,0] > MinValueTrain)]
    #KDissVec[iIdxVec]  = KDiss[iIdxVec,0] 

    csvkinetics_KDiss        = write_predictiondata(KineticFile_KDiss, csvkinetics_KDiss, 0, Molecules, Atoms, iIdxVec, KDiss[iIdxVec,0])


    #===================================================================================================================================
    ### Closing Files for Rates
    csvkinetics_KDiss = write_predictiondata(KineticFile_KDiss, csvkinetics_KDiss, -2, Molecules, Atoms, None, None)




