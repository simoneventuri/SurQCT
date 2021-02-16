import time
import os
import shutil
import sys
import tensorflow                             as tf
import numpy                                  as np
import seaborn                                as sns
import pandas                                 as pd
import matplotlib.pyplot                      as plt
import numpy.random                           as random
from sklearn.utils                        import shuffle
from sklearn.model_selection              import train_test_split


from Reading  import read_levelsdata, read_kexcitdata, sample_initiallevels, read_sampledinitiallevels


#=======================================================================================================================================
def generate_data(InputData):

    OtherVar           = InputData.OtherVar
    xVarsVec           = InputData.xVarsVec

    InputData.MultFact = 1.e+09
    MinValueTrain      = 1.e-16 * InputData.MultFact
    MinValueTest       = 1.e-16 * InputData.MultFact
    NoiseSD            = 1.e-13 * InputData.MultFact


    #===================================================================================================================================
    ### Reading Levels Info of Initial and Final Molecules
    LevelsData       = read_levelsdata(InputData.PathToLevelsFile[0], xVarsVec, '')
    NLevels          = LevelsData.shape[0]


    #===================================================================================================================================
    ### Loading Input and Output for Training and Validation
    print('[SurQCT]:   Generating Training and Validation Data Points')
    TTranVec         = InputData.TTranVecTrain
    NTTran           = len(InputData.TTranVecTrain)
    

    ### Initializing Quantities
    iIdxData         = pd.DataFrame(columns = ['Idx_i'])
    jIdxData         = pd.DataFrame(columns = ['Idx_j'])
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    jLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])
    KExcitData       = pd.DataFrame(columns = ['KExcit'])


    for iT in range(NTTran):
        print('[SurQCT]:     Translational Temperature: T = ' + str(int(TTranVec[iT])) + 'K')

        ### Reading Rates at Temperature TTranVec[iT]
        KExcitMat, KExchMat       = read_kexcitdata(InputData, InputData.PathToHAHDF5File, TTranVec[iT], TTranVec[iT], 3)


        ### Deciding Initial Levels LIst        
        if   (InputData.iLevelsIntFlg == 1):
            iIdxVec = InputData.iLevelsVec
        elif (InputData.iLevelsIntFlg == 2):
            np.random.seed(InputData.iLevelsSeedsVec[0])
            iIdxVec = np.random.choice(NLevels, InputData.NiLevelsSampled, replace=False)
        elif (InputData.iLevelsIntFlg == 3):
            NSamplesPerGroup = 1
            iIdxVec          = sample_initiallevels(InputData.PathToGrouping, NSamplesPerGroup, InputData.iLevelsSeedsVec[iT])
        elif (InputData.iLevelsIntFlg == 4):
            iIdxVec = read_sampledinitiallevels(InputData.PathToSampledLevels, TTranVec[iT])
        print('[SurQCT]:       Vector of Initial Levels: iIdxVec = ', iIdxVec)
        iIdxVec = iIdxVec - 1


        ### Loop on Initial States
        for iIdx in iIdxVec:

            ### Selecting only Final States with EXOTHERMIC KExit > MinValueTrain 
            jIdxVec               = [jIdx for jIdx, x in enumerate(KExcitMat[iIdx,:] > MinValueTrain) if (x and jIdx<iIdx)]
            jNLevels              = len(jIdxVec)
            kIdxVec               = [iIdx]*jNLevels
            

            ### Appending Vertically
            iIdxData              = iIdxData.append(pd.DataFrame({'Idx_i': kIdxVec}))
            jIdxData              = jIdxData.append(pd.DataFrame({'Idx_j': jIdxVec}))

            TTran                 = np.ones((jNLevels)) * TTranVec[iT]
            TTranData             = TTranData.append(pd.DataFrame({'TTran': TTran}))

            KExcitData            = KExcitData.append(pd.DataFrame({'KExcit': KExcitMat[iIdx, jIdxVec]}))
            
            iLevelsDataTemp       = LevelsData.iloc[kIdxVec,:].copy()
            iLevelsDataTemp.index = np.arange(len(TTran))
            iLevelsData           = iLevelsData.append(iLevelsDataTemp)

            jLevelsDataTemp       = LevelsData.iloc[jIdxVec,:].copy()        
            jLevelsDataTemp.index = np.arange(len(TTran))
            if (OtherVar == '_Delta'):
                jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
            else:
                jLevelsDataTemp   = jLevelsDataTemp
            jLevelsData           = jLevelsData.append(jLevelsDataTemp)

        print('[SurQCT]:       Now the Data Matrix contains ', len(KExcitData), ' Data Points')

    ### Resetting Data Frames Indexing
    iIdxData.index      = np.arange(len(TTranData))
    jIdxData.index      = np.arange(len(TTranData))
    TTranData.index     = np.arange(len(TTranData))
    iLevelsData.index   = np.arange(len(TTranData))
    jLevelsData.index   = np.arange(len(TTranData))
    KExcitData.index    = np.arange(len(TTranData))


    ### Concatenating Horizzontally
    iLevelsData         = pd.concat([iLevelsData, TTranData], axis=1)
    iLevelsData.columns = [(VarName + '_i') for VarName in iLevelsData.columns]
    jLevelsData         = pd.concat([jLevelsData, TTranData], axis=1)
    jLevelsData.columns = [(VarName + OtherVar) for VarName in jLevelsData.columns]
    DataSet             = pd.concat([iLevelsData, jLevelsData], axis=1)
    DataSet             = pd.concat([DataSet, KExcitData], axis=1)
    DataSet             = pd.concat([DataSet, iIdxData],   axis=1)
    DataSet             = pd.concat([DataSet, jIdxData],   axis=1)
 

    ### Splitting DataSet in Training, Validation
    # TrainData = DataSet.sample(frac=(1.0-InputData.TestPerc/100.0), random_state=3)
    # AllData  = DataSet.drop(TrainData.index)
    TrainData = DataSet.copy()
    AllData   = DataSet.copy()

    TrainData = TrainData.sample(frac=(1.0-InputData.ValidPerc/100.0), random_state=3)
    ValidData = DataSet.drop(TrainData.index)


    ### Adding Noise to Training and Validation
    TrainDataFinal        = TrainData.copy()
    ValidDataFinal        = ValidData.copy()

    for iSample in range(InputData.NSamplesNoise):

        TrainDataTemp        = TrainData.copy()
        TrainDataTemp.KExcit = TrainDataTemp.KExcit + random.normal(loc=0.0, scale=NoiseSD, size=len(TrainData))
        TrainDataFinal       = TrainDataFinal.append(TrainDataTemp[TrainDataTemp['KExcit'] > MinValueTrain] )

        ValidDataTemp        = ValidData.copy()
        ValidDataTemp.KExcit = ValidDataTemp.KExcit + random.normal(loc=0.0, scale=NoiseSD, size=len(ValidData))
        ValidDataFinal       = ValidDataFinal.append(ValidDataTemp[ValidDataTemp['KExcit'] > MinValueTrain] )

    TrainDataFinal.KExcit    = np.log( TrainDataFinal.KExcit )
    ValidDataFinal.KExcit    = np.log( ValidDataFinal.KExcit )
    AllData.KExcit           = np.log( AllData.KExcit )

    TrainDataFinal.index     = np.arange(len(TrainDataFinal))
    ValidDataFinal.index     = np.arange(len(ValidDataFinal))


    ### Collecting Training and Validation
    x_train = TrainDataFinal.copy()
    x_train.pop('KExcit')
    x_valid = ValidDataFinal.copy()
    x_valid.pop('KExcit')
    x_all   = AllData.copy()
    x_all.pop('KExcit')

    y_train = TrainDataFinal[['KExcit', 'TTran_i']]
    y_valid = ValidDataFinal[['KExcit', 'TTran_i']]
    y_all   = AllData[['KExcit', 'TTran_i']]



    #===================================================================================================================================
    ### Loading Input and Output for Labeled Testing 
    print('[SurQCT]:   Generating Labeled Test Data Points')
    TTranVec         = InputData.TTranVecTest
    NTTran           = len(InputData.TTranVecTest)

    iIdxVec          = InputData.iLevelsVecTest

    iIdxData         = pd.DataFrame(columns = ['Idx_i'])
    jIdxData         = pd.DataFrame(columns = ['Idx_j'])
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    jLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])
    KExcitData       = pd.DataFrame(columns = ['KExcit'])
    for iT in range(NTTran):
        KExcitMat, KExchMat       = read_kexcitdata(InputData, InputData.PathToHDF5File, TTranVec[iT], TTranVec[iT], 3)

        for iIdx in iIdxVec:
            jIdxVec               = [jIdx for jIdx, x in enumerate(KExcitMat[iIdx,:] > MinValueTest) if (x and jIdx<iIdx)]
            jNLevels              = len(jIdxVec)
            kIdxVec               = [iIdx]*jNLevels
    
            iIdxData              = iIdxData.append(pd.DataFrame({'Idx_i': kIdxVec}))
            jIdxData              = jIdxData.append(pd.DataFrame({'Idx_j': jIdxVec}))

            TTran                 = np.ones((jNLevels)) * TTranVec[iT]
            TTranData             = TTranData.append(pd.DataFrame({'TTran': TTran}))

            KExcitData            = KExcitData.append(pd.DataFrame({'KExcit': np.log( KExcitMat[iIdx, jIdxVec] )}))
            
            iLevelsDataTemp       = LevelsData.iloc[kIdxVec,:].copy()
            iLevelsDataTemp.index = np.arange(len(TTran))
            iLevelsData           = iLevelsData.append(iLevelsDataTemp)

            jLevelsDataTemp       = LevelsData.iloc[jIdxVec,:].copy()        
            jLevelsDataTemp.index = np.arange(len(TTran))
            if (OtherVar == '_Delta'):
                jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
            else:
                jLevelsDataTemp   = jLevelsDataTemp
            jLevelsData           = jLevelsData.append(jLevelsDataTemp)
            
    iIdxData.index      = np.arange(len(TTranData))
    jIdxData.index      = np.arange(len(TTranData))
    TTranData.index     = np.arange(len(TTranData))
    iLevelsData.index   = np.arange(len(TTranData))
    jLevelsData.index   = np.arange(len(TTranData))
    KExcitData.index    = np.arange(len(TTranData))

    iLevelsData         = pd.concat([iLevelsData, TTranData], axis=1)
    iLevelsData.columns = [(VarName + '_i') for VarName in iLevelsData.columns]
    jLevelsData         = pd.concat([jLevelsData, TTranData], axis=1)
    jLevelsData.columns = [(VarName + OtherVar) for VarName in jLevelsData.columns]
    DataSet             = pd.concat([iLevelsData, jLevelsData], axis=1)
    DataSet             = pd.concat([DataSet, KExcitData], axis=1)
    DataSet             = pd.concat([DataSet, iIdxData],   axis=1)
    DataSet             = pd.concat([DataSet, jIdxData],   axis=1)

    x_test = DataSet.copy()
    x_test.pop('KExcit')
    y_test = DataSet[['KExcit', 'TTran_i']]



    #===================================================================================================================================
    ### Loading Input and Output for Unlabeled Testing 
    print('[SurQCT]:   Generating Un-Labeled Test Data Points')
    TTranVec    = InputData.TTranVecExtra
    NTTran      = len(InputData.TTranVecExtra)

    iIdxData         = pd.DataFrame(columns = ['Idx_i'])
    jIdxData         = pd.DataFrame(columns = ['Idx_j'])
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    jLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])

    for iT in range(NTTran):
        
        iIdxVec                   = [1000]#np.random.choice(NLevels, NPerTTranTrain, replace=False)
        for iIdx in iIdxVec:
            jIdxVec               = [jIdx for jIdx, x in enumerate(KExcitMat[iIdx,:] > MinValueTest) if (x and jIdx<iIdx)]
            jNLevels              = len(jIdxVec)
            kIdxVec               = [iIdx]*jNLevels
    
            iIdxData              = iIdxData.append(pd.DataFrame({'Idx_i': kIdxVec}))
            jIdxData              = jIdxData.append(pd.DataFrame({'Idx_j': jIdxVec}))

            TTran                 = np.ones((jNLevels)) * TTranVec[iT]
            TTranData             = TTranData.append(pd.DataFrame({'TTran': TTran}))
            
            iLevelsDataTemp       = LevelsData.iloc[kIdxVec,:].copy()
            iLevelsDataTemp.index = np.arange(len(TTran))
            iLevelsData           = iLevelsData.append(iLevelsDataTemp)

            jLevelsDataTemp       = LevelsData.iloc[jIdxVec,:].copy()        
            jLevelsDataTemp.index = np.arange(len(TTran))
            if (OtherVar == '_Delta'):
                jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
            else:
                jLevelsDataTemp   = jLevelsDataTemp
            jLevelsData           = jLevelsData.append(jLevelsDataTemp)
            
    iIdxData.index      = np.arange(len(TTranData))
    jIdxData.index      = np.arange(len(TTranData))
    TTranData.index     = np.arange(len(TTranData))
    iLevelsData.index   = np.arange(len(TTranData))
    jLevelsData.index   = np.arange(len(TTranData))

    iLevelsData         = pd.concat([iLevelsData, TTranData], axis=1)
    iLevelsData.columns = [(VarName + '_i') for VarName in iLevelsData.columns]
    jLevelsData         = pd.concat([jLevelsData, TTranData], axis=1)
    jLevelsData.columns = [(VarName + OtherVar) for VarName in jLevelsData.columns]
    DataSet             = pd.concat([iLevelsData, jLevelsData], axis=1)
    DataSet             = pd.concat([DataSet, iIdxData],   axis=1)
    DataSet             = pd.concat([DataSet, jIdxData],   axis=1)

    x_extra = DataSet.copy()



    TrainData = (x_train, y_train)
    ValidData = (x_valid, y_valid)
    AllData   = (x_all,   y_all)
    TestData  = (x_test,  y_test)
    ExtraData = (x_extra)

    return InputData, TrainData, ValidData, AllData, TestData, ExtraData

