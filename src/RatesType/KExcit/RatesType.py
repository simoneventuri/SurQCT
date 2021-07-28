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
from tqdm                                 import tqdm
from os                                   import path


#=======================================================================================================================================
def generate_trainingdata(InputData):

    from Reading  import read_levelsdata, read_diatdata, sample_initiallevels, read_sampledinitiallevels


    #===================================================================================================================================
    OtherVar           = InputData.OtherVar
    xVarsVec_i         = InputData.xVarsVec_i
    xVarsVec_Delta     = InputData.xVarsVec_Delta
    xVarsVec           = list(set(xVarsVec_i) | set(xVarsVec_Delta))
    print('[SurQCT]:   Reading Variables: ', xVarsVec)

    InputData.MultFact = 1.e+09
    MinValueTrain      = 1.e-16 * InputData.MultFact
    MinValueTest       = 1.e-16 * InputData.MultFact
    NoiseSD            = 1.e-13 * InputData.MultFact

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

        DiatDataTemp = read_diatdata(InputData.PathToDiatFile[iMol], InputData.Molecules[iMol], InputData.TTranVecTrain, InputData.TTranVecTest)
        DiatData.append(DiatDataTemp)
        
        NLevelsTemp    = LevelsDataTemp.shape[0]
        NLevels.append(NLevelsTemp)


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
        KInelMat, KExchMatList   = read_kexcitdata(InputData, InputData.PathToHAHDF5File, TTranVec[iT], TTranVec[iT], 3)
        if (  InputData.ExcitType == 'KInel'):
            KMatoI                    = KInelMat
        elif (InputData.ExcitType == 'KExch'):
            KMatoI                    = KExchMatList[0]
        elif (InputData.ExcitType == 'KExcit'):
            KMatoI                    = KInelMat + KExchMatList[0]


        ### Deciding Initial Levels LIst        
        if   (InputData.iLevelsIntFlg == 1):
            iIdxVec = InputData.iLevelsVec
        elif (InputData.iLevelsIntFlg == 2):
            np.random.seed(InputData.iLevelsSeedsVec[0])
            iIdxVec = np.random.choice(NLevels[0], InputData.NiLevelsSampled, replace=False)
        elif (InputData.iLevelsIntFlg == 3):
            NSamplesPerGroup = 3
            iIdxVec          = sample_initiallevels(InputData.PathToGrouping, NSamplesPerGroup, InputData.iLevelsSeedsVec[iT])
        elif (InputData.iLevelsIntFlg == 4):
            iIdxVec = read_sampledinitiallevels(InputData.PathToSampledLevels, TTranVec[iT])
        print('[SurQCT]:       Vector of Initial Levels: iIdxVec = ', iIdxVec)
        iIdxVec = iIdxVec - 1

        

        ### Loop on Initial States
        Str = 'q_'+str(int(TTranVec[iT]))
        for iIdx in iIdxVec:

            ### Selecting only Final States with EXOTHERMIC KExit > MinValueTrain 
            if (InputData.ExoEndoFlg):
                jIdxVec           = [jIdx for jIdx, x in enumerate(KMatoI[iIdx,:] > MinValueTrain) if (x and DiatData[1]['EInt'].to_numpy()[jIdx] < DiatData[0]['EInt'].to_numpy()[iIdx])]
            else:
                jIdxVec           = [jIdx for jIdx, x in enumerate(KMatoI[iIdx,:] > MinValueTrain) if (x and DiatData[1][Str].to_numpy()[jIdx]    > DiatData[0][Str].to_numpy()[iIdx])]
            jNLevels              = len(jIdxVec)
            kIdxVec               = [iIdx]*jNLevels
            

            ### Appending Vertically
            iIdxData              = iIdxData.append(pd.DataFrame({'Idx_i': kIdxVec}))
            jIdxData              = jIdxData.append(pd.DataFrame({'Idx_j': jIdxVec}))

            TTran                 = np.ones((jNLevels)) * TTranVec[iT]
            TTranData             = TTranData.append(pd.DataFrame({'TTran': TTran}))

            KExcitData            = KExcitData.append(pd.DataFrame({'KExcit': KMatoI[iIdx, jIdxVec]}))
            
            iLevelsDataTemp       = LevelsData[0].iloc[kIdxVec,:].copy()
            iLevelsDataTemp.index = np.arange(len(TTran))
            iLevelsData           = iLevelsData.append(iLevelsDataTemp[xVarsVec_i])

            jLevelsDataTemp       = LevelsData[1].iloc[jIdxVec,:].copy() 
            jLevelsDataTemp       = jLevelsDataTemp   
            jLevelsDataTemp.index = np.arange(len(TTran))
            if (OtherVar == '_Delta'):
                jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
            else:
                jLevelsDataTemp   = jLevelsDataTemp
            jLevelsData           = jLevelsData.append(jLevelsDataTemp[xVarsVec_Delta])

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

    iIdxData         = pd.DataFrame(columns = ['Idx_i'])
    jIdxData         = pd.DataFrame(columns = ['Idx_j'])
    iLevelsData      = pd.DataFrame(columns = xVarsVec)
    jLevelsData      = pd.DataFrame(columns = xVarsVec)
    TTranData        = pd.DataFrame(columns = ['TTran'])
    KExcitData       = pd.DataFrame(columns = ['KExcit'])
    for iT in range(NTTran):

        ### Reading Rates at Temperature TTranVec[iT]
        KInelMat, KExchMatList   = read_kexcitdata(InputData, InputData.PathToHDF5File, TTranVec[iT], TTranVec[iT], 3)
        if (  InputData.ExcitType == 'KInel'):
            KMatoI                    = KInelMat
        elif (InputData.ExcitType == 'KExch'):
            KMatoI                    = KExchMatList[0]
        elif (InputData.ExcitType == 'KExcit'):
            KMatoI                    = KInelMat + KExchMatList[0]


        Str     = 'q_'+str(int(TTranVec[iT]))
        iIdxVec = InputData.iLevelsVecTest
        for iIdx in iIdxVec:
            if (InputData.ExoEndoFlg):
                jIdxVec           = [jIdx for jIdx, x in enumerate(KMatoI[iIdx,:] > MinValueTrain) if (x and DiatData[1]['EInt'].to_numpy()[jIdx] < DiatData[0]['EInt'].to_numpy()[iIdx])]
            else:
                jIdxVec           = [jIdx for jIdx, x in enumerate(KMatoI[iIdx,:] > MinValueTrain) if (x and DiatData[1][Str].to_numpy()[jIdx]    > DiatData[0][Str].to_numpy()[iIdx])]
            jNLevels              = len(jIdxVec)
            kIdxVec               = [iIdx]*jNLevels
    
            iIdxData              = iIdxData.append(pd.DataFrame({'Idx_i': kIdxVec}))
            jIdxData              = jIdxData.append(pd.DataFrame({'Idx_j': jIdxVec}))

            TTran                 = np.ones((jNLevels)) * TTranVec[iT]
            TTranData             = TTranData.append(pd.DataFrame({'TTran': TTran}))

            KExcitData            = KExcitData.append(pd.DataFrame({'KExcit': np.log( KMatoI[iIdx, jIdxVec] )}))
            
            iLevelsDataTemp       = LevelsData[0].iloc[kIdxVec,:].copy()
            iLevelsDataTemp.index = np.arange(len(TTran))
            iLevelsData           = iLevelsData.append(iLevelsDataTemp[xVarsVec_i])

            jLevelsDataTemp       = LevelsData[1].iloc[jIdxVec,:].copy()   
            jLevelsDataTemp.index = np.arange(len(TTran))
            if (OtherVar == '_Delta'):
                jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
            else:
                jLevelsDataTemp   = jLevelsDataTemp
            jLevelsData           = jLevelsData.append(jLevelsDataTemp[xVarsVec_Delta])
            
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

        iIdxVec = InputData.iLevelsVecTest
        for iIdx in iIdxVec:
            jIdxVec               = np.arange(NLevels[1])
            jNLevels              = len(jIdxVec)
            kIdxVec               = [iIdx]*jNLevels
    
            iIdxData              = iIdxData.append(pd.DataFrame({'Idx_i': kIdxVec}))
            jIdxData              = jIdxData.append(pd.DataFrame({'Idx_j': jIdxVec}))

            TTran                 = np.ones((jNLevels)) * TTranVec[iT]
            TTranData             = TTranData.append(pd.DataFrame({'TTran': TTran}))
            
            iLevelsDataTemp       = LevelsData[0].iloc[kIdxVec,:].copy()
            iLevelsDataTemp.index = np.arange(len(TTran))
            iLevelsData           = iLevelsData.append(iLevelsDataTemp[xVarsVec_i])

            jLevelsDataTemp       = LevelsData[1].iloc[jIdxVec,:].copy()  
            jLevelsDataTemp.index = np.arange(len(TTran))
            if (OtherVar == '_Delta'):
                jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
            else:
                jLevelsDataTemp   = jLevelsDataTemp
            jLevelsData           = jLevelsData.append(jLevelsDataTemp[xVarsVec_Delta])
            
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
# Reading Excitation Rates Data 
def read_kexcitdata(InputData, PathToHDF5File, TTra, TInt, NProcTypes):
    print('[SurQCT]:       Reading HDF5 File from: ' + PathToHDF5File + ' for Excitation Rates at Temperature ' + str(int(TTra)) + 'K')

    HDF5Exist_Flg = path.exists(PathToHDF5File)
    if (HDF5Exist_Flg):
        f = h5py.File(PathToHDF5File, 'a')
    else:
        f = {'key': 'value'}

    TStr = 'T_' + str(int(TTra)) + '_' + str(int(TInt)) + '/Rates/'
    grp  = f[TStr]

    Data  = grp["Inel"]
    KInel = Data[...] * InputData.MultFact  

    KOther = []
    for iProc in range(2, NProcTypes):
        ExchStr    = "Exch_" + str(iProc-1)
        Data       = grp[ExchStr] 
        KOtherTemp = Data[...]
        KOther.append(KOtherTemp * InputData.MultFact)

    f.close()   


    return KInel, KOther
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
            FigPath = InputData.PathToFigFld + '/' + CaseType + 'Case_T' + str(int(TTran)) + 'K_Level' + str(iIdx+1) + '.png'
            fig.savefig(FigPath, dpi=600)
            plt.show()
            #plt.close()

