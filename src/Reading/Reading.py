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
    KInel = Data[...]

    KOther = []
    for iProc in range(2, NProcTypes):
        ExchStr    = "Exch_" + str(iProc-1)
        Data       = grp[ExchStr] 
        KOtherTemp = Data[...]
        KOther.append(KOtherTemp)

    f.close()   


    # if (InputData.LossFunction == 'mean_squared_logarithmic_error'):
    #     KExcit = KInel * InputData.MultFact
    #     KExch  = 0.0
    # else:
    #     #KExcit = np.log10(KInel + KOther[0] + 1e-20)
    #     KExcit = np.log(KInel + 1e-20)
    #     KExch  = 0.0      
    KExcit = KInel * InputData.MultFact  
    KExch  = 0.0     

    return KExcit, KExch
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
