import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator,LogLocator)

import Initialize_Paths as Paths


# Mole fraction Plot
def Plot_MoleFraction(System,QCT,SurQCT,TempVec,MoleFractionXLim):

    fig,ax = plt.subplots(1,1,figsize=(10,10))
    MoleculeName = System.Molecule[0].Name
    
    plt.plot(QCT.time, QCT[MoleculeName], '-k', label='QCT',linewidth=5)
    plt.plot(SurQCT.time, SurQCT[MoleculeName], '-r', label='SurQCT',linewidth=5)
    
    plt.legend(frameon=False)
    plt.xscale('linear')
    plt.xlabel('\\textbf{t [s]}')
    plt.ylabel('\\textbf{X}')
    plt.xlim(MoleFractionXLim)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    fig.tight_layout(pad=0.5)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    return fig

# Energy evolution plot
def Plot_Energies(System,QCT,SurQCT,TempVec,EnergyXLim):
    
    iTemp = 0
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    plt.plot(QCT[iTemp].time, QCT[iTemp].eRot,'--k', label='\\textbf{ERot}',linewidth=3)
    plt.plot(QCT[iTemp].time, QCT[iTemp].eVib, '-k', label='\\textbf{EVib}',linewidth=3)
    
    for iTemp in range(len(TempVec)):
        
        Temp = TempVec[iTemp]
        
        plt.plot(QCT[iTemp].time, QCT[iTemp].eRot,'--k', linewidth=3)
        plt.plot(QCT[iTemp].time, QCT[iTemp].eVib, '-k', linewidth=3)
        
        plt.plot(SurQCT[iTemp].time, SurQCT[iTemp].eRot, color='red', linestyle='dashed', linewidth=5)
        plt.plot(SurQCT[iTemp].time, SurQCT[iTemp].eVib, color='red',linestyle='-', linewidth=5)

        plt.legend(frameon=False)                                                 
        plt.xscale('log')                                                 
        plt.xlabel('\\textbf{t [s]}')
        plt.ylabel('\\textbf{E [eV]}')
        plt.xlim([EnergyXLim[iTemp]])
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
        fig.tight_layout(pad=0.75)
        plt.savefig((Figure_ME_path+System.Name+'_'+ReactionFlgSurQCT+'_T'+str(Temp)+'K_Energy.pdf'), format='pdf', dpi=600)
        
    return fig

# Population plot times
def find_nearest(array, value):
    i = 0
    iStep=[]
    for ivalue in value:
        array = np.asarray(array)
        idx = (np.abs(array - ivalue)).argmin()
        iStep.append(idx)
        i = i+1
    return iStep

# Population plots
def Plot_Populations(iTemp,plot_times,QSSFlg):
    
    iStepVec = find_nearest(QCT[iTemp].time, plot_times)                                              
    iStepVecSurQCT = find_nearest(SurQCT[iTemp].time, plot_times)  

    for iStep in range(len(iStepVec)):
        
        fig,ax = plt.subplots(1,1,figsize=(18,9))
        cmap=mpl.colors.ListedColormap(["k","mediumvioletred","slategray","yellowgreen","sandybrown","sienna","b","c","g","cyan","navy","crimson","limegreen","gold","r","y"])
        
        cp = ax.scatter(DiatData[0]['EInt'], PopQCT[iTemp].Pop_g[iStepVec[iStep],:], c='k',label='QCT')       
        cp = ax.scatter(DiatData[0]['EInt'], PopSurQCT[iTemp].Pop_g[iStepVecSurQCT[iStep],:], c='r',label='SurQCT')
        
        plt.legend(fontsize=50,frameon=False)            
        plt.yscale('log')
        plt.xlabel('$\epsilon$ [eV]')
        plt.ylabel('$N_i/g_i$ [m$^{-3}$]')
        fig.tight_layout(pad=0.5)
        ax.tick_params(axis='x', labelsize=50)
        ax.tick_params(axis='y', labelsize=50)

        if(QSSFlg):
            title='QSS'
            plt.title(title)
            plt.savefig((Figure_ME_path+System.Name+'_T'+str(Temp)+'K_'+ReactionFlgSurQCT+'_pop_'+System.Molecule[0].Name+'_QSS.eps'), format='eps', dpi=150)
        else:
            title='t = '+str(QCT[iTemp].time[iStep])+' s' 
            plt.title(title)
            plt.savefig((Figure_ME_path+System.Name+'_T'+str(Temp)+'K_'+ReactionFlgSurQCT+'_pop_'+System.Molecule[0].Name+'_'+str(iStepVec[iStep])+'.eps'), format='eps', dpi=150)

        return fig
        
