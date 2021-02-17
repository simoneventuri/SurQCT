import os
import sys
import tensorflow                             as tf
import numpy                                  as np


if __name__ == "__main__": 


    SurQCTFldr        = '/home/venturi/WORKSPACE/SurQCT/surqct/'

    TTranVec          = [6000.0, 10000.0, 12000.0]

    PathToLevelsFile  = ['/home/venturi/WORKSPACE/Air_Database/Run_0D/database/levels/O2.csv']
    KineticFldr       = '/home/venturi/WORKSPACE/Air_Database/Run_0D/database_HighAccuracy/kinetics/O3_UMN/'



    for TTran in (TTranVec):



        sys.path.insert(0, SurQCTFldr  + '/src/RatesType/KExcit/')
        from RatesType import generate_predictiondata

        KInelMat, KExchMat = generate_predictiondata(SurQCTFldr, PathToLevelsFile, TTran, KineticFldr)



        # sys.path.insert(0, SurQCTFldr  + '/src/RatesType/KDiss/')
        # from RatesType import generate_predictiondata

        # KDissVec = generate_predictiondata(SurQCTFldr, PathToLevelsFile, TTran, KineticFldr)
