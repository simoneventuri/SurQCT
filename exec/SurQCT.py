import os
import shutil
import sys
import tensorflow                             as tf
import numpy                                  as np


if __name__ == "__main__": 

    WORKSPACE_PATH = os.environ['WORKSPACE_PATH']
    SurQCTFldr     = WORKSPACE_PATH + '/SurQCT/surqct/'


    print("\n======================================================================================================================================")
    print(" TensorFlow version: {}".format(tf.__version__))
    print(" Eager execution: {}".format(tf.executing_eagerly()))


    #===================================================================================================================================
    print("\n[SurQCT]: Loading Modules and Functions ...")

    sys.path.insert(0, SurQCTFldr  + '/src/Reading/')
    sys.path.insert(0, SurQCTFldr  + '/src/Plotting/')
    from Plotting import plot_losseshistory


    if (len(sys.argv) > 1):
        InputFile = sys.argv[1]
        print("[SurQCT]:   Calling SurQCT with Input File = ", InputFile)
        sys.path.insert(0, InputFile)
    else:
        InputFile = SurQCTFldr + '/src/InputData/'
        print("[SurQCT]:   Calling SurQCT with the PRESET Input File Located in " + InputFile )
        sys.path.insert(0, InputFile)

    #===================================================================================================================================



    #===================================================================================================================================
    print("\n[SurQCT]: Keep Loading Modules and Functions...")
    from SurQCT_Input import inputdata

    print("\n[SurQCT]: Initializing Input ...")
    InputData    = inputdata(WORKSPACE_PATH, SurQCTFldr)

    try:
        os.makedirs(InputData.PathToRunFld)
    except OSError as e:
        pass
    
    Prefix = 'Run_'
    if (InputData.NNRunIdx == 0):
        if (len([x for x in os.listdir(InputData.PathToRunFld) if 'Run_' in x]) > 0):
            InputData.NNRunIdx = str(np.amax( np.array( [int(x[len(Prefix):]) for x in os.listdir(InputData.PathToRunFld) if Prefix in x], dtype=int) ) + 1)
        else:
            InputData.NNRunIdx = 1

    InputData.PathToRunFld = InputData.PathToRunFld+'/'+Prefix+str(InputData.NNRunIdx)
    try:
        os.makedirs(InputData.PathToRunFld)
    except OSError as e:
        pass

    try:
        shutil.copyfile(InputFile+'/SurQCT_Input.py', InputData.PathToRunFld+'/SurQCT_Input.py')
    except OSError as e:
        pass
    
    InputData.PathToFigFld = InputData.PathToRunFld+'/'+InputData.PathToFigFld
    try:
        os.makedirs(InputData.PathToFigFld)
    except OSError as e:
        pass

    InputData.PathToParamsFld = InputData.PathToRunFld+'/'+InputData.PathToParamsFld

    #===================================================================================================================================


    #===================================================================================================================================
    print("\n[SurQCT]: Loading Final Modules ... ")

    sys.path.insert(0, SurQCTFldr  + '/src/Model/' + InputData.ApproxModel + '/')
    from Model import model

    sys.path.insert(0, SurQCTFldr  + '/src/RatesType/' + InputData.RatesType + '/')
    from RatesType import generate_trainingdata, plot_prediction, generate_predictiondata

    #===================================================================================================================================



    #===================================================================================================================================
    print("\n[SurQCT]: Generating Data ... ")

    InputData, TrainData, ValidData, AllData, TestData, ExtraData = generate_trainingdata(InputData)

    #===================================================================================================================================



    #===================================================================================================================================
    print('\n[SurQCT]: Initializing ML Model ... ')

    NN = model(InputData, InputData.PathToRunFld, TrainData, ValidData)

    #===================================================================================================================================



    #===================================================================================================================================
    if (InputData.TrainIntFlg > 0):


        if (InputData.TrainIntFlg == 1):
            print('\n[SurQCT]: Reading the ML Model Parameters ... ')

            NN.load_params(InputData.PathToParamsFld)


        print('\n[SurQCT]: Training the ML Model ... ')

        History = NN.train(InputData)


        print('\n[SurQCT]: Plotting the Losses Evolution ... ')

        plot_losseshistory(InputData, History)


    else:

        print('\n[SurQCT]: Reading the ML Model Parameters ... ')

        NN.load_params(InputData.PathToParamsFld)

    #===================================================================================================================================



    #===================================================================================================================================

    # if (InputData.PlotIntFlg >= 1):

       # print('\n[SurQCT]: Evaluating the ML Model at the Training Data and Plotting the Results ... ')
       
       # xAll      = AllData[0]
       # yAll      = AllData[1]
       # yPred     = NN.Model.predict(xAll[NN.xTrainingVar])

       # plot_prediction(InputData, 'Train', InputData.TTranVecTrain, xAll, yAll, yPred)

    #===================================================================================================================================



    # #===================================================================================================================================

    if (InputData.TestIntFlg >= 1):

        if (InputData.PlotIntFlg >= 1):

             print('\n[SurQCT]: Evaluating the ML Model at the Test Data and Plotting the Results ... ')

             xTest     = TestData[0]
             yTest     = TestData[1]
             yPred     = NN.Model.predict(xTest[NN.xTrainingVar])

             plot_prediction(InputData, 'Test', InputData.TTranVecTest, xTest, yTest, yPred)

    # #===================================================================================================================================



    #===================================================================================================================================

    if (InputData.TestIntFlg >= 1):

        if (InputData.PlotIntFlg >= 1):

            print('\n[SurQCT]: Evaluating the ML Model at the Test Data and Plotting the Results ... ')

            xExtra    = ExtraData
            yPred     = NN.Model.predict(xExtra[NN.xTrainingVar])
            yData     = []

            plot_prediction(InputData, 'Extra', InputData.TTranVecExtra, xExtra, yData, yPred)

    #===================================================================================================================================


    #===================================================================================================================================

#    if (InputData.PredictIntFlg >= 1):
   
#        print('\n[SurQCT]: Generating Rate Matrixes ... ')

#        TTran = 10000.0
#        KExcitMat = generate_predictiondata(InputData, NN, TTran)
       # print(KExcitMat)
       # print(KExcitMat[9,:])

    #===================================================================================================================================