#=======================================================================================================================================



#=======================================================================================================================================
def plot_prediction(InputData, CaseType, TTranVec, xPred, yData, yPred):

    TrainingVar = InputData.RatesType
    Idxs        = xPred.Idx_i.unique()
    
    for TTran in (TTranVec):

        for iIdx in Idxs:
            kIdx1 = xPred.index[(xPred['Idx_i'] == iIdx)].tolist()
            kIdx2 = xPred.index[(xPred['TTran_i'] == TTran)].tolist()
            kIdx  = list(set(kIdx1) & set(kIdx2))

            fig = plt.figure()
            plt.xlabel('Level Index')
            plt.ylabel('$K_i^{Excit}$ [$cm^3$/s]')
            if (len(yData)>0):
                plt.scatter(xPred['Idx_j'][kIdx], np.exp(yData[TrainingVar][kIdx])/InputData.MultFact, c='k', marker='+', linewidths =0.5, label='Data')
            plt.scatter(    xPred['Idx_j'][kIdx], np.exp(yPred[kIdx])/InputData.MultFact,              c='r', marker='x', linewidths =0.5, label='Predicted')    
            plt.yscale('log')
            plt.legend()
            plt.grid()
            plt.title('Excitation Rates at T = ' + str(int(TTran)) + 'K')
            FigPath = InputData.PathToFigFld + '/' + CaseType + 'Case_T' + str(int(TTran)) + 'K_Level' + str(iIdx) + '.png'
            fig.savefig(FigPath, dpi=600)
            plt.show()
            #plt.close()

#=======================================================================================================================================
