import os
import numpy as np

class inputdata(object):


    def __init__(self, WORKSPACE_PATH, ProPDEFldr):

        ################################################################################################################################################################
        ### Case Name
        self.PDEName     = 'MSD2'

        ################################################################################################################################################################
        ### Execution Flags
        self.LoadIntFlg          = 0                                                                      # Loading Parameters             0=>No, 1=>Yes
        self.TrainIntFlg         = 1                                                                      # Training                       0=>No, 1=>Yes
        self.TestIntFlg          = 2                                                                      # Evaluating                     0=>No, 1=>Yes
        self.PlotIntFlg          = 2                                                                      # Plotting Data                  0=>Never, 1=>After Training, 2=>Also During Training
        self.WriteDataIntFlg     = 2                                                                      # Writing Data After Training    0=>Never, 1=>After Training, 2=>Also During Training
        self.WriteParamsIntFlg   = 2                                                                      # Writing Parameters             0=>Never, 1=>After Train., 2=>HDF5 During Train., 3=>CSV during Train.
        self.NEpochTest          = 200

        ################################################################################################################################################################
        ### Paths
        self.WORKSPACE_PATH      = WORKSPACE_PATH                                                         # os.getenv('WORKSPACE_PATH')      
        self.ProPDEFldr          = ProPDEFldr                                                             # $WORKSPACE_PATH/ProPDE/
        self.NNRunIdx            = 1                                                                      # Training Case Identification Number 
        self.PathToRunFld        = self.ProPDEFldr + '/../' + self.PDEName + '/Test' + str(self.NNRunIdx) # Path To Training Folder
        self.PathToFigFld        = self.PathToRunFld + '/Figures/'                                        # Path To Training Figures Folder 
        self.PathToDataFld       = self.PathToRunFld + '/Data/'                                           # Path To Training Data Folder 
        self.PathToParamsFld     = self.PathToRunFld + '/Params/'                                         # Path To Training Parameters Folder 
        self.PathToHDF5Fld       = self.PathToRunFld + '/Params/'                                         # Path to HDF5 File For Loading Parameters

        ################################################################################################################################################################
        ### PDE Properties
        self.uDim        = 2                                                                                 # Dimensionality of Initial Condition Vectors
        self.uRanges     = np.array([[-4.0, 4.0],[-2.0, 2.0]], dtype=np.float64)                             # Minimum and Maximum Values for Initial Conditions of Each of u's Dimensions
        self.xDim        = 2                                                                                 # Dimensionality of State Vectors
        self.xNames      = ['Position', 'Velocity']                                                          # Names for the State Variables
        self.PDEParams   = np.array([1.0, 0.5, 3.0], dtype=np.float64)                                       # Parameters for the ODE Solution and for Computing Residuals

        ###############################################################################################################################################################
        ## NN Model Structure
        self.ApproxModel     = 'DeepONet'
        self.BranchLayers    = np.array([[2, 50, 40], [2, 50, 40]])
        self.TrunkLayers     = np.array([1, 50, 40])
        self.ScaleActFunsFlg = False
        self.BiasBranchFlg   = True

        ################################################################################################################################################################
        ### Training Quanties
        self.NTrainCases = 10                                                                                # Number of Training Cases
        self.t0          = 0.0                                                                               # Time at which Imposing Initial Conditions
        self.tEnd        = 15.0                                                                              # Maximum Time for Selecting Training Collocation Points
        self.NColl       = 100                                                                               # Number of Training Collocation Points
        self.RandDataFlg = True                                                                              # Randomize Training Data 

        self.NEpoch              = 400                                                                       # Number of Epoches
        self.LearningRate        = 5.e-4                                                                     # Initial Learning Rate
        self.Optimizer           = 'adam'                                                                    # Optimizer Identificator
        self.OptimizerParams     = [0.95, 1.e-7]                                                             # Parameters for the Optimizer
        self.WeightDecay         = np.array([1.e-5, 1.e-5], dtype=np.float64)                                # Hyperparameters for L1 and L2 Weight Decay Regularizations

        ################################################################################################################################################################
        ### Testing Quantities
        self.NTestCases  = 2                                                                                 # Number of Test Cases
        self.t0Test      = 0.0                                                                               # Initial Time for Plotting Test Solutions
        self.dtTest      = 0.01                                                                              # Time Step for Plotting Test Solutions
        self.tEndTest    = 10.0                                                                              # Final Time for Plotting Test Solutions

        ################################################################################################################################################################
        ### Plotting Quantities
        self.xLogPlotFlg = False
        self.yLogPlotFlg = False