#=======================================================================================================================================



# #=======================================================================================================================================
# def plot_prediction(InputData, CaseType, TTranVec, xPred, yData, yPred):

#     import matplotlib.tri as tri
#     import matplotlib.pyplot as plt

#     TrainingVar = InputData.RatesType
#     Idxs        = xPred.Idx_i.unique()
    
#     for TTran in (TTranVec):

#         for iIdx in Idxs:
#             kIdx1 = xPred.index[(xPred['Idx_i'] == iIdx)].tolist()
#             kIdx2 = xPred.index[(xPred['TTran_i'] == TTran)].tolist()
#             kIdx  = list(set(kIdx1) & set(kIdx2))

#             if (len(yData)>0):
#                 fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(20,20))
#                 ax1.tricontour( xPred['EVib_Delta'][kIdx], xPred['ERot_Delta'][kIdx], np.log10(np.exp(yData[TrainingVar][kIdx])/InputData.MultFact), 15, linewidths=0.5, colors='k')
#                 ax1.tricontourf(xPred['EVib_Delta'][kIdx], xPred['ERot_Delta'][kIdx], np.log10(np.exp(yData[TrainingVar][kIdx])/InputData.MultFact), 15)
#                 plt.xlabel('$\Delta \epsilon_v$')
#                 plt.ylabel("$\Delta \epsilon_J$")
#             else:
#                 fig, (ax2) = plt.subplots(1)
#                 plt.ylabel("$\Delta \epsilon_J$")
#             ax2.tricontour(     xPred['EVib_Delta'][kIdx], xPred['ERot_Delta'][kIdx], np.log10(np.exp(np.squeeze(yPred[kIdx]))/InputData.MultFact),              15, linewidths=0.5, colors='k')
#             ax2.tricontourf(    xPred['EVib_Delta'][kIdx], xPred['ERot_Delta'][kIdx], np.log10(np.exp(np.squeeze(yPred[kIdx]))/InputData.MultFact),              15)

