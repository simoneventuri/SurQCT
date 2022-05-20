def Initialize_O3_UMN(InputData,Dimension):   

    return InputData

def Initialize_N3_NASA(InputData,Dimension):   
    if(Dimension=='nondim'):
        InputData.Molecules       = ['N2','N2']
        InputData.PathToLevelsFile = [InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_log_nd.csv',
                                      InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_LeRoy_log_nd.csv']
        InputData.PathToDiatFile  = [InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/LeRoy/MyLeroy_FromRobyn.inp',
                                     InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/LeRoy/MyLeroy_FromRobyn.inp']   
        InputData.PathToHDF5File  = InputData.WORKSPACE_PATH  + '/Air_Database/HDF5_Database_semiClassicalApprox/N3_NASA.hdf5'
    
    return InputData

def Initialize_NON_UMN(InputData,Dimension):   
    if(Dimension=='nondim'):
        InputData.Molecules       = ['NO','NO'] 
        InputData.PathToLevelsFile= [InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/NO_UMN_log_nd.csv',
                                     InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/NO_UMN_log_nd.csv']
        InputData.PathToDiatFile  = [InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/NO/UMN/Recomputed.inp',
                                     InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/NO/UMN/Recomputed.inp']
        InputData.PathToHDF5File  = InputData.WORKSPACE_PATH  + '/Air_Database/HDF5_Database/NON_UMN.hdf5'

    return InputData

def Initialize_N2O_UMN(InputData,Dimension):   
    if(Dimension=='nondim'):
        InputData.Molecules       = ['N2','N2'] 
        InputData.PathToLevelsFile= [InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_UMN_ForN2O2_log_nd.csv',
                                     InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/N2_UMN_ForN2O2_log_nd.csv']
        InputData.PathToDiatFile  = [InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/UMN_ForN2O2/Recomputed.inp',
                                     InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/N2/UMN_ForN2O2/Recomputed.inp'] 
        InputData.PathToHDF5File  = InputData.WORKSPACE_PATH  + '/Air_Database/HDF5_Database/N2O_UMN.hdf5'
    return InputData

def Initialize_CO2_NASA(InputData,Dimension):   
    if(Dimension=='nondim'):
        InputData.Molecules       = ['CO','CO'] 
        InputData.PathToLevelsFile= [InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/CO_NASA_log_nd.csv',
                                     InputData.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/CO_NASA_log_nd.csv']
        InputData.PathToDiatFile  = [InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/CO/NASA/CO_levels_venturi.dat',
                                     InputData.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/CO/NASA/CO_levels_venturi.dat']
        InputData.PathToHDF5File  = InputData.WORKSPACE_PATH  + '/Air_Database/HDF5_Database/CO2_NASA.hdf5'

    return InputData