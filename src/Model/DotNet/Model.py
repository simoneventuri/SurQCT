import time
import os
import shutil
import sys
import tensorflow                             as tf
import numpy                                  as np
from tensorflow                           import keras
from tensorflow                           import train
from tensorflow.keras                     import layers
from tensorflow.keras                     import initializers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras                     import regularizers
from tensorflow.keras                     import optimizers
from tensorflow.keras                     import losses
from tensorflow.keras                     import callbacks
from tensorflow.python.ops                import array_ops
from sklearn.model_selection              import train_test_split


# from Plotting import plot_var
# from Reading  import read_parameters_hdf5
# from Saving   import save_parameters, save_parameters_hdf5, save_data

WORKSPACE_PATH = os.environ['WORKSPACE_PATH']
SurQCTFldr     = WORKSPACE_PATH + '/SurQCT/surqct/'

sys.path.append(SurQCTFldr + 'src/Callbacks/')
from customCallbacks import customReduceLROnPlateau



#=======================================================================================================================================
from datetime import datetime

def get_curr_time():
    return datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

def get_start_time():
    return get_curr_time()

#=======================================================================================================================================



#=======================================================================================================================================
@tf.keras.utils.register_keras_serializable(package='Custom', name='l1')
class L1Regularizer(tf.keras.regularizers.Regularizer):
  def __init__(self, l1, x0):
    self.l1 = l1
    self.x0 = x0

  def __call__(self, x):
    return self.l1 * tf.math.reduce_sum(tf.math.abs(x - self.x0))

  def get_config(self):
    return {'l1': float(self.l1)}


@tf.keras.utils.register_keras_serializable(package='Custom', name='l2')
class L2Regularizer(tf.keras.regularizers.Regularizer):
  def __init__(self, l2, x0):
    self.l2 = l2
    self.x0 = x0

  def __call__(self, x):
    return self.l2 * tf.math.reduce_sum(tf.math.square(x - self.x0))

  def get_config(self):
    return {'l2': float(self.l2)}


@tf.keras.utils.register_keras_serializable(package='Custom', name='l1l2')
class L1L2Regularizer(tf.keras.regularizers.Regularizer):
  def __init__(self, l1, l2, x0):
    self.l1 = l1
    self.l2 = l2
    self.x0 = x0

  def __call__(self, x):
    Diff = x - self.x0
    return self.l1 * tf.math.reduce_sum(tf.math.abs(Diff)) + self.l2 * tf.math.reduce_sum(tf.math.square(Diff))

  def get_config(self):
    return {'l1l2': float(self.l2)}
#=======================================================================================================================================



#=======================================================================================================================================
def NNBranch(InputData, normalized, NNName, Idx, NN_Transfer_Model):

    kW1      = InputData.WeightDecay[0]
    kW2      = InputData.WeightDecay[1]
    NNLayers = InputData.NNLayers[Idx]
    NLayers  = len(NNLayers)
    ActFun   = InputData.ActFun[Idx]
    Mol      = '_i'

    hiddenVec = [normalized]
    for iLayer in range(NLayers):
        WeightsName = NNName + '_HL' + str(iLayer+1) 
        LayerName   = WeightsName + Mol 

        if (InputData.TransferFlg):
            x0     = NN_Transfer_Model.get_layer(LayerName).kernel.numpy()
            b0     = NN_Transfer_Model.get_layer(LayerName).bias.numpy()
            WIni   = tf.keras.initializers.RandomNormal(mean=x0, stddev=1.e-10)
            bIni   = tf.keras.initializers.RandomNormal(mean=b0, stddev=1.e-10)
            WRegul = L1L2Regularizer(kW1, kW2, x0)
            bRegul = L1L2Regularizer(kW1, kW2, b0)
        else:
            WIni   = 'glorot_normal'
            bIni   = 'zeros'
            WRegul = regularizers.l1_l2(l1=kW1, l2=kW2)
            bRegul = regularizers.l1_l2(l1=kW1, l2=kW2)


        hiddenVec.append(layers.Dense(units            = NNLayers[iLayer],
                                    activation         = ActFun[iLayer],
                                    use_bias           = True,
                                    kernel_initializer = WIni,
                                    bias_initializer   = bIni,
                                    kernel_regularizer = WRegul,
                                    bias_regularizer   = bRegul,
                                    name               = LayerName)(hiddenVec[-1]))
        
        if (iLayer < NLayers-1):
            hiddenVec.append(layers.Dropout(InputData.DropOutRate, input_shape=(NNLayers[iLayer],))(hiddenVec[-1]))          

    return hiddenVec[-1]

