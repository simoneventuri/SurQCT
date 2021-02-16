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


from Reading  import read_levelsdata, read_kdissdata, sample_initiallevels, read_sampledinitiallevels


#=======================================================================================================================================
def generate_data(InputData):

    xVarsVec         = InputData.xVarsVec

    InputData.MultFact = 1.e+01
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
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])
    KDissData        = pd.DataFrame(columns = ['KDiss'])

    
    for iT in range(NTTran):
        print('[SurQCT]:     Translational Temperature: T = ' + str(int(TTranVec[iT])) + 'K')

        ### Reading Rates at Temperature TTranVec[iT]
        KDiss       = read_kdissdata(InputData, InputData.PathToHAHDF5File, TTranVec[iT], TTranVec[iT])


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
        iIdxVec     = iIdxVec - 1

        iIdxVec     = [jIdx for jIdx in iIdxVec if (KDiss[jIdx] > MinValueTrain)]
        print('[SurQCT]:       Vector of Initial Levels Cleaned from Zero Values: iIdxVec = ', iIdxVec)
        NLevelsTemp = len(iIdxVec)


        ### Appending Vertically
        iIdxData    = iIdxData.append(pd.DataFrame({'Idx_i': iIdxVec}))
        iLevelsData = iLevelsData.append(LevelsData.iloc[iIdxVec])
        TTran       = np.ones((NLevelsTemp)) * TTranVec[iT]
        TTranData   = TTranData.append(pd.DataFrame({'TTran': TTran}))
        KDissData   = KDissData.append(pd.DataFrame({'KDiss': np.log(KDiss[iIdxVec]) }))

        print('[SurQCT]:       Now the Data Matrix contains ', len(KDissData), ' Data Points')


    ### Resetting Data Frames Indexing
    iIdxData.index     = np.arange(len(TTranData))
    iLevelsData.index  = np.arange(len(TTranData))
    TTranData.index    = np.arange(len(TTranData))
    KDissData.index    = np.arange(len(TTranData))


    ### Concatenating Horizzontally
    iLevelsData         = pd.concat([iLevelsData, TTranData], axis=1)
    iLevelsData.columns = [(VarName + '_i') for VarName in iLevelsData.columns]
    DataSet             = pd.concat([iLevelsData, KDissData], axis=1)
    DataSet             = pd.concat([DataSet, iIdxData],   axis=1)


    ### Splitting DataSet in Training, Validation
    # TrainData = DataSet.sample(frac=(1.0-InputData.TestPerc/100.0), random_state=3)
    # AllData  = DataSet.drop(TrainData.index)
    TrainData = DataSet.copy()
    AllData   = DataSet.copy()

    TrainData = TrainData.sample(frac=(1.0-InputData.ValidPerc/100.0), random_state=3)
    ValidData = DataSet.drop(TrainData.index)


    ### Collecting Training and Validation
    x_train = TrainData.copy()
    x_train.pop('KDiss')
    x_valid = ValidData.copy()
    x_valid.pop('KDiss')
    x_all   = AllData.copy()
    x_all.pop('KDiss')

    y_train = TrainData[['KDiss', 'TTran_i']]
    y_valid = ValidData[['KDiss', 'TTran_i']]
    y_all   = AllData[['KDiss', 'TTran_i']]



    #===================================================================================================================================
    ### Loading Input and Output for Labeled Testing 
    print('[SurQCT]:   Generating Labeled Test Data Points')
    TTranVec         = InputData.TTranVecTest
    NTTran           = len(InputData.TTranVecTest)

    iIdxData         = pd.DataFrame(columns = ['Idx_i'])
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])
    KDissData        = pd.DataFrame(columns = ['KDiss'])
    
    for iT in range(NTTran):
        KDiss       = np.log(read_kdissdata(InputData, InputData.PathToHDF5File, TTranVec[iT], TTranVec[iT]) + 1.e-20)

        iIdxData    = iIdxData.append(pd.DataFrame({'Idx_i': np.arange(NLevels)}))
        iLevelsData = iLevelsData.append(LevelsData)
        TTran       = np.ones((NLevels)) * TTranVec[iT]
        TTranData   = TTranData.append(pd.DataFrame({'TTran': TTran}))
        KDissData   = KDissData.append(pd.DataFrame({'KDiss': KDiss}))

    ### Resetting Data Frames Indexing
    iIdxData.index      = np.arange(len(TTranData))
    iLevelsData.index   = np.arange(len(TTranData))
    TTranData.index     = np.arange(len(TTranData))
    KDissData.index     = np.arange(len(TTranData))

    ### Concatenating Horizzontally
    iLevelsData         = pd.concat([iLevelsData, TTranData], axis=1)
    iLevelsData.columns = [(VarName + '_i') for VarName in iLevelsData.columns]
    DataSet             = pd.concat([iLevelsData, KDissData], axis=1)
    DataSet             = pd.concat([DataSet, iIdxData],   axis=1)

    x_test = DataSet.copy()
    x_test.pop('KDiss')
    y_test = DataSet[['KDiss', 'TTran_i']]



    #===================================================================================================================================
    ### Loading Input and Output for Unlabeled Testing 
    print('[SurQCT]:   Generating Un-Labeled Test Data Points')
    TTranVec         = InputData.TTranVecExtra
    NTTran           = len(InputData.TTranVecExtra)

    iIdxData         = pd.DataFrame(columns = ['Idx_i'])
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])
    KDissData        = pd.DataFrame(columns = ['KDiss'])
    
    for iT in range(NTTran):

        iIdxData     = iIdxData.append(pd.DataFrame({'Idx_i': np.arange(NLevels)}))
        iLevelsData  = iLevelsData.append(LevelsData)
        TTran        = np.ones((NLevels)) * TTranVec[iT]
        TTranData    = TTranData.append(pd.DataFrame({'TTran': TTran}))

    ### Resetting Data Frames Indexing
    iIdxData.index     = np.arange(len(TTranData))
    iLevelsData.index  = np.arange(len(TTranData))
    TTranData.index    = np.arange(len(TTranData))

    ### Concatenating Horizzontally
    iLevelsData           = pd.concat([iLevelsData, TTranData], axis=1)
    iLevelsData.columns   = [(VarName + '_i') for VarName in iLevelsData.columns]
    DataSet               = pd.concat([iLevelsData, iIdxData], axis=1)

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
    NLevels     = len(yPred)
    Idxs        = np.arange(NLevels)+1

    for TTran in (TTranVec):
        kIdx = xPred.index[(xPred['TTran_i'] == TTran)].tolist()

        fig = plt.figure()
        plt.xlabel('Level Index')
        plt.ylabel('$K_i^D$ [$cm^3$/s]')
        plt.ylim([1.e-15, 5.e-8])
        # plt.xlim([min(time), max(time)])
        if (len(yData)==NLevels):
            plt.scatter(xPred['Idx_i'][kIdx], np.exp(yData[TrainingVar][kIdx])/InputData.MultFact, c='k', marker='+', linewidths =0.5, label='Data')
        plt.scatter(    xPred['Idx_i'][kIdx], np.exp(yPred[kIdx])/InputData.MultFact,              c='r', marker='x', linewidths =0.5, label='Predicted')
        plt.yscale('log')
        plt.legend()
        plt.grid()
        plt.title('Dissociation Rates at T = ' + str(int(TTran)) + 'K')
        FigPath = InputData.PathToFigFld + '/' + CaseType + 'Case_T' + str(int(TTran)) + 'K.png'
        fig.savefig(FigPath, dpi=600)
        plt.show()
        #plt.close()

#=======================================================================================================================================
