import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter

import Initialize_Paths as Paths

# Mole fraction Plot
def Plot_MoleFraction(System,QCT,SurQCT,TempVec):
    
    for iTemp in range(len(TempVec)):
        Temp = TempVec[iTemp]

        fig,ax = plt.subplots(1,1,figsize=(8,8))

        MoleculeName = System.Molecule[0].Name
        plt.plot(QCT[iTemp].time, QCT[iTemp][MoleculeName], '-k', label='QCT',linewidth=3)
        plt.plot(SurQCT[iTemp].time, SurQCT[iTemp][MoleculeName], '-r', label='SurQCT',linewidth=3)
        
        plt.legend(frameon=False)
        plt.xscale('linear')
        plt.xlabel('t [s]')
        plt.ylabel('X')
        plt.xlim(System.MoleFractionXLim)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.set_aspect('equal', adjustable='box')
        fig.tight_layout(pad=0.5)
        #plt.savefig((Fig_path+System[0]+'_T'+str(Temp)+'K_'+ReactionFlg+'_X.eps'), format='eps', dpi=600)

        return fig

def Plot_Energies(System,QCT,SurQCT,TempVec):

    for iTemp in range(len(TempVec)):
        Temp = TempVec[iTemp]

        fig,ax = plt.subplots(1,1,figsize=(5,5))
        plt.plot(QCT[iTemp].time, QCT[iTemp].eRot,'--k', label='ERot',linewidth=3)
        plt.plot(QCT[iTemp].time, QCT[iTemp].eVib, '-k', label='EVib',linewidth=3)
        plt.plot(QCT[iTemp].time, QCT[iTemp].eRot,'--r', linewidth=3)
        plt.plot(QCT[iTemp].time, QCT[iTemp].eVib, '-r', linewidth=3)
        
        plt.legend(frameon=False)
        plt.xscale('log')
        plt.xlabel('t [s]')
        plt.ylabel('E [eV]')
        plt.xlim([1e-12,1e-3])
        fig.tight_layout(pad=0.5)
        #plt.savefig((Fig_path+System[0]+'_T'+str(Temp)+'K_'+ReactionFlg+'_Energy.eps'), format='eps', dpi=600)

        return fig
    
def Plot_Populations():

    iTemp=0
    plot_times=[4e-6]
    iStepVec = find_nearest(QCT[iTemp].time, plot_times)
    
    for iStep in iStepVec:
        # CNH
        fig,ax = plt.subplots(1,1,figsize=(20,9))
        
        cmap=mpl.colors.ListedColormap(["k","mediumvioletred","slategray","yellowgreen","sandybrown","sienna","b","c","g","cyan","navy","crimson","limegreen","gold","r","y"])
        #     v_color = DiatData[0]['vqn']
        #     ecb_color = DiatData[0]['ECB']
        cp = ax.scatter(PopSurQCT[iTemp].Energy[iStep,:], PopQCT[iTemp].Pop_g[iStep,:], c='k')
        cp = ax.scatter(PopSurQCT[iTemp].Energy[iStep,:], PopSurQCT[iTemp].Pop_g[iStep,:], c='r')
        cbar = fig.colorbar(cp)
        cbar.set_label('vqn',fontsize=40,rotation=270,labelpad=50)
        
        #     title='t = '+str(CNH[iTemp].time[iStep])+' s'
        plt.title(title)
        plt.legend(frameon=False)
        plt.yscale('log')
        plt.xlabel('$\epsilon$ [eV]')
        plt.ylabel('$N_i/g_i$ [m$^{-3}$]')
        fig.tight_layout(pad=0.5)
        #     plt.savefig((Fig_path+System[0]+'_T'+str(TempVec[iTemp])+'K_'+ReactionFlg+'_pop_'+Molecules[0]+str(iStep)+'.eps'), format='eps', dpi=600)
        #     plt.savefig((Fig_path+System[0]+'_T'+str(TempVec[iTemp])+'K_'+ReactionFlg+'_pop_QSS_ECB.eps'), format='eps', dpi=600)


        

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


def Plot_taus(System):
    
    QCT_tausFile = Paths.Data_ME_path+'/QCT_Taus_'+System.Molecule[0].Name+'_0_1_1_0.csv'
    QCT_taus = pd.read_csv(QCT_tausFile,header=None,skiprows=1)
    QCT_taus.columns = ['Temp','tauInt','tauRot','tauVib']

    SurQCT_tausFile = Paths.Data_ME_path+'/DNN_Taus_'+System.Molecule[0].Name+'_0_1_1_0.csv'
    SurQCT_taus = pd.read_csv(DNN_tausFile,header=None,skiprows=1)
    SurQCT_taus.columns = ['Temp','tauInt','tauRot','tauVib']
    
    return fig


def Plot_KDth_qss(System):

    QCT_KDFile = Paths.Data_ME_path+'/QCT_KGlobal_'+System.Molecule[0].Name+'_0_1_1_0.csv'
    QCT_KD = pd.read_csv(QCT_KDFile,header=None,skiprows=1)
    QCT_KD.columns = ['Temp','KdissTh','KexchTh','KdissQSS','KexchQSS']

    SurQCT_KDFile = Paths.Data_ME_path+'/DNN_KGlobal_'+System.Molecule[0].Name+'_0_1_1_0.csv'
    SurQCT_KD = pd.read_csv(DNN_KDFile,header=None,skiprows=1)
    SurQCT_KD.columns = ['Temp','KdissTh','KexchTh','KdissQSS','KexchQSS']

    plt.plot(10000/QCT_KD.Temp, QCT_KD.KdissTh, '--ks')
    plt.plot(10000/SurQCT_KD.Temp, SurQCT_KD.KdissTh, 'rs', markersize=10)
    plt.legend(frameon=False)
    plt.yscale('log') 
    plt.xlabel('10000/T')
    plt.ylabel('$k^D$ [cm$^3$/s]')
    plt.xlim([0,3])
    plt.ylim([1e-15,1e-9])
    #plt.savefig((Fig_path+'CH_kDthermal_k1k2k3.eps'), format='eps', dpi=600, bbox_inches = 'tight')

    return fig
