import os
import sys
import tensorflow as tf
import numpy      as np


if __name__ == "__main__": 

    WORKSPACE_PATH = os.environ['WORKSPACE_PATH']
    SurQCTFldr     = WORKSPACE_PATH + '/SurQCT/surqct/'


    print("\n======================================================================================================================================")
    print(" TensorFlow version: {}".format(tf.__version__))
    print(" Eager execution: {}".format(tf.executing_eagerly()))


    ##==============================================================================================================
    print("\n[SurQCT]: Loading Modules and Functions ...")

    sys.path.insert(0, SurQCTFldr  + '/src/Reading/')
    # from Reading import read_data, read_losseshistory
    sys.path.insert(0, SurQCTFldr  + '/src/Plotting/')
    from Plotting import plot_losseshistory
    # sys.path.insert(0, SurQCTFldr  + '/src/Saving/')
    # from Saving import save_parameters, save_data


    if (len(sys.argv) > 1):
        InputFile = sys.argv[1]
        print("[SurQCT]:   Calling SurQCT with Input File = ", InputFile)
        sys.path.insert(0, InputFile)
    else:
        InputFile = SurQCTFldr + '/src/InputData/'
        print("[SurQCT]:   Calling SurQCT with the PRESET Input File Located in " + InputFile )
        sys.path.insert(0, InputFile)
    ##--------------------------------------------------------------------------------------------------------------


    ##==============================================================================================================
    print("\n[SurQCT]: Keep Loading Modules and Functions...")
    from SurQCT_Input import inputdata

    print("\n[SurQCT]: Initializing Input ...")
    InputData    = inputdata(WORKSPACE_PATH, SurQCTFldr)
    ##--------------------------------------------------------------------------------------------------------------


    ##==============================================================================================================
    print("\n[SurQCT]: Loading Final Modules ... ")

    sys.path.insert(0, SurQCTFldr  + '/src/Model/' + InputData.ApproxModel + '/')
    from Model import model
    # if (InputData.ApproxModel == 'FNN'):
    #     from Model import FNN

    sys.path.insert(0, SurQCTFldr  + '/src/RatesType/' + InputData.RatesType + '/')
    from RatesType import generate_data
    # Generating Data
    InputData, TrainData, TestData, AllData, ExtraData = generate_data(InputData)
    ##--------------------------------------------------------------------------------------------------------------


    PathToFldr = InputData.PathToRunFld
    try:
        os.makedirs(PathToFldr)
    except OSError as e:
        pass


    ### Initializing the Surrogate Model
    NN = model(InputData, TrainData)

    ### Training the Surrogate Model
    if (InputData.TrainIntFlg >= 1):
        History = NN.train(InputData)

    ### Plotting the Losses History
    plot_losseshistory(InputData, History)


    # ### Saving the Surrogate Model Parameters
    # if (InputData.WriteParamsIntFlg >= 1):
    #     save_parameters(NN, InputData)


    ### Generating Test Results
    if (InputData.TestIntFlg >= 1):
        xAll   = AllData[0]
        yAll   = AllData[1]
        xExtra = ExtraData


        for TTran in InputData.TTranVecTest:
            MaskVec = (xAll['TTran'] == TTran)
            xPred   = xAll.loc[MaskVec]
            yPred   = NN.Model.predict(xPred)
            yData   = yAll.loc[MaskVec]

            ### Plotting Test Results
            if (InputData.PlotIntFlg >= 1):

                PathToFldr = InputData.PathToFigFld
                try:
                    os.makedirs(PathToFldr)
                except OSError as e:
                    pass
                NN.plot_prediction(InputData, yData, yPred, TTran)


        for TTran in InputData.TTranVecExtra:
            MaskVec = (xExtra['TTran'] == TTran)
            xPred   = xExtra.loc[MaskVec]
            yPred   = NN.Model.predict(xPred)
            yData   = []

            ### Plotting Test Results
            if (InputData.PlotIntFlg >= 1):

                PathToFldr = InputData.PathToFigFld
                try:
                    os.makedirs(PathToFldr)
                except OSError as e:
                    pass
                NN.plot_prediction(InputData, yData, yPred, TTran)


    #         ### Saving Test Data
    #         if (InputData.WriteDataIntFlg >= 1):

    #             PathToFldr = InputData.PathToDataFld
    #             try:
    #                 os.makedirs(PathToFldr)
    #             except OSError as e:
    #                 pass
    #             PredData       = tf.concat([tf.expand_dims(tTest,axis=1), xPred], axis=1)
    #             PathToPredData = PathToFldr + '/TestCase' + str(iTestCase+1) + '.csv.Final'
    #             save_data(PathToPredData, PredData)

    #         ### Producing the Video of the Treaning History
    #         if ((InputData.WriteDataIntFlg == 2) and (InputData.PlotIntFlg >= 1)):
                
    #             DataFile     = InputData.PathToDataFld + '/TestCase'  + str(iTestCase+1) + '.csv.Data'
    #             tData, xData = read_data(DataFile, InputData.xDim)
    #             PredFile     = InputData.PathToDataFld + '/TestCase' + str(iTestCase+1) + '.csv.'
    #             video_history(InputData, iTestCase, tData, xData, PredFile, 1e10)
