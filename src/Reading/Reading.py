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
# Reading Levels Data 
def read_diatdata(DataFile, Molecule, TTranVecTrain, TTranVecTest):
    print('[SurQCT]:   Reading Molecular Levels Data from: ' + DataFile)

    # Extracting all the rot-vib levels
    xMat           = pd.read_csv(DataFile, delim_whitespace=True, skiprows=15, header=None)
    xMat.columns   = ['vqn','jqn','EInt','egam','rMin','rMax','VMin','VMax','Tau','ri','ro']    

    # Shifting Energies so that Zero is the Min of Diatomic Potential at J=0
    xMat['EInt']   = ( xMat['EInt'].to_numpy() - np.amin(xMat['VMax'].to_numpy()) ) * 27.211399
    xMat['VMax']   = ( xMat['VMax'].to_numpy() - np.amin(xMat['VMax'].to_numpy()) ) * 27.211399
    xMat['VMin']   = ( xMat['VMin'].to_numpy() - np.amin(xMat['VMax'].to_numpy()) ) * 27.211399

    xMat['g']      = compute_degeneracy(xMat['jqn'].to_numpy(int), Molecule) 

    kB = 8.617333262e-5
    
    for TTran in TTranVecTrain:
        Str       = 'q_'+str(int(TTran))
        xMat[Str] = xMat['g'].to_numpy() * np.exp( - xMat['EInt'].to_numpy() / (kB*TTran) )

    for TTran in TTranVecTest:
        Str       = 'q_'+str(int(TTran))
        xMat[Str] = xMat['g'].to_numpy() * np.exp( - xMat['EInt'].to_numpy() / (kB*TTran) )

    return xMat


def compute_degeneracy(jqn, Molecule):

    if (Molecule == 'N2'):
        if (jqn % 2 == 0):
            g = 6*(2*jqn + 1)
        else:
            g = 3*(2*jqn + 1)
    elif (Molecule == 'O2'):
        g = (2*jqn + 1)
    elif (Molecule == 'NO'):
        g = (2*jqn + 1)
    else:
        print('\n\nDEGENERACY NOT IMPLEMENTED FOR THIS MOLECULE!\n\n')

    return g
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
