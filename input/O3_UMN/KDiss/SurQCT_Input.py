import os
import numpy                                  as np


#=======================================================================================================================================
class inputdata(object):


    def __init__(self, WORKSPACE_PATH, SurQCTFldr):

        #=======================================================================================================================================
        ### Case Name
        self.RatesType = 'KDiss'

        #=======================================================================================================================================
        ### Execution Flags
        self.DefineModelIntFlg   = 1
        self.TrainIntFlg         = 2                                                                      # Training                       0=>No, 1=>Yes
        self.WriteParamsIntFlg   = 1                                                                      # Writing Parameters             0=>Never, 1=>After Training, 2=>Also During Training
        self.WriteDataIntFlg     = 2                                                                      # Writing Data After Training    0=>Never, 1=>After Training, 2=>Also During Training
        self.TestIntFlg          = 2                                                                      # Evaluating                     0=>No, 1=>Yes
        self.PlotIntFlg          = 2                                                                      # Plotting Data                  0=>Never, 1=>After Training, 2=>Also During Training

        #=======================================================================================================================================
        ### Paths
        self.WORKSPACE_PATH      = WORKSPACE_PATH                                                         # os.getenv('WORKSPACE_PATH')      
        self.SurQCTFldr          = SurQCTFldr                                                             # $WORKSPACE_PATH/ProPDE/
        self.NNRunIdx            = 1                                                                      # Training Case Identification Number 
        self.PathToRunFld        = self.SurQCTFldr + '/../' + self.RatesType + '/Test' + str(self.NNRunIdx) # Path To Training Folder
        self.TBCheckpointFldr    = self.PathToRunFld + '/TB/'
        self.PathToFigFld        = self.PathToRunFld + '/Figures/'                                        # Path To Training Figures Folder 
        self.PathToDataFld       = self.PathToRunFld + '/Data/'                                           # Path To Training Data Folder 
        self.PathToParamsFld     = self.PathToRunFld + '/Params/'                                         # Path To Training Parameters Folder 
        self.PathToHAHDF5File    = self.WORKSPACE_PATH  + '/Air_Database/HDF5_Database_HighAccuracy/O3_UMN.hdf5'
        self.PathToHDF5File      = self.WORKSPACE_PATH  + '/Air_Database/HDF5_Database/O3_UMN.hdf5'
        self.PathToLevelsFile    = [self.WORKSPACE_PATH + '/Air_Database/Run_0D/database/levels/O2.csv']
        self.PathToGrouping      = self.WORKSPACE_PATH  + '/Air_Database/Run_0D/database/grouping/O3_UMN/O2/LevelsMap_DPM45.csv'   

        #=======================================================================================================================================
        ## NN Model Structure
        self.ApproxModel         = 'FNN'
        self.NNLayers            = np.array([32, 16])
        self.ActFun              = ['relu', 'relu']
        self.DropOutRate         = 1.e-2

        #=======================================================================================================================================
        ### Training Quanties
        self.xVarsVec            = ['EVib','ERot','rMin','rMax','VMin','VMax','Tau','ri','ro']
        self.RandDataFlg         = True                                                                      # Randomize Training Data 

        self.TTranVecTrain       = np.array([1500.0, 5000.0, 10000.0, 15000.0, 20000.0])#np.array([1500.0, 5000.0, 8000.0, 12000.0, 15000.0, 20000.0])
        self.iLevelsIntFlg       = 4
        self.PathToSampledLevels = self.WORKSPACE_PATH  + '/Air_Database/Run_0D/database/levels/O2_Sampled_'
        #self.iLevelsSeedsVec     = [0, 4, 3, 1, 2]
        #self.iLevelsVecTrain     = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000]
        #self.NiLevelsSampled    = 100

        self.NEpoch              = 30000                                                                     # Number of Epoches
        self.MiniBatchSize       = 64
        self.LossFunction        = 'mean_absolute_percentage_error'
        self.LearningRate        = 1.e-5                                                                     # Initial Learning Rate
        self.Optimizer           = 'adam'                                                                    # Optimizer Identificator
        self.OptimizerParams     = [0.9, 0.999, 1e-07]                                                       # Parameters for the Optimizer
        self.WeightDecay         = np.array([1.e-5, 1.e-5], dtype=np.float64)                                # Hyperparameters for L1 and L2 Weight Decay Regularizations
        self.ImpThold            = 1.e-4
        self.NPatience           = 500
        self.ValidPerc           = 30.0                                                                      # Percentage of Training Data to Be Used for Validation (e.g., = 20.0 => 20%)

        #=======================================================================================================================================
        ### Testing Quantities
        self.TestPerc            = 0.0                                                                      # Percentage of Overall Data to Be Used for Testing (e.g., = 20.0 => 20%)
        self.TTranVecTest        = np.array([1500.0, 2500.0, 5000.0, 6000.0, 8000.0, 10000.0, 12000.0, 14000.0, 15000.0, 20000.0])
        self.TTranVecExtra       = np.array([300.0, 40000.0])
