import os
import sys
import tensorflow as tf
import numpy      as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import animation
import math


def plot_points(time, pos_data):
    fig = plt.figure()
    plt.xlabel('Time [s]')
    plt.ylabel('Position')
    plt.ylim([math.floor(min(pos_data)-2), math.ceil(max(pos_data)+2)])
    plt.xlim([min(time), max(time)])
    plt.scatter(time[1:], pos_data[1:], marker='o', label='Collocation points')
    plt.scatter(time[0],  pos_data[0],  marker='x', label='I.C. point')
    plt.legend()
    plt.grid()
    plt.title('Data Points for Mass-Spring-Damper system')
    FigPath = InputData.PathToFigFld + '/points.png'
    fig.savefig(FigPath, dpi=600)
    #plt.show()
    plt.close()


def plot_var(InputData, t, xTest, xPred, VarName, iTestCase):
    fig = plt.figure()

    plt.xlabel('Time [s]')
    #plt.ylabel(VarName)

    if (InputData.xLogPlotFlg):
        plt.xscale('log')
        plt.xlim([1.e-15, max(t)])
    else:
        plt.xlim([min(t), max(t)])

    if (InputData.yLogPlotFlg):
        plt.yscale('log')

    LineVec = ['k-', 'k--', 'r-', 'r--', 'g-', 'g--', 'b-', 'b--', 'p-', 'p--']

    for ixDim in range(InputData.xDim):
        #plt.ylim([math.floor(min(xTest)-2), math.ceil(max(xTest)+2)])

        TempName = 'ODE, ' + VarName[ixDim]
        plt.plot(t, xTest[:, ixDim], LineVec[(ixDim)*2],   label=TempName)

        TempName = InputData.ApproxModel + ', ' + VarName[ixDim]
        plt.plot(t, xPred[:, ixDim], LineVec[(ixDim)*2+1], label=TempName)

    plt.legend()
    plt.grid()
    Title = InputData.PDEName
    plt.title(Title)
    FigPath = InputData.PathToFigFld + '/TestCase' + str(iTestCase+1) + '.png'
    fig.savefig(FigPath, dpi=600)
    #plt.show()
    plt.close()


def video_history(InputData, iTestCase, tData, xData, PredFile, NEpochCurrent):
    ### Requires: sudo apt-get install ffmpeg (Ubuntu) / brew install ffmpeg (MacOS)

    NEpochTemp = int(np.minimum(NEpochCurrent, int(InputData.NEpoch)))

    fig     = plt.figure()
    ax      = plt.axes(xlim=(np.amin(tData), np.amax(tData)), ylim=(np.amin(xData), np.amax(xData)))
    LineVec = ['k-', 'k--', 'r-', 'r--', 'g-', 'g--', 'b-', 'b--', 'p-', 'p--']
    lines   = []
    for ixDim in range(InputData.xDim):
        DataName = 'ODE, '                      + InputData.xNames[ixDim]
        PredName = InputData.ApproxModel + ', ' + InputData.xNames[ixDim]
        lines    = lines + [plt.plot([], [], LineVec[(ixDim)*2], lw=2, label=DataName)[0], plt.plot([], [], LineVec[(ixDim)*2+1], lw=1, label=PredName)[0]]
    plt.legend()
    plt.xlabel('Time [s]')
    plt.grid()


    # Animation function.  This is called sequentially
    def animate(i, xDim, tData, xData, PredFile, read_data, NEpochTest):

        for ixDim in range(xDim):
            lines[(ixDim)*2].set_data(tData, xData[:,ixDim])

        iRun         = i*NEpochTest+1
        PredFile     = PredFile + str(iRun)
        tPred, xPred = read_data(PredFile, xDim)

        for ixDim in range(xDim):
            lines[(ixDim)*2+1].set_data(tPred, xPred[:,ixDim])

        return lines


    # call the animator.  blit=True means only re-draw the parts that have changed.
    #anim = animation.FuncAnimation(fig, animate, init_func=init, frames=40, interval=1, blit=True)
    NFrames = 0
    for iEpoch in range(NEpochTemp):
        if (iEpoch % InputData.NEpochTest == 0):
            NFrames+=1
    anim = animation.FuncAnimation(fig, animate, frames=NFrames, fargs=(InputData.xDim, tData, xData, PredFile, read_data, InputData.NEpochTest, ), interval=1, blit=True)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    VideoFileName = InputData.PathToFigFld + '/TestCase' + str(iTestCase+1) + '.mp4'
    #anim.save(VideoFileName, progress_callback=lambda i, n: print(f'[ProPDE]:   Saving frame {i+1} of {n}'), dpi=600, fps=10, extra_args=['-vcodec', 'libx264'])
    anim.save(VideoFileName, dpi=600, fps=10, extra_args=['-vcodec', 'libx264'])

    plt.close()


# def plot_losseshistory(InputData, Iter, Loss, MSE0, MSEf, MSEr, TimeTrain):

#     fig = plt.figure()
#     plt.xlabel('Iteration')
#     plt.ylabel('Loss')
#     plt.plot(Iter, Loss, 'k', label='Total Loss')
#     plt.plot(Iter, MSE0, 'r', label='Loss from Initial Conditions')
#     plt.plot(Iter, MSEf, 'b', label='Loss from Residuals')
#     plt.plot(Iter, MSEr, 'g', label='Loss from Weight Decays')
#     plt.yscale('log')
#     plt.legend()
#     plt.grid()
#     plt.title('Training History')
#     FigPath = InputData.PathToFigFld + '/LossesHistory.png'
#     fig.savefig(FigPath, dpi=600)
#     #plt.show()
#     plt.close()


def plot_losseshistory(InputData, history):

    fig = plt.figure()
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Error [MPG]')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.title('Training History')
    FigPath = InputData.PathToFigFld + '/LossesHistory.png'
    fig.savefig(FigPath, dpi=1000)
    #plt.show()
    plt.close()