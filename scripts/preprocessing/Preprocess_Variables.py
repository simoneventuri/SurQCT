import os
import sys
import numpy                                  as np
import time
import shutil
import seaborn                                as sns
import pandas                                 as pd


### ---------------------------------------------------------------------------------------------------------------------------------- ###

WORKSPACE_PATH   = os.getenv('WORKSPACE_PATH')  

PathToOutputFldr =  WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/'

### O2+O
Molecules        = ['O2_UMN']
PathToDiatPot    = [WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/O2/UMN/FromUMN_Sorted.inp']

# ### N2+N
# Molecules        = ['N2_LeRoy']
# PathToDiatPot    = [WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/LeRoy/MyLeroy_FromRobyn.inp']

# ### N2+O
# Molecules        = ['N2_UMN_ForN2O2', 'NO_UMN']
# PathToDiatPot    = [WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/UMN_ForN2O2/Recomputed.inp', 
#                     WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/NO/UMN/Recomputed.inp']
### ---------------------------------------------------------------------------------------------------------------------------------- ###



### ---------------------------------------------------------------------------------------------------------------------------------- ###

def compute_vibenergy(eint, vqn, jqn):
    NLevels = len(eint)
    EVib    = np.zeros((NLevels,1))
    ERot    = np.zeros((NLevels,1))
    ETemp   = np.zeros((np.amax(vqn)+1,1))
    for iLevel in range(NLevels):
        if (jqn[iLevel] == 0):
            EVib[iLevel]       = eint[iLevel]
            ETemp[vqn[iLevel]] = eint[iLevel]
        else:
            EVib[iLevel] = ETemp[vqn[iLevel]]
            ERot[iLevel] = eint[iLevel] - EVib[iLevel]
    return EVib, ERot



NMolecules = len(Molecules)
for iMol in range(NMolecules):
    
    ### Reading Levels Data
    LevelsData           = pd.read_csv(PathToDiatPot[iMol], delim_whitespace=True, skiprows=15, header=None)
    LevelsData.columns   = ['vqn','jqn','EInt','egam','rMin','rMax','VMin','VMax','Tau','ri','ro']    
    
    
    ### Shifting Energies so that Zero is the Min of Diatomic Potential at J=0
    LevelsData['EInt']   = LevelsData['EInt'].to_numpy() -  np.amin(LevelsData['VMin'].to_numpy())
    LevelsData['VMax']   = LevelsData['VMax'].to_numpy() -  np.amin(LevelsData['VMin'].to_numpy())
    LevelsData['VMin']   = LevelsData['VMin'].to_numpy() -  np.amin(LevelsData['VMin'].to_numpy())
    
    
    ### Splitting Energy in Rotational and Vibrational Contribution
    EVib, ERot           = compute_vibenergy(LevelsData.EInt.to_numpy(), LevelsData.vqn.to_numpy(int), LevelsData.jqn.to_numpy(int))
    LevelsData['EVib']   = EVib
    LevelsData['ERot']   = ERot
    
    LevelsDataNew        = LevelsData.copy()
    LevelsDataNew.head()
    
    
    ### Normalizing Variables
    # ...
    
    
    ### Taking Logarithms
    LevelsDataNew['EVib'] = np.log10(LevelsData.EVib.to_numpy())
    LevelsDataNew['ERot'] = np.log10(LevelsData.ERot.to_numpy() + 1.e-6)
    LevelsDataNew['Tau']  = np.log10(LevelsData.Tau.to_numpy())
    LevelsDataNew['ro']   = np.log10(LevelsData.ro.to_numpy())
    
    
    ### Writing Data File
    LevelsDataNew.to_csv(PathToOutputFldr+Molecules[iMol]+'_nd.csv', index=False)