import os
import numpy                                  as np


#=======================================================================================================================================
class inputdata(object):


    def __init__(self, WORKSPACE_PATH, SurQCTFldr):

        #=======================================================================================================================================
        ### Case Name
        self.RatesType     = 'KExcit'
        self.ExcitType     = 'KInel'
        self.SameMolecules = True
        
        #=======================================================================================================================================
        ### Execution Flags
        self.DefineModelIntFlg   = 1
        self.TrainIntFlg         = 2                                                                                              # Training                       0=>No, 1=>Yes
        self.WriteParamsIntFlg   = 1                                                                                              # Writing Parameters             0=>Never, 1=>After Training, 2=>Also During Training
        self.WriteDataIntFlg     = 2                                                                                              # Writing Data After Training    0=>Never, 1=>After Training, 2=>Also During Training
        self.TestIntFlg          = 2                                                                                              # Evaluating                     0=>No, 1=>Yes
        self.PlotIntFlg          = 2                                                                                              # Plotting Data                  0=>Never, 1=>After Training, 2=>Also During Training
        self.PredictIntFlg       = 2                                                                                              # Plotting Data                  0=>Never, 1=>After Training, 2=>Also During Training

        #=======================================================================================================================================
        ### Paths
        self.WORKSPACE_PATH      = WORKSPACE_PATH                                                                                 # os.getenv('WORKSPACE_PATH')      
        self.SurQCTFldr          = SurQCTFldr                                                                                     # $WORKSPACE_PATH/ProPDE/
        self.NNRunIdx            = 0                                                                                              # Training Case Identification Number 
        self.PathToRunFld        = self.SurQCTFldr + '/../' + self.RatesType + '/all_temperatures_nondim/' + self.ExcitType + '/' # Path To Training Fldr
        self.TBCheckpointFldr    = self.SurQCTFldr + '/../' + self.RatesType + '/all_temperatures_nondim/TB/'
        self.PathToFigFld        = '/Figures/'                                                                                    # Path To Training Figures Folder 
        self.PathToDataFld       = '/Data/'                                                                                       # Path To Training Data Folder 
        self.PathToParamsFld     = '/Params/'                                                                                     # Path To Training Parameters Folder 
        self.PathToHAHDF5File    = self.WORKSPACE_PATH  + '/Air_Database/HDF5_Database_HighAccuracy_AmalInel/O3_UMN.hdf5'
        self.PathToHDF5File      = self.WORKSPACE_PATH  + '/Air_Database/HDF5_Database/O3_UMN.hdf5'

        self.Molecules           = ['O2','O2'] 
        self.PathToLevelsFile    = [self.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/O2_UMN_nd.csv',
                                    self.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/O2_UMN_nd.csv']
        self.PathToDiatFile      = [self.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/O2/UMN/FromUMN_Sorted.inp',
                                    self.WORKSPACE_PATH + '/CoarseAIR/coarseair/dtb/Molecules/O2/UMN/FromUMN_Sorted.inp']   
                                                            
        self.PathToGrouping      = self.WORKSPACE_PATH  + '/Air_Database/Run_0D/database/grouping/O3_UMN/O2/LevelsMap_DPM45.csv'   

        #=======================================================================================================================================
        ## NN Model Structure
        # self.ApproxModel         = 'FNN'
        # self.NNLayers            = np.array([32, 32, 32 ])
        # self.ActFun              = ['sigmoid', 'sigmoid', 'sigmoid']
        self.ApproxModel         = 'DotNet'
        self.NormalizeInput      = True
        self.NNLayers            = [np.array([64, 64, 64]), np.array([64, 64, 64])]
        self.ActFun              = [['tanh', 'tanh', 'tanh'], ['tanh', 'tanh', 'linear']]
        self.DropOutRate         = 1.e-3
        # self.ApproxModel         = 'SumNet'
        # self.NNLayers            = [np.array([32, 32, 32]), np.array([32, 32, 32]), np.array([32, 1])]
        # self.ActFun              = [['sigmoid', 'sigmoid', 'sigmoid'], ['sigmoid', 'sigmoid', 'sigmoid'], ['sigmoid', 'linear']]


        #=======================================================================================================================================
        ### Training Quanties
        self.xVarsVec_i          = ['EVib','ERot','rMin','rMax','VMin','VMax','Tau','ri','ro'] #['EVib','ERot','VMin','VMax','Tau','ri','ro','vqn','jqn']
        self.xVarsVec_Delta      = ['EVib','ERotR','rMin','rMax','VMin','VMax','Tau','ri','ro'] #['EVib','ERot','VMin','VMax','Tau','ri','ro','vqn','jqn']
        self.OtherVar            = '_Delta'
        self.NSamplesNoise       = 0
        self.RandDataFlg         = True                                                                      # Randomize Training Data 
        self.TTranVecTrain       = np.array([1500.0, 5000.0, 10000.0, 15000.0, 20000.0]) #np.array([1500.0, 5000.0, 8000.0, 12000.0, 15000.0, 20000.0, 30000.0, 50000.0])])
        self.iLevelsIntFlg       = 4
        self.PathToSampledLevels = self.WORKSPACE_PATH  + '/Air_Database/Run_0D/database/levels/AmalInel_Sampled_with_extremes/O2_Sampled_Inel_'
        self.ExoEndoFlg          = False
        #self.iLevelsSeedsVec     = [0, 4, 3, 1, 2]
        #self.iLevelsVecTrain     = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000]
        #self.NiLevelsSampled    = 100

        self.NEpoch              = 50000                                                                      # Number of Epoches
        self.MiniBatchSize       = 64
        self.LossFunction        = 'mean_absolute_percentage_error'#'mean_squared_logarithmic_error'
        self.LearningRate        = 1.e-4                                                                     # Initial Learning Rate
        self.Optimizer           = 'adam'                                                                    # Optimizer Identificator
        self.OptimizerParams     = [0.9, 0.999, 1e-07]                                                       # Parameters for the Optimizer
        self.WeightDecay         = np.array([5.e-5, 1.e-10], dtype=np.float64)                               # Hyperparameters for L1 and L2 Weight Decay Regularizations
        self.ImpThold            = 1.e-4   
        self.NPatience           = 1000 
        self.ValidPerc           = 20.0                                                                      # Percentage of Training Data to Be Used for Validation (e.g., = 20.0 => 20%)

        #=======================================================================================================================================
        ### Testing Quantities
        self.TestPerc            = 0.0                                                                       # Percentage of Overall Data to Be Used for Testing (e.g., = 20.0 => 20%)
        self.TTranVecTest        = np.array([6000.0, 10000.0]) #np.array([1500.0, 2500.0, 5000.0, 6000.0, 8000.0, 10000.0, 12000.0, 14000.0, 15000.0, 20000.0])
        self.iLevelsVecTest      = [4580, 4581, 6058, 6097, 6105, 6108, 6111]#[500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
        self.TTranVecExtra       = np.array([300.0, 50000.0])
