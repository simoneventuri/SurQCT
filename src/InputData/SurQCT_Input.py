import os
import numpy                                  as np


#=======================================================================================================================================
class inputdata(object):


    def __init__(self, WORKSPACE_PATH, SurQCTFldr):

        #=======================================================================================================================================
        ### Case Name
        self.RatesType = None
        self.ExcitType = None

        #=======================================================================================================================================
        ### Execution Flags
        self.DefineModelIntFlg   = 0
        self.TrainIntFlg         = 0                                                                      # Training                       0=>No, 1=>Yes
        self.WriteParamsIntFlg   = 0                                                                      # Writing Parameters             0=>Never, 1=>After Training, 2=>Also During Training
        self.WriteDataIntFlg     = 0                                                                      # Writing Data After Training    0=>Never, 1=>After Training, 2=>Also During Training
        self.TestIntFlg          = 0                                                                      # Evaluating                     0=>No, 1=>Yes
        self.PlotIntFlg          = 0                                                                      # Plotting Data                  0=>Never, 1=>After Training, 2=>Also During Training
        self.PredictIntFlg       = 1                                                                      # Plotting Data                  0=>Never, 1=>After Training, 2=>Also During Training

        #=======================================================================================================================================
        ### Paths
        self.WORKSPACE_PATH      = WORKSPACE_PATH                                                         # os.getenv('WORKSPACE_PATH')      
        self.SurQCTFldr          = SurQCTFldr
        self.NNRunIdx            = 3                                                                      # Training Case Identification Number 
        self.PathToRunFld        = None                                                                   # Path To Training Folder
        self.TBCheckpointFldr    = '/TB/'
        self.PathToFigFld        = '/Figures/'                                                            # Path To Training Figures Folder 
        self.PathToDataFld       = '/Data/'                                                               # Path To Training Data Folder 
        self.PathToParamsFld     = '/Params/'                                                             # Path To Training Parameters Folder 
        self.PathToHAHDF5File    = None
        self.PathToHDF5File      = None
        self.PathToLevelsFile    = None
        self.PathToGrouping      = None  

        #=======================================================================================================================================
        ## NN Model Structure
        self.ApproxModel         = None
        self.NNLayers            = None
        self.ActFun              = None
        self.DropOutRate         = None

        #=======================================================================================================================================
        ### Training Quanties
        self.xVarsVec            = None
        self.OtherVar            = None
        self.NSamplesNoise       = None
        self.RandDataFlg         = None                                                                  

        self.TTranVecTrain       = None
        self.iLevelsIntFlg       = None
        self.PathToSampledLevels = None
        #self.iLevelsSeedsVec     = [0, 4, 3, 1, 2]
        #self.iLevelsVecTrain     = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000]
        #self.NiLevelsSampled    = 100

        self.NEpoch              = None                                                                     
        self.MiniBatchSize       = None
        self.LossFunction        = None
        self.LearningRate        = None                                                               
        self.Optimizer           = None                                                                   
        self.OptimizerParams     = None
        self.WeightDecay         = None
        self.ImpThold            = None   
        self.NPatience           = None 
        self.ValidPerc           = None                                 

        #=======================================================================================================================================
        ### Testing Quantities
        self.TestPerc            = None
        self.TTranVecTest        = None
        self.iLevelsVecTest      = None
        self.TTranVecExtra       = None