#             plt.xlabel('$\Delta \epsilon_v$')
#             fig.suptitle('Excitation Rates at T = ' + str(int(TTran)) + 'K, i = ' + str(iIdx+1))
#             FigPath = InputData.PathToFigFld + '/' + CaseType + 'Case_T' + str(int(TTran)) + 'K_Level' + str(iIdx+1) + '_CPlot.png'
#             fig.savefig(FigPath, dpi=600)
#             plt.show()
#             #plt.close()

# #=======================================================================================================================================



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
    InputData.RatesType        = 'KExcit'
    InputData.xVarsVec         = ['EVib','ERot','rMin','rMax','VMin','VMax','Tau','ri','ro'] #['EVib','ERot','ri','ro'] 
    InputData.OtherVar         = '_Delta'
    InputData.ApproxModel      = 'DotNet'

    OtherVar                   = InputData.OtherVar
    xVarsVec                   = InputData.xVarsVec

    InputData.MultFact         = 1.e+09
    MinValue                   = 1.e-16

    #===================================================================================================================================



    #===================================================================================================================================
    print("\n[SurQCT]: Loading Final Modules ... ")

    sys.path.insert(0, SurQCTFldr  + '/src/Model/' + InputData.ApproxModel + '/')
    from Model import model

    #===================================================================================================================================



    #===================================================================================================================================
    print('\n[SurQCT]: Initializing ML Model for KInel and Loading its Parameters ... ')

    PathToRunFld              = SurQCTFldr + '/../' + InputData.RatesType + '/all_temperatures_nondim/KExcit_Test' + str(InputData.NNRunIdx)
    InputData.PathToDataFld   = PathToRunFld + '/Data/'                                                               
    InputData.PathToParamsFld = PathToRunFld + '/Params/'                                                            

    NN_KInel     = model(InputData, PathToRunFld, None, None)
    NN_KInel.load_params(InputData.PathToParamsFld)


