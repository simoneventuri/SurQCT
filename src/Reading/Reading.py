import sys
import os, errno
import os.path
from os import path
import shutil

import tensorflow as tf
import pandas     as pd
import numpy      as np
import h5py


# Reading Levels Data 
def read_levelsdata(DataFile, xVarsVec, Indx):

    # Extracting all the rot-vib levels
    xMat         = pd.read_csv(DataFile, header=0, skiprows=0)
    xMat         = xMat[xVarsVec]
    xMat.columns = [(VarName + '_' + str(Indx)) for VarName in xMat.columns]
    # xMat  = xMat.apply(pd.to_numeric, errors='coerce')
    # xMat  = np.array(xMat)                                                               
    # xMat  = tf.convert_to_tensor(xMat, dtype=tf.float64, name='xData')

    return xMat


# Reading Dissociation Rates Data 
def read_kdissdata(PathToHDF5File, TTra, TInt):

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
    
    KDiss = np.log10(np.expand_dims(KDiss[:,0]+1.e-18, axis=1))
    #KDiss = tf.expand_dims(tf.convert_to_tensor(KDiss[:,0], dtype=tf.float64, name='yData'), axis=1)

    return KDiss


# Reading Excitation Rates Data 
def read_kexcitdata(PathToHDF5File, TTra, TInt, NProcTypes):

    HDF5Exist_Flg = path.exists(PathToHDF5File)
    if (HDF5Exist_Flg):
        f = h5py.File(PathToHDF5File, 'a')
    else:
        f = {'key': 'value'}

    TStr = 'T_' + str(int(TTra)) + '_' + str(int(TInt)) + '/Rates/'
    grp  = f[TStr]

    Data  = grp["Inel"]
    KInel = Data[...]

    KExch = []
    for iProc in range(2, NProcTypes):
        ExchStr  = "Exch_" + str(iProc-1)
        Data     = grp[ExchStr]
        KExch.append(Data[...])

    f.close()                                                          
  
    return KInel, KExch


# # Reading Training History 
# def read_losseshistory(HistoryFile):

#     # Extracting all the rot-vib levels
#     TempData   = pd.read_csv(HistoryFile, header=None, skiprows=0)
#     TempData   = TempData.apply(pd.to_numeric, errors='coerce')
#     Iter       = np.expand_dims(np.array(TempData[0]),axis=1)                                                              
#     Loss       = np.expand_dims(np.array(TempData[1]),axis=1)                                                              
#     MSE0       = np.expand_dims(np.array(TempData[2]),axis=1)                                                              
#     MSEf       = np.expand_dims(np.array(TempData[3]),axis=1)                                                              
#     MSEr       = np.expand_dims(np.array(TempData[4]),axis=1)                                                              
#     TimeTrain  = np.expand_dims(np.array(TempData[5]),axis=1)                                                              

#     return Iter, Loss, MSE0, MSEf, MSEr, TimeTrain



# ### Reading Parameters from HDF5
# def read_parameters_hdf5(model, InputData):

#     PathToFile    = InputData.PathToHDF5Fld + 'Params.hdf5'
#     HDF5Exist_Flg = path.exists(PathToFile)
#     if (HDF5Exist_Flg):
#         f = h5py.File(PathToFile, 'a')
#     else:
#         f = {'key': 'value'}


#     CheckStr        = 'Finalb'
#     Data            = f['Finalb']
#     model.biasFinal = tf.Variable(Data[...], dtype=tf.float64, name='BiasFinal')


#     NBranches = InputData.BranchLayers.shape[0]
#     for iBranch in range(NBranches):
#         #print('[ProPDE]:   Reading Parameters for Branch ' + str(iBranch))
#         NetName  = 'Branch'  + str(iBranch+1)
#         CheckStr = '/' + NetName + '/'
#         grp      = f[CheckStr]

#         #print('[ProPDE]:   Reading Activation Functions Scaling Parameters')
#         ActScalingName                  = NetName + 'ActScaling'
#         Data                            = grp["ActScaling"]
#         model.ActScalingBranch[iBranch] = tf.Variable(Data[...], dtype=tf.float64, name=ActScalingName)

#         NLayers = InputData.TrunkLayers.shape[0]
#         for iLayer in range(NLayers-1):
#             #print('[ProPDE]:   Saving Weights and Biases for Layer ' + str(iLayer+1))
#             CheckStrTemp  = CheckStr + '/HL' + str(iLayer+1) + '/'

#             WeightsName   = NetName + 'Weight' + str(iLayer+1)
#             Data          = grp[CheckStrTemp+'W']
#             model.weightsBranch[iBranch][iLayer] = tf.Variable(Data[...], dtype=tf.float64, name=WeightsName)

#             BiasesName    = NetName + 'Biases' + str(iLayer+1)
#             Data          = grp[CheckStrTemp+'b']
#             model.biasesBranch[iBranch][iLayer]  = tf.Variable(Data[...], dtype=tf.float64, name=BiasesName)
            
     
#     NetName  = 'Trunk'
#     CheckStr = '/' + NetName + '/'
#     grp      = f[CheckStr]
#     #print('[ProPDE]:   Reading Parameters for Trunk')

#     #print('[ProPDE]:   Reading Activation Functions Scaling Parameters')
#     ActScalingName        = NetName + 'ActScaling'
#     Data                  = grp["ActScaling"]
#     model.ActScalingTrunk = tf.Variable(Data[...], dtype=tf.float64, name=ActScalingName)

#     NLayers = InputData.TrunkLayers.shape[0]
#     for iLayer in range(NLayers-1):
#         #print('[ProPDE]:   Reading Weights and Biases for Layer ' + str(iLayer+1))
#         CheckStrTemp               = CheckStr + '/HL' + str(iLayer+1) + '/'

#         WeightsName                = NetName + 'Weight' + str(iLayer+1)
#         Data                       = grp[CheckStrTemp+'W']
#         model.weightsTrunk[iLayer] = tf.Variable(Data[...], dtype=tf.float64, name=WeightsName)

#         BiasesName                 = NetName + 'Biases' + str(iLayer+1)
#         Data                       = grp[CheckStrTemp+'b']
#         model.biasesTrunk[iLayer]  = tf.Variable(Data[...], dtype=tf.float64, name=BiasesName)
   

#     f.close()    


#     return model