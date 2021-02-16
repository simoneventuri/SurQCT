import os
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
    from Reading import sample_initiallevels

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
    print("\n[SurQCT]: Keep Loading Modules and Functions ...")
    from SurQCT_Input import inputdata

    print("\n[SurQCT]: Initializing Input ...")
    InputData    = inputdata(WORKSPACE_PATH, SurQCTFldr)

    #===================================================================================================================================



    #===================================================================================================================================
    print("\n[SurQCT]: Sampling Groups ...")

    iSeed = 23
    iIdxVec = sample_initiallevels(InputData.PathToGrouping, 1, iSeed)

    print("\n[SurQCT]: iIdxVec = ", iIdxVec)
    
    #===================================================================================================================================