#    print('\n[SurQCT]: Initializing ML Model for KExch and Loading its Parameters ... ')
#
#    PathToRunFld              = SurQCTFldr + '/../' + InputData.RatesType + '/KExch_Test' + str(InputData.NNRunIdx)
#    InputData.PathToDataFld   = PathToRunFld + '/Data/'                                                               
#    InputData.PathToParamsFld = PathToRunFld + '/Params/'   
#
    NN_KExch     = model(InputData, PathToRunFld, None, None)
    NN_KExch.load_params(InputData.PathToParamsFld)

    #===================================================================================================================================



    #===================================================================================================================================
    print('\n[SurQCT]: Generating Rate Matrix at Translational Temperature: T = ' + str(int(TTran)) + 'K')


    #===================================================================================================================================
    ### Reading Levels Info of Initial and Final Molecules
    LevelsData = []
    NLevels    = []
    for iMol in range(NMolecules):
        LevelsDataTemp = read_levelsdata(InputData.PathToLevelsFile[iMol], xVarsVec, '')
        LevelsData.append(LevelsDataTemp)
        NLevelsTemp    = LevelsDataTemp.shape[0]
        NLevels.append(NLevelsTemp)


    #===================================================================================================================================
    ### Initializing Rates Matrix
    KInelMat = None #np.zeros((NLevels[0], NLevels[1]))
    KExchMat = None #np.zeros((NLevels[0], NLevels[1]))

    try:
        os.makedirs(KineticFldr)
    except OSError as e:
        pass


    PathToKineticFldr = KineticFldr + '/KExcit_Test' + str(InputData.NNRunIdx) + '/T' + str(int(TTran)) + 'K'
    try:
        os.makedirs(PathToKineticFldr)
    except OSError as e:
        pass
    
    #===================================================================================================================================
    ### Opening Files for Writing Rates
    KineticFile_KInel = PathToKineticFldr + '/Inel.dat'
    csvkinetics_KInel = write_predictiondata(KineticFile_KInel, None, -1, None, None, None)
    KineticFile_KExch = PathToKineticFldr + '/Exch_Type1.dat'
    csvkinetics_KExch = write_predictiondata(KineticFile_KExch, None, -1, None, None, None)


    ### Loop on Initial States
    for iIdx in tqdm(range(1, NLevels[0]), desc='[SurQCT]:     Generating Inelastic and Exchange Rate Matrixes'):
        time.sleep(0.02)
        jIdxVec               = np.arange(iIdx)
        jNLevels              = len(jIdxVec)
        kIdxVec               = [iIdx]*jNLevels
        

        TTranVec              = np.ones((jNLevels))*TTran
        TTranDataTemp         = pd.DataFrame({'TTran': TTranVec})
        TTranDataTemp.index   = jIdxVec

        iLevelsDataTemp       = LevelsData[0].iloc[kIdxVec,:].copy()
        iLevelsDataTemp.index = jIdxVec

        jLevelsDataTemp       = LevelsData[1].iloc[jIdxVec,:].copy()        
        if (OtherVar == '_Delta'):
            jLevelsDataTemp   = iLevelsDataTemp.subtract(jLevelsDataTemp) 
        else:
            jLevelsDataTemp   = jLevelsDataTemp
        jLevelsDataTemp.index = jIdxVec

        iLevelsData           = pd.concat([iLevelsDataTemp, TTranDataTemp], axis=1)
        iLevelsData.columns   = [(VarName + '_i') for VarName in iLevelsData.columns]
        jLevelsData           = pd.concat([jLevelsDataTemp, TTranDataTemp], axis=1)
        jLevelsData.columns   = [(VarName + OtherVar) for VarName in jLevelsData.columns]
        xTemp                 = pd.concat([iLevelsData, jLevelsData], axis=1)

        KInel                    = np.exp( NN_KInel.Model.predict(xTemp[NN_KInel.xTrainingVar]) ) / InputData.MultFact
        jIdxVec                  = [i for i in range(jNLevels) if (KInel[i,0] > MinValue)]
        #KInelMat[iIdx, jIdxVec]  = KInel[jIdxVec,0] 

        csvkinetics_KInel        = write_predictiondata(KineticFile_KInel, csvkinetics_KInel, 0, iIdx, jIdxVec, KInel[jIdxVec,0])


        KExch                    = np.exp( NN_KExch.Model.predict(xTemp[NN_KExch.xTrainingVar]) ) / InputData.MultFact
        jIdxVec                  = [i for i in range(jNLevels) if (KExch[i,0] > MinValue)]
        #KExchMat[iIdx, jIdxVec]  = KExch[jIdxVec,0] 
        
        csvkinetics_KExch        = write_predictiondata(KineticFile_KExch, csvkinetics_KExch, 0, iIdx, jIdxVec, KExch[jIdxVec,0])


    #===================================================================================================================================
    ### Closing Files for Rates
    csvkinetics_KInel = write_predictiondata(KineticFile_KInel, csvkinetics_KInel, -2, None, None, None)
    csvkinetics_KExch = write_predictiondata(KineticFile_KExch, csvkinetics_KExch, -2, None, None, None)


    return KInelMat, KExchMat
#    return KInelMat
#=======================================================================================================================================



#=======================================================================================================================================
def write_predictiondata(KineticFile, csvkinetics, iFlg, iLevel, jLevelVec, KVec):

    Mol1_Name  = 'O2'
    Atom1_Name = 'O'
    Mol2_Name  = 'O2'
    Atom2_Name = 'O'

    if (iFlg == 0):
        for i in range(len(jLevelVec)): 
            ProcName = Mol1_Name + '(' + str(iLevel+1) + ')+' + Atom1_Name + '=' + Mol2_Name + '(' + str(jLevelVec[i]+1) + ')+' + Atom2_Name
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