def Plot_Populations_vcolor(iTemp,plot_times,QSSFlg):

    v_color = DiatData[0]['vqn'] 
    iStepVec = find_nearest(QCT[iTemp].time, plot_times)                                              
    iStepVecSurQCT = find_nearest(SurQCT[iTemp].time, plot_times)  

    for iStep in range(len(iStepVec)):
        
        fig,ax = plt.subplots(1,1,figsize=(18,9))
        cmap=mpl.colors.ListedColormap(["k","mediumvioletred","slategray","yellowgreen","sandybrown","sienna","b","c","g","cyan","navy","crimson","limegreen","gold","r","y"])
        
        cp = ax.scatter(DiatData[0]['EInt'], PopQCT[iTemp].Pop_g[iStepVec[iStep],:], c=(v_color), cmap=cmap,label='QCT')       
        cp = ax.scatter(DiatData[0]['EInt'], PopSurQCT[iTemp].Pop_g[iStepVecSurQCT[iStep],:], c=(v_color), cmap=cmap, label='SurQCT')
        cbar = fig.colorbar(cp)
        cbar.set_label('vqn',fontsize=40,rotation=270,labelpad=50)
        
        plt.legend(fontsize=50,frameon=False)            
        plt.yscale('log')
        plt.xlabel('$\epsilon$ [eV]')
        plt.ylabel('$N_i/g_i$ [m$^{-3}$]')
        fig.tight_layout(pad=0.5)
        ax.tick_params(axis='x', labelsize=50)
        ax.tick_params(axis='y', labelsize=50)

        if(QSSFlg):
            title='QSS'
            plt.title(title)
            plt.savefig((Figure_ME_path+System.Name+'_T'+str(Temp)+'K_'+ReactionFlgSurQCT+'_pop_'+System.Molecule[0].Name+'_QSS_vcolor.eps'), format='eps', dpi=150)
        else:
            title='t = '+str(QCT[iTemp].time[iStep])+' s' 
            plt.title(title)
            plt.savefig((Figure_ME_path+System.Name+'_T'+str(Temp)+'K_'+ReactionFlgSurQCT+'_pop_'+System.Molecule[0].Name+'_'+str(iStepVec[iStep])+'_vcolor.eps'), format='eps', dpi=150)

        return fig

def Plot_Populations_ecbcolor(iTemp,plot_times,QSSFlg):

    ecb_color = DiatData[0]['ECB'] 
    iStepVec = find_nearest(QCT[iTemp].time, plot_times)                                              
    iStepVecSurQCT = find_nearest(SurQCT[iTemp].time, plot_times)  

    for iStep in range(len(iStepVec)):
        
        fig,ax = plt.subplots(1,1,figsize=(18,9))
        cmap=mpl.colors.ListedColormap(["k","mediumvioletred","slategray","yellowgreen","sandybrown","sienna","b","c","g","cyan","navy","crimson","limegreen","gold","r","y"])
        
        cp = ax.scatter(DiatData[0]['EInt'], PopQCT[iTemp].Pop_g[iStepVec[iStep],:], c=(ecb_color), cmap=cmap,label='QCT')       
        cp = ax.scatter(DiatData[0]['EInt'], PopSurQCT[iTemp].Pop_g[iStepVecSurQCT[iStep],:], c=(ecb_color), cmap=cmap, label='SurQCT')
        cbar = fig.colorbar(cp)
        cbar.set_label('ECB',fontsize=40,rotation=270,labelpad=50)
        
        plt.legend(fontsize=50,frameon=False)            
        plt.yscale('log')
        plt.xlabel('$\epsilon$ [eV]')
        plt.ylabel('$N_i/g_i$ [m$^{-3}$]')
        fig.tight_layout(pad=0.5)
        ax.tick_params(axis='x', labelsize=50)
        ax.tick_params(axis='y', labelsize=50)

        if(QSSFlg):
            title='QSS'
            plt.title(title)
            plt.savefig((Figure_ME_path+System.Name+'_T'+str(Temp)+'K_'+ReactionFlgSurQCT+'_pop_'+System.Molecule[0].Name+'_QSS_ecbcolor.eps'), format='eps', dpi=150)
        else:
            title='t = '+str(QCT[iTemp].time[iStep])+' s' 
            plt.title(title)
            plt.savefig((Figure_ME_path+System.Name+'_T'+str(Temp)+'K_'+ReactionFlgSurQCT+'_pop_'+System.Molecule[0].Name+'_'+str(iStepVec[iStep])+'_ecbcolor.eps'), format='eps', dpi=150)

        return fig