#=======================================================================================================================================




#=======================================================================================================================================
class BiasLayer(layers.Layer):
    def __init__(self, b0):
        super(BiasLayer, self).__init__(name='FinalScaling')
        self.b0   = b0

    def build(self, input_shape):
        bIni      = tf.keras.initializers.constant(value=self.b0)
        self.bias = self.add_weight('bias',
                                    shape       = input_shape[1:],
                                    initializer = bIni,
                                    trainable   = True)
    def call(self, x):
        return x + self.bias

#=======================================================================================================================================



#=======================================================================================================================================
class model:    


    # Class Initialization
    def __init__(self, InputData, PathToRunFld, TrainData, ValidData):


        #===================================================================================================================================
        class AdditiveGaussNoise(layers.Layer):
          def __init__(self, mean, stddev):
            super(AdditiveGaussNoise, self).__init__()
            self.mean   = mean
            self.stddev = stddev

          def build(self, input_shape):
            self.input_shape_  = input_shape 
            
          def call(self, input):
            return input + tf.random.normal(shape=array_ops.shape(input), mean=self.mean, stddev=self.stddev)

        #===================================================================================================================================



        #-------------------------------------------------------------------------------------------------------------------------------        
        VarsVec_i         = InputData.xVarsVec_i + ['TTran']
        ChooseVarsI       = [(VarName + '_i') for VarName in VarsVec_i]
        VarsVec_Delta     = InputData.xVarsVec_Delta + ['TTran']
        ChooseVarsData    = [(VarName + InputData.OtherVar) for VarName in VarsVec_Delta]
        self.xTrainingVar = ChooseVarsI + ChooseVarsData
        self.yTrainingVar = InputData.RatesType
        print('[SurQCT]:   Variables Selected for Training:')
        print('[SurQCT]:     x = ', self.xTrainingVar)
        print('[SurQCT]:     y = ', self.yTrainingVar)
        #-------------------------------------------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------------------------------------------  
        if (InputData.TrainIntFlg >= 1):
            self.xTrain       = TrainData[0]
            self.yTrain       = TrainData[1]
            self.xValid       = ValidData[0]
            self.yValid       = ValidData[1]
        #-------------------------------------------------------------------------------------------------------------------------------  

        if (InputData.DefineModelIntFlg > 0):
            print('[SurQCT]:   Defining ML Model from Scratch')

            if (InputData.TransferFlg): 
                ModelFile         = InputData.TransferModelFld + '/MyModel/'
                NN_Transfer_Model = keras.models.load_model(ModelFile)
                MCFile            = InputData.TransferModelFld + '/Params/ModelCheckpoint/cp-{epoch:04d}.ckpt'
                checkpoint_dir    = os.path.dirname(MCFile)
                latest            = train.latest_checkpoint(checkpoint_dir)
                NN_Transfer_Model.load_weights(latest)
            else:
                NN_Transfer_Model = None

            #---------------------------------------------------------------------------------------------------------------------------
            xDim_i              = len(VarsVec_i)
            xDim_Delta          = len(VarsVec_Delta)
            input_              = tf.keras.Input(shape=[xDim_i+xDim_Delta,])
            inputI, inputDeltaI = tf.split(input_, num_or_size_splits=[xDim_i, xDim_Delta], axis=1)

            ### Normalizer Layers
            if (InputData.NormalizeInput):
                if (InputData.TransferFlg): 
                    Mean             = NN_Transfer_Model.get_layer('normalization').mean.numpy()
                    Variance         = NN_Transfer_Model.get_layer('normalization').variance.numpy()
                    normalizerI      = preprocessing.Normalization(mean=Mean, variance=Variance)
                else:
                    normalizerI      = preprocessing.Normalization()
                    self.xTrainI         = self.xTrain[ChooseVarsI]
                    normalizerI.adapt(np.array(self.xTrainI))
                InputI               = normalizerI(inputI)
                #
                if (InputData.TransferFlg): 
                    Mean             = NN_Transfer_Model.get_layer('normalization_1').mean.numpy()
                    Variance         = NN_Transfer_Model.get_layer('normalization_1').variance.numpy()
                    normalizerDeltaI = preprocessing.Normalization(mean=Mean, variance=Variance)
                else:
                    normalizerDeltaI = preprocessing.Normalization()
                    self.xTrainDataI     = self.xTrain[ChooseVarsData]
                    normalizerDeltaI.adapt(np.array(self.xTrainDataI))
                InputDeltaI          = normalizerDeltaI(inputDeltaI)
            else:
                InputI               = inputI
                InputDeltaI          = inputDeltaI

            ### NN Branches
            outputI        = NNBranch(InputData, InputI,      'Branch', 0, NN_Transfer_Model)
            #
            outputDelta    = NNBranch(InputData, InputDeltaI, 'Trunk',  1, NN_Transfer_Model)

            ### Final Dot Product
            output_P       = layers.Dot(axes=1)([outputI, outputDelta])
           
            ### Final Layer
            LayerName      = 'FinalScaling'
            if (InputData.FinalLayerFlg):
                if (InputData.TransferFlg):
                    x0     = NN_Transfer_Model.get_layer(LayerName).kernel.numpy()
                    b0     = NN_Transfer_Model.get_layer(LayerName).bias.numpy()
                    WIni   = tf.keras.initializers.RandomNormal(mean=x0, stddev=1.e-10)
                    bIni   = tf.keras.initializers.RandomNormal(mean=b0, stddev=1.e-10)
                else:
                    WIni   = 'glorot_normal'
                    bIni   = 'zeros'
                output_Final   = layers.Dense(units              = 1,
                                              activation         = 'linear',
                                              use_bias           = True,
                                              kernel_initializer = WIni,
                                              bias_initializer   = bIni,
                                              name               = 'FinalScaling')(output_P) 
            else:
                b0 = 0
                if (InputData.TransferFlg): 
                    b0 = NN_Transfer_Model.get_layer(LayerName).bias.numpy()[0]
                output_Final    = BiasLayer(b0=b0)(output_P)

            # ### Adding Noise
            # Meann           = -34.5
            # StdDevv         = 0.5
            # output_Final    = AdditiveGaussNoise(Meann, StdDevv)(output_2)

            self.Model      = keras.Model(inputs=[input_], outputs=[output_Final] )
            #---------------------------------------------------------------------------------------------------------------------------


            #---------------------------------------------------------------------------------------------------------------------------
            LearningRate = optimizers.schedules.ExponentialDecay(InputData.LearningRate, decay_steps=200000, decay_rate=0.98, staircase=True)
            #LearningRate = InputData.LearningRate

            MTD = InputData.Optimizer
            if (MTD == 'adadelta'):  # A SGD method based on adaptive learning rate
                opt = optimizers.Adadelta(learning_rate=LearningRate, rho=0.95, epsilon=InputData.epsilon, name='Adadelta')
            elif (MTD == 'adagrad'):
                opt = optimizers.Adagrad(learning_rate=LearningRate, initial_accumulator_value=0.1, epsilon=InputData.epsilon, name="Adagrad")
            elif (MTD == 'adam'):    # A SGD method based on adaptive estimation of first-order and second-order moments
                opt = optimizers.Adam(learning_rate=LearningRate, beta_1=InputData.OptimizerParams[0], beta_2=InputData.OptimizerParams[1], epsilon=InputData.OptimizerParams[2], amsgrad=False, name='Adam')
            elif (MTD == 'adamax'):  # Variant of Adam algorithm based on the infinity norm.
                opt = optimizers.Adam(learning_rate=LearningRate, beta_1=InputData.OptimizerParams[0], beta_2=InputData.OptimizerParams[1], epsilon=InputData.OptimizerParams[2], name='Adamax')
            elif (MTD == 'ftrl'):
                opt = optimizers.Ftrl(learning_rate=LearningRate, learning_rate_power=-0.5, initial_accumulator_value=0.1, l1_regularization_strength=kW1, l2_regularization_strength=kW2, name='Ftrl', l2_shrinkage_regularization_strength=0.0, beta=0.0)
            elif (MTD == 'nadam'):   # Variant of Adam algorithm with Nesterov momentum
                opt = optimizers.Nadam(learning_rate=LearningRate, beta_1=InputData.OptimizerParams[0], beta_2=InputData.OptimizerParams[1], epsilon=InputData.OptimizerParams[2], name='Nadam')
            elif (MTD == 'rmsprop'):
                opt = optimizers.RMSprop(learning_rate=LearningRate, rho=0.9, momentum=InputData.OptimizerParams[0], epsilon=InputData.OptimizerParams[1], centered=False, name='RMSprop')
            elif (MTD == 'sgd'):
                opt = optimizers.SGD(learning_rate=LearningRate, momentum=InputData.OptimizerParams[0], nesterov=NestFlg, name="SGD")
            #---------------------------------------------------------------------------------------------------------------------------


            #---------------------------------------------------------------------------------------------------------------------------
            LF = InputData.LossFunction
            if (LF == 'binary_crossentropy'):
                lss = losses.BinaryCrossentropy(from_logits=False, label_smoothing=0, reduction="auto", name="binary_crossentropy")
            elif (LF == 'categorical_crossentropy'):
                lss = losses.CategoricalCrossentropy(from_logits=False, label_smoothing=0, reduction="auto", name="categorical_crossentropy",)
            elif (LF == 'sparse_categorical_crossentropy'):
                lss = losses.SparseCategoricalCrossentropy(from_logits=False, reduction="auto", name="sparse_categorical_crossentropy")
            elif (LF == 'poisson'):
                lss = losses.Poisson(reduction="auto", name="poisson")
            elif (LF == 'binary_crossenkl_divergencetropy'):
                lss = losses.KLDivergence(reduction="auto", name="kl_divergence")
            elif (LF == 'mean_squared_error'):
                lss = losses.MeanSquaredError(reduction="auto", name="mean_squared_error")
            elif (LF == 'mean_absolute_error'):
                lss = losses.MeanAbsoluteError(reduction="auto", name="mean_absolute_error")
            elif (LF == 'mean_absolute_percentage_error'):
                lss = losses.MeanAbsolutePercentageError(reduction="auto", name="mean_absolute_percentage_error")
            elif (LF == 'mean_squared_logarithmic_error'):
                lss = losses.MeanSquaredLogarithmicError(reduction="auto", name="mean_squared_logarithmic_error")
            elif (LF == 'cosine_similarity'):
                lss = losses.CosineSimilarity(axis=-1, reduction="auto", name="cosine_similarity")
            elif (LF == 'huber_loss'):
                lss = losses.Huber(delta=1.0, reduction="auto", name="huber_loss")
            elif (LF == 'log_cosh'):
                lss = losses.LogCosh(reduction="auto", name="log_cosh")
            elif (LF == 'hinge'):
                lss = losses.Hinge(reduction="auto", name="hinge")
            elif (LF == 'squared_hinge'):
                lss = losses.SquaredHinge(reduction="auto", name="squared_hinge")
            elif (LF == 'categorical_hinge'):
                lss = losses.CategoricalHinge(reduction="auto", name="categorical_hinge")
            elif (LF == 'rmse'):
                lss = rmse
            elif (LF == 'rmseexp'):
                lss = rmseexp
            elif (LF == 'rmsenorm'):
                lss = rmsenorm
            #---------------------------------------------------------------------------------------------------------------------------

            #---------------------------------------------------------------------------------------------------------------------------
            print('[SurQCT]:   Compiling ML Model with Loss and Optimizer')
            self.Model.compile(loss=lss, optimizer=opt)

            ModelFile = PathToRunFld + '/MyModel'
            print('[SurQCT]:   Saving ML Model in File: ' + ModelFile)
            self.Model.save(ModelFile)
            #---------------------------------------------------------------------------------------------------------------------------

            #-------------------------------------------------------------------------------------------------------------------------------
            print('[SurQCT]:   Summarizing ML Model Structure:')
            self.Model.summary()
            #-------------------------------------------------------------------------------------------------------------------------------

            if (InputData.TransferFlg):
                print('\n normalization,   Mean    : ', self.Model.get_layer('normalization').mean.numpy() )
                print('\n normalization,   Variance: ', self.Model.get_layer('normalization').variance.numpy() )
                print('\n normalization_1, Mean    : ', self.Model.get_layer('normalization_1').mean.numpy() )
                print('\n normalization_1, Variance: ', self.Model.get_layer('normalization_1').variance.numpy() )
                
                print('\n FinalScaling,    Bias:     ', self.Model.get_layer('FinalScaling').bias.numpy() )
        else:
            
            #---------------------------------------------------------------------------------------------------------------------------
            ModelFile      = PathToRunFld + '/MyModel'
            print('[SurQCT]:   Loading ML Model from Folder: ' + ModelFile)
            self.Model     = keras.models.load_model(ModelFile)
            #---------------------------------------------------------------------------------------------------------------------------

            #---------------------------------------------------------------------------------------------------------------------------
            ModelFile      = PathToRunFld + '/MyModel/MyWeights.h5'
            print('[SurQCT]:   Restoring ML Model Weigths to File: ' + ModelFile)
            self.Model.save_weights(ModelFile)
            #---------------------------------------------------------------------------------------------------------------------------

    #===================================================================================================================================



    #===================================================================================================================================
    def train(self, InputData):

        _start_time      = get_start_time()
        TBCheckpointFldr = InputData.TBCheckpointFldr + "/" + InputData.ExcitType +"/Run" + str(InputData.NNRunIdx) + "_{}".format(get_start_time())

        ESCallBack    = callbacks.EarlyStopping(monitor='val_loss', min_delta=InputData.ImpThold, patience=InputData.NPatience, restore_best_weights=True, mode='auto', baseline=None, verbose=1)
        MCFile        = InputData.PathToParamsFld + "/ModelCheckpoint/cp-{epoch:04d}.ckpt"
        MCCallBack    = callbacks.ModelCheckpoint(filepath=MCFile, monitor='val_loss', save_best_only=True, save_weights_only=True, verbose=0, mode='auto', save_freq='epoch', options=None)
        LRCallBack    = customReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=200, mode='auto', min_delta=1.e-4, cooldown=0, min_lr=1.e-8, verbose=1)
        TBCallBack    = callbacks.TensorBoard(log_dir=TBCheckpointFldr, histogram_freq=0, write_graph=True, write_grads=True, write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None)
        
        CallBacksList = [ESCallBack, MCCallBack, LRCallBack, TBCallBack]
        #CallBacksList = [TBCallBack, MCCallBack, LRCallBack]

        #History       = self.Model.fit(self.xTrain[self.xTrainingVar], self.yTrain[self.yTrainingVar], batch_size=InputData.MiniBatchSize, validation_split=InputData.ValidPerc/100.0, verbose=1, epochs=InputData.NEpoch, callbacks=CallBacksList)
        # xTrain, xValid, yTrain, yValid = train_test_split(self.xTrain[self.xTrainingVar], self.yTrain[self.yTrainingVar], test_size=InputData.ValidPerc/100.0) #stratify=self.yTrain[self.yTrainingVar],
        print('[SurQCT]:   Here Some of the Training   Labels ... ', self.yTrain[self.yTrainingVar])
        print('[SurQCT]:   Here Some of the Validation Labels ... ', self.yValid[self.yTrainingVar])

        History       = self.Model.fit(self.xTrain[self.xTrainingVar], self.yTrain[self.yTrainingVar], 
                                       batch_size=InputData.MiniBatchSize, 
                                       validation_data=(self.xValid[self.xTrainingVar], self.yValid[self.yTrainingVar]), 
                                       verbose=1, 
                                       epochs=InputData.NEpoch, 
                                       callbacks=CallBacksList)

        ModelFile = InputData.PathToRunFld + '/MyModel/MyWeights.h5'
        self.Model.save_weights(ModelFile)

        return History

    #===================================================================================================================================



    #===================================================================================================================================
    def load_params(self, PathToParamsFld):

        MCFile         = PathToParamsFld + "/ModelCheckpoint/cp-{epoch:04d}.ckpt"
        checkpoint_dir = os.path.dirname(MCFile)
        latest         = train.latest_checkpoint(checkpoint_dir)

        print('[SurQCT]:   Loading ML Model Parameters from File: ', latest)

        self.Model.load_weights(latest)

    #===================================================================================================================================

