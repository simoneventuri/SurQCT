import sys
import os
import errno
import shutil
import h5py
import tensorflow                             as tf
import numpy                                  as np
import pandas                                 as pd
from os                                   import path


#=======================================================================================================================================
# Reading Levels Data 
def read_levelsdata(DataFile, xVarsVec, Suffix):
    print('[SurQCT]:   Reading Molecular Levels Data from: ' + DataFile)

    # Extracting all the rot-vib levels
    xMat         = pd.read_csv(DataFile, header=0, skiprows=0)
    xMat         = xMat.astype('float64')
    xMat         = xMat[xVarsVec]
    xMat.columns = [(VarName + Suffix) for VarName in xMat.columns]
    # xMat  = xMat.apply(pd.to_numeric, errors='coerce')
    # xMat  = np.array(xMat)                                                               
    # xMat  = tf.convert_to_tensor(xMat, dtype=tf.float64, name='xData')

    return xMat

#=======================================================================================================================================



#=======================================================================================================================================
# Reading Levels-to-Group Mapping
def sample_initiallevels(PathToGrouping, NSamplesPerGroup, iSeed):
    print('[SurQCT]:       Reading Grouping from File: ' + PathToGrouping + ' and Sampling ' + str(NSamplesPerGroup) + ' Levels per Group with Seed ' + str(iSeed))

    xMat    = pd.read_csv(PathToGrouping, header=0, skiprows=0)
    iIdxVec = xMat.groupby('Group', group_keys=False).apply(lambda df: df.sample(NSamplesPerGroup, random_state=iSeed))['#Idx'].values
  
    return iIdxVec
#=======================================================================================================================================



#=======================================================================================================================================
# Reading Sampled Levels
def read_sampledinitiallevels(PathToSampledLevels, TTran):

    PathToSampledLevels = PathToSampledLevels + str(int(TTran)) + 'K.csv'
    print('[SurQCT]:       Reading Sampled Initial Levels List from File: ' + PathToSampledLevels)

    iIdxVec             = pd.read_csv(PathToSampledLevels, header=0)
    iIdxVec             = np.squeeze(iIdxVec.to_numpy())
  
    return iIdxVec

#=======================================================================================================================================
