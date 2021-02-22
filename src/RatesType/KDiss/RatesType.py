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
def generate_trainingdata(InputData):

    from Reading  import read_levelsdata, sample_initiallevels, read_sampledinitiallevels

    xVarsVec           = InputData.xVarsVec

    InputData.MultFact = 1.e+07
    MinValueTrain      = 1.e-18 * InputData.MultFact
    MinValueTest       = 1.e-18 * InputData.MultFact
    NoiseSD            = 1.e-13 * InputData.MultFact


    #===================================================================================================================================
    ### Reading Levels Info of Initial and Final Molecules
    LevelsData         = read_levelsdata(InputData.PathToLevelsFile[0], xVarsVec, '')
    NLevels            = LevelsData.shape[0]


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
# Reading Dissociation Rates Data 
def read_kdissdata(InputData, PathToHDF5File, TTra, TInt):
    print('[SurQCT]:       Reading HDF5 File from: ' + PathToHDF5File + ' for Dissociation Rates at Temperature ' + str(int(TTra)) + 'K')

    HDF5Exist_Flg = path.exists(PathToHDF5File)
    if (HDF5Exist_Flg):
        f = h5py.File(PathToHDF5File, 'a')
    else:
        f = {'key': 'value'}

    TStr = 'T_' + str(int(TTra)) + '_' + str(int(TInt)) + '/Rates/'
    grp  = f[TStr]

    Data  = grp["Diss"]
    KDiss = Data[...]

    f.close()                                                          
    
    KDiss = KDiss[:,0] * InputData.MultFact  

    return KDiss

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
        plt.ylim([1.e-17, 5.e-8])
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



#=======================================================================================================================================
def generate_predictiondata(SurQCTFldr, PathToLevelsFile, TTran, KineticFldr):


    #===================================================================================================================================
    print("\n[SurQCT]: Loading Input Module ...")
    
    InputFile = SurQCTFldr + '/src/InputData/'
    print("[SurQCT]:   Calling SurQCT with the PRESET Input File Located in " + InputFile )
    sys.path.insert(0, InputFile)
    from SurQCT_Input import inputdata

    sys.path.insert(0, SurQCTFldr  + '/src/Reading/')
    from Reading import read_levelsdata

    #====================================================================================================================================



    #===================================================================================================================================
    print("\n[SurQCT]: Initializing Input ...")
    WORKSPACE_PATH             = os.getenv('WORKSPACE_PATH')  

    InputData                  = inputdata(WORKSPACE_PATH, SurQCTFldr)

    InputData.PathToLevelsFile = PathToLevelsFile
    InputData.RatesType        = 'KDiss'
    InputData.xVarsVec         = ['EVib','ERot','VMax','ro','rMax']
    InputData.ApproxModel      = 'FNN'

    OtherVar                   = InputData.OtherVar
    xVarsVec                   = InputData.xVarsVec

    InputData.MultFact         = 1.e+07
    MinValue                   = 1.e-18
    InputData.DissCorrFactor   = 16.0/3.0
    #===================================================================================================================================



    #===================================================================================================================================
    print("\n[SurQCT]: Loading Final Modules ... ")

    sys.path.insert(0, SurQCTFldr  + '/src/Model/' + InputData.ApproxModel + '/')
    from Model import model

    #===================================================================================================================================



    #===================================================================================================================================
    print('\n[SurQCT]: Initializing ML Model for KInel and Loading its Parameters ... ')

    PathToRunFld              = SurQCTFldr + '/../' + InputData.RatesType + '/Test' + str(InputData.NNRunIdx)
    InputData.PathToDataFld   = PathToRunFld + '/Data/'                                                               
    InputData.PathToParamsFld = PathToRunFld + '/Params/'                                                            

    NN_KDiss     = model(InputData, PathToRunFld, None, None)
    NN_KDiss.load_params(InputData.PathToParamsFld)

    #===================================================================================================================================



    #===================================================================================================================================
    print('\n[SurQCT]: Generating Rate Matrix at Translational Temperature: T = ' + str(int(TTran)) + 'K')


    #===================================================================================================================================
    ### Reading Levels Info of Initial and Final Molecules
    LevelsData                = read_levelsdata(InputData.PathToLevelsFile[0], xVarsVec, '')
    NLevels                   = LevelsData.shape[0]


    #===================================================================================================================================
    ### Initializing Rates Matrix
    KDissVec = None #np.zeros((NLevels))


    #===================================================================================================================================
    ### Opening Files for Writing Rates 
    KineticFldr_Temp = KineticFldr + '/T' + str(int(TTran)) + 'K/'
    PathToFldr = InputData.PathToFigFld
    try:
        os.makedirs(KineticFldr_Temp)
    except OSError as e:
        pass
    FileName     = '/Diss.dat'
    if (InputData.DissCorrFactor != 0.0):
        FileName = '/Diss_Corrected.dat' 
    KineticFile_KDiss = KineticFldr_Temp + FileName
    csvkinetics_KDiss = write_predictiondata(KineticFile_KDiss, None, -1, None, None)


    print('[SurQCT]:     Generating Dissociation Rate Vector')

    iIdxVec                  = np.arange(NLevels)

    TTranVec                 = np.ones((NLevels))*TTran
    TTranDataTemp            = pd.DataFrame({'TTran': TTranVec})
    TTranDataTemp.index      = iIdxVec

    iLevelsDataTemp          = LevelsData.copy()
    iLevelsDataTemp.index    = iIdxVec

    xTemp                    = pd.concat([iLevelsDataTemp, TTranDataTemp], axis=1)
    xTemp.columns            = [(VarName + '_i') for VarName in xTemp.columns]

    KDiss                    = np.exp( NN_KDiss.Model.predict(xTemp[NN_KDiss.xTrainingVar]) ) / InputData.MultFact * InputData.DissCorrFactor
    iIdxVec                  = [i for i in range(NLevels) if (KDiss[i,0] > MinValue)]
    #KDissVec[iIdxVec]  = KDiss[iIdxVec,0] 

    csvkinetics_KDiss        = write_predictiondata(KineticFile_KDiss, csvkinetics_KDiss, 0, iIdxVec, KDiss[iIdxVec,0])


    #===================================================================================================================================
    ### Closing Files for Rates
    csvkinetics_KDiss = write_predictiondata(KineticFile_KDiss, csvkinetics_KDiss, -2, None, None)


    return KDissVec

#=======================================================================================================================================



#=======================================================================================================================================
def write_predictiondata(KineticFile, csvkinetics, iFlg, iLevelVec, KVec):

    Mol1_Name  = 'O2'
    Atom1_Name = 'O'
    Atom2_Name = 'O'
    Atom3_Name = 'O'

    if (iFlg == 0):
        for iLevel in range(len(iLevelVec)): 
            ProcName = Mol1_Name + '(' + str(iLevel+1) + ')+' + Atom1_Name + '=' + Atom1_Name + '+' + Atom2_Name + '+' + Atom3_Name
            Line     = ProcName + ':%.4e,+0.0000E+00,+0.0000E+00,2\n' % KVec[iLevel]
            csvkinetics.write(Line)

    elif (iFlg == -1):
        print('[SurQCT]:   Writing Kinetics in File: ' + KineticFile )
        csvkinetics  = open(KineticFile, 'w')

    elif (iFlg == -2):
        print('[SurQCT]:   Closing Kinetics File: ' + KineticFile )
        csvkinetics.close()


    return csvkinetics

#=======================================================================================================================================
