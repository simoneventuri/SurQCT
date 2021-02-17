import time
import os
import shutil
import sys
import tensorflow                             as tf
import numpy                                  as np
from tensorflow                           import keras
from tensorflow                           import train
from tensorflow.keras                     import layers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras                     import regularizers
from tensorflow.keras                     import optimizers
from tensorflow.keras                     import losses
from tensorflow.keras                     import callbacks
from sklearn.model_selection              import train_test_split


# from Plotting import plot_var
# from Reading  import read_parameters_hdf5
# from Saving   import save_parameters, save_parameters_hdf5, save_data


#=======================================================================================================================================
def NNBranch(InputData, normalized, NNName, Idx):

    kW1      = InputData.WeightDecay[0]
    kW2      = InputData.WeightDecay[1]
    NNLayers = InputData.NNLayers[Idx]
    NLayers  = len(NNLayers)
    ActFun   = InputData.ActFun[Idx]

    hiddenVec = [normalized]

    for iLayer in range(NLayers):
        LayerName = NNName + str(Idx) + '_HL' + str(iLayer+1) 
        hiddenVec.append(layers.Dense(units=NNLayers[iLayer],
                                activation=ActFun[iLayer],
                                use_bias=True,
                                kernel_initializer='glorot_normal',
                                bias_initializer='zeros',
                                kernel_regularizer=regularizers.l1_l2(l1=kW1, l2=kW2),
                                bias_regularizer=regularizers.l1_l2(l1=kW1, l2=kW2),
                                name=LayerName)(hiddenVec[-1]))
        if (iLayer < NLayers-1):
            hiddenVec.append(layers.Dropout(InputData.DropOutRate, input_shape=(NNLayers[iLayer],))(hiddenVec[-1]))


    return hiddenVec[-1]

#=======================================================================================================================================



#=======================================================================================================================================
class model:    

    # Class Initialization
    def __init__(self, InputData, PathToRunFld, TrainData, ValidData):

        #-------------------------------------------------------------------------------------------------------------------------------        
        VarsVec           = InputData.xVarsVec + ['TTran']
        ChooseVarsI       = [(VarName + '_i') for VarName in VarsVec]
        ChooseVarsData    = [(VarName + InputData.OtherVar) for VarName in VarsVec]
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


            #---------------------------------------------------------------------------------------------------------------------------
            xDim               = len(InputData.xVarsVec)+1
            input_             = tf.keras.Input(shape=[xDim*2,])
            inputI, inputDelta = tf.split(input_, num_or_size_splits=[xDim, xDim], axis=1)

            ### Normalizer Layers
            normalizerI        = preprocessing.Normalization()
            self.xTrainI       = self.xTrain[ChooseVarsI]
            normalizerI.adapt(np.array(self.xTrainI))
            normalizedI        = normalizerI(inputI)
            #
            self.xTrainData    = self.xTrain[ChooseVarsData]
            normalizerDelta    = preprocessing.Normalization()
            normalizerDelta.adapt(np.array(self.xTrainData))
            normalizedDelta    = normalizerDelta(inputDelta)

            ### NN Branches
            outputI         = NNBranch(InputData, normalizedI,     'Branch', 0)
            #
            outputDelta     = NNBranch(InputData, normalizedDelta, 'Branch', 1)

            ### Final Dot Product
            output_1        = layers.Dot(axes=1)([outputI, outputDelta])
           
            ### Adding Noise
            # output_2        = tf.math.exp(output_1)
            # StDev           = 5e-14
            # output_3        = tf.nn.relu(layers.GaussianNoise(stddev=StDev)(output_2))
            # output_4        = tf.math.log(output_3)

            output_Final    = layers.Dense(units=1,
                                           activation='linear',
                                           use_bias=True,
                                           kernel_initializer='glorot_normal',
                                           bias_initializer='zeros',
                                           name='FinalScaling')(output_1)   

            self.Model      = keras.Model(inputs=[input_], outputs=[output_Final] )
            #---------------------------------------------------------------------------------------------------------------------------


            #---------------------------------------------------------------------------------------------------------------------------
            LearningRate = optimizers.schedules.ExponentialDecay(InputData.LearningRate, decay_steps=50000, decay_rate=0.98, staircase=True)

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

        else:
            
            #---------------------------------------------------------------------------------------------------------------------------
            ModelFile      = PathToRunFld + '/MyModel'
            print('[SurQCT]:   Loading ML Model from Folder: ' + ModelFile)
            self.Model     = keras.models.load_model(ModelFile)
            #---------------------------------------------------------------------------------------------------------------------------

    #===================================================================================================================================



    #===================================================================================================================================
    def train(self, InputData):

        ESCallBack    = callbacks.EarlyStopping(monitor='val_loss', min_delta=InputData.ImpThold, patience=InputData.NPatience, restore_best_weights=True, mode='auto', baseline=None, verbose=1)
        MCFile        = InputData.PathToParamsFld + "/ModelCheckpoint/cp-{epoch:04d}.ckpt"
        MCCallBack    = callbacks.ModelCheckpoint(filepath=MCFile, monitor='val_loss', save_best_only=True, save_weights_only=True, verbose=0, mode='auto', save_freq='epoch', options=None)
        #LRCallBack    = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.7, patience=500, mode='auto', min_delta=1.e-6, cooldown=0, min_lr=1.e-8, verbose=1)
        TBCallBack    = callbacks.TensorBoard(log_dir=InputData.TBCheckpointFldr, histogram_freq=100, batch_size=InputData.MiniBatchSize, write_graph=True, write_grads=True, write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None)
        #CallBacksList = [MCCallBack, ESCallBack, TBCallBack]
        CallBacksList = [ESCallBack, TBCallBack, MCCallBack]

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
