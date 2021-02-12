import tensorflow as tf
import numpy      as np
import time
import os
import shutil
from scipy.integrate import ode
from pyDOE import *
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import sys
import seaborn as sns
import pandas     as pd

from Reading  import read_levelsdata, read_kdissdata


def generate_data(InputData):

    xVarsVec         = InputData.xVarsVec
    PathToLevelsFile = InputData.PathToLevelsFile
    PathToHDF5File   = InputData.PathToHDF5File


    #########################################################################################################################
    ### Using PANDAS

    ### Loading Input and Output for Training 
    TTranVec         = InputData.TTranVecTrain
    NTTran           = len(InputData.TTranVecTrain)

    LevelsData              = read_levelsdata(PathToLevelsFile[0], xVarsVec, 1)
    NLevels                 = LevelsData.shape[0]
    TTran                   = np.ones(NLevels) * TTranVec[0]
    DataSet                 = LevelsData
    DataSet['TTran']        = TTran
    KDiss                   = read_kdissdata(PathToHDF5File, TTranVec[0], TTranVec[0])
    DataSet['log10(KDiss)'] = KDiss
    DataSet = DataSet[DataSet['log10(KDiss)'] > -17.0] 
    for iT in range(1, NTTran):
        LevelsData                  = read_levelsdata(PathToLevelsFile[0], xVarsVec, 1)
        TTran                       = np.ones(NLevels) * TTranVec[iT]
        DataSetTemp                 = LevelsData
        DataSetTemp['TTran']        = TTran
        KDiss                       = read_kdissdata(PathToHDF5File, TTranVec[iT], TTranVec[iT])
        DataSetTemp['log10(KDiss)'] = KDiss
        DataSetTemp                 = DataSetTemp[DataSetTemp['log10(KDiss)'] > -17.0] 
        DataSet                     = DataSet.append(DataSetTemp)


    TrainData = DataSet.sample(frac=(1.0-InputData.TestPerc/100.0), random_state=3)
    TestData  = DataSet.drop(TrainData.index)

    x_train = TrainData.copy()
    x_train.pop('log10(KDiss)')
    x_test  = TestData.copy()
    x_test.pop('log10(KDiss)')

    y_train = TrainData[['log10(KDiss)', 'TTran']]
    y_test  = TestData[['log10(KDiss)', 'TTran']]



    ### Loading Input and Output for Testing 
    TTranVec         = InputData.TTranVecTest
    NTTran           = len(InputData.TTranVecTest)

    LevelsData       = read_levelsdata(PathToLevelsFile[0], xVarsVec, 1)
    NLevels          = LevelsData.shape[0]
    TTran            = np.ones(NLevels) * TTranVec[0]
    DataSet          = LevelsData
    DataSet['TTran'] = TTran
    KDiss            = read_kdissdata(PathToHDF5File, TTranVec[0], TTranVec[0])
    DataSet['log10(KDiss)'] = KDiss
    for iT in range(1, NTTran):
        LevelsData           = read_levelsdata(PathToLevelsFile[0], xVarsVec, 1)
        TTran                = np.ones(NLevels) * TTranVec[iT]
        DataSetTemp          = LevelsData
        DataSetTemp['TTran'] = TTran
        KDiss                = read_kdissdata(PathToHDF5File, TTranVec[iT], TTranVec[iT])
        DataSetTemp['log10(KDiss)'] = KDiss
        DataSet = DataSet.append(DataSetTemp)

    x_all = DataSet.copy()
    x_all.pop('log10(KDiss)')
    y_all = DataSet[['log10(KDiss)', 'TTran']]



    ### Loading Input and Output for Testing 
    TTranVec         = InputData.TTranVecExtra
    NTTran           = len(InputData.TTranVecExtra)

    LevelsData       = read_levelsdata(PathToLevelsFile[0], xVarsVec, 1)
    NLevels          = LevelsData.shape[0]
    TTran            = np.ones(NLevels) * TTranVec[0]
    DataSet          = LevelsData
    DataSet['TTran'] = TTran
    for iT in range(1, NTTran):
        LevelsData           = read_levelsdata(PathToLevelsFile[0], xVarsVec, 1)
        TTran                = np.ones(NLevels) * TTranVec[iT]
        DataSetTemp          = LevelsData
        DataSetTemp['TTran'] = TTran
        DataSet = DataSet.append(DataSetTemp)

    x_extra = DataSet.copy()



    TrainData = (x_train, y_train)
    TestData  = (x_test,  y_test)
    AllData   = (x_all,   y_all)
    ExtraData = (x_extra)

    return InputData, TrainData, TestData, AllData, ExtraData