def Plot_KGlobal():

    for iTemp in range(len(TempVec)):
        Temp = TempVec[iTemp]
        # CNH
        Molecule='CN'
        CNH[iTemp]['KDGlobal']=compute_GlobalRates(CNHPop[iTemp].CNPop_g,KDissCNH[:,0],Molecule,CNH[iTemp].time)
    
        # CNH
        fig = plt.figure(figsize=(10,10))
        plt.plot(CNH[iTemp].time, CNH[iTemp].KDGlobal, '-b',linewidth=3)
        plt.legend(frameon=False)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('t [s]')
        plt.ylabel('$k^D_{Global}$ [cm$^3$/s]')
        plt.xlim([1e-13,1e-3])
        plt.ylim([1e-16,5e-11])
        fig.tight_layout(pad=0.5)
        plt.savefig((Fig_path+System[0]+'_T'+str(Temp)+'K_'+ReactionFlg+'_KDissGlobal.eps'), format='eps', dpi=600)


def Plot_taus(System,Data_ME_path,ReactionFlgQCT,ReactionFlgSurQCT):

    QCT_tausFile = Data_ME_path+'/QCT_Taus_'+System.Molecule[0].Name+'_'+ReactionFlgQCT+'.csv'
    QCT_taus = pd.read_csv(QCT_tausFile,header=None,skiprows=1)
    QCT_taus.columns = ['Temp','P','tauInt','tauRot','tauVib'] 
                                                                             
    SurQCT_tausFile = Data_ME_path+'/DNN_Taus_'+System.Molecule[0].Name+'_'+ReactionFlgSurQCT+'.csv'
    SurQCT_taus = pd.read_csv(SurQCT_tausFile,header=None,skiprows=1)
    SurQCT_taus.columns = ['Temp','P','tauInt','tauRot','tauVib'] 
    
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    plt.plot(QCT_taus.Temp, QCT_taus.tauRot, 'ks', markersize=15, label='$\\tau_{Rot}$')
    plt.plot(SurQCT_taus.Temp, SurQCT_taus.tauRot, 'rs', markersize=15)   
    plt.plot(QCT_taus.Temp, QCT_taus.tauVib, 'k^', markersize=15, label='$\\tau_{Vib}$')
    plt.plot(SurQCT_taus.Temp, SurQCT_taus.tauVib, 'r^' , markersize=15)
    
    plt.legend(frameon=False)    
    plt.yscale('log')            
    plt.xlabel('\\textbf{T [K]}')
    plt.ylabel('$\\tau$ \\textbf{[atm*s]}')
    
    plt.ylim([1e-9,1e-7])    
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    fig.tight_layout(pad=2.0) 
    plt.xticks([5000,10000,15000,20000])
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    return fig

def Plot_KDth_qss(System,Data_ME_path,ReactionFlgQCT,ReactionFlgSurQCT):

    QCT_KDFile = Data_ME_path+'/QCT_KGlobal_'+ReactionFlgSurQCT+'_'+System.Molecule[0].Name+'.csv'
    QCT_KD = pd.read_csv(QCT_KDFile,header=None,skiprows=1)
    QCT_KD.columns = ['Temp','KdissTh','KexchTh','KdissQSS','KexchQSS']
    
    SurQCT_KDFile = Data_ME_path+'/DNN_KGlobal_'+ReactionFlgSurQCT+'_'+System.Molecule[0].Name+'.csv'
    SurQCT_KD = pd.read_csv(SurQCT_KDFile,header=None,skiprows=1)
    SurQCT_KD.columns = ['Temp','KdissTh','KexchTh','KdissQSS','KexchQSS']
    
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    plt.plot(10000/QCT_KD.Temp, QCT_KD.KdissTh, 'ks', markersize=10, label='$k^D_{Th}$')
    plt.plot(10000/SurQCT_KD.Temp, SurQCT_KD.KdissTh, '--rs',markersize=7,linewidth=3)
    
    plt.plot(10000/QCT_KD.Temp, QCT_KD.KdissQSS, 'ko', markersize=10, label='$k^D_{QSS}$')
    plt.plot(10000/SurQCT_KD.Temp, SurQCT_KD.KdissQSS, ':ro',markersize=7,linewidth=3)

    plt.legend(frameon=False)
    plt.yscale('log')
    plt.xlabel('\\textbf{10000/T [K}$^{-1}$\\textbf{]}')
    plt.ylabel('$k^D$ \\textbf{[cm}$^3$\\textbf{/s]}')  
    plt.xlim(System.KDXLim)                                                                                              
    plt.ylim(System.KDYLim)
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    fig.tight_layout(pad=2.0) 
    
    return fig 
