import numpy as np

def compute_energy(System,Pop,DiatData,Run):
    # Energy computation
    eRot=np.zeros(Run.NSteps)
    eVib=np.zeros(Run.NSteps)

    #    for iMol in range(len(System.Molecule)):
    iMol = 0
    for iStep in range(0,Run.NSteps):
        Ni = Pop[iStep,:]
        NiTot = np.sum(Ni)   
        eRot[iStep] = sum( DiatData[iMol]['ERot']*Ni ) / NiTot
        eVib[iStep] = sum( DiatData[iMol]['EVibv0Ref']*Ni ) / NiTot
        
    return eRot, eVib

def compute_GlobalRates(Pop,KDiss,Mol,time):
    # Global Rates computation
    NSteps = np.size(time)
    KDGlobal=np.zeros(NSteps)
    iMol=Molecules.index(Mol)
    
    for iStep in range(0,NSteps):
        Ni = Pop[iStep,:]
        NiTot = np.sum(Ni)
        KDGlobal[iStep] = sum( KDiss*Ni )/NiTot

    return KDGlobal    

#def compute_ErrorMoleFraction(QCT,SurQCT):
    
    
