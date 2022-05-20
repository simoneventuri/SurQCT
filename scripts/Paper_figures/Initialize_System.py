import numpy as np
import Initialize_Paths as Paths
from System import system

def Initialize_O3_UMN():   

    SystemName  = 'O3_UMN'
    NbAtoms = 1
    NbMolecules = 1
    NbProcesses = 3
    System = system(SystemName,NbAtoms,NbMolecules,NbProcesses)

    System.Atom[0].Name  = 'O'
    System.Molecule[0].Name = 'O2'
    System.Box_Header = ['time',System.Atom[0].Name,System.Molecule[0].Name,'Temp','Density','Pressure','NbPart','Energy']
    System.QCTMEPath = 'Run_0D/'
    System.PathToDiatFile = [Paths.CoarseAir_path+System.Molecule[0].Name+'/UMN/FromUMN_Sorted.inp']
    System.PathToHDF5Fld  = Paths.Workspace_path + 'Air_Database/HDF5_Database/'

    # Plotting specifications
    System.MoleFractionXLim = [0,3e-6]
    System.KDXLim=[0.5,3.0]
    System.KDYLim=[1.e-15,1.e-9]
    
    return System

def Initialize_N3_NASA():   

    SystemName  = 'N3_NASA'
    NbAtoms = 1
    NbMolecules = 1
    NbProcesses = 3
    System = system(SystemName,NbAtoms,NbMolecules,NbProcesses)

    System.Atom[0].Name  = 'N'
    System.Molecule[0].Name = 'N2'
    System.Box_Header = ['time',System.Atom[0].Name,System.Molecule[0].Name,'Temp','Density','Pressure','NbPart','Energy']
    System.QCTMEPath = 'Run_0D_semi/'
    System.PathToDiatFile = [Paths.CoarseAir_path+System.Molecule[0].Name+'/LeRoy/MyLeroy_FromRobyn.inp']
    System.PathToHDF5Fld  = Paths.Workspace_path + 'Air_Database/HDF5_Database_semiClassicalApprox/'

    # Plotting specifications
    System.MoleFractionXLim = [0,1e-3]
    System.KDXLim=[0.4,1.1]
    System.KDYLim=[1.e-15,1.e-9]
    
    return System

def Initialize_NON_UMN():   

    SystemName  = 'NON_UMN'
    NbAtoms = 2
    NbMolecules = 2
    NbProcesses = 4
    System = system(SystemName,NbAtoms,NbMolecules,NbProcesses)

    System.Atom[0].Name  = 'N'
    System.Atom[1].Name  = 'O'
    System.Molecule[0].Name = 'NO'
    System.Molecule[1].Name = 'N2'
    System.Box_Header = ['time',System.Atom[0].Name,System.Atom[1].Name,System.Molecule[1].Name,System.Molecule[0].Name,'Temp','Density','Pressure','NbPart','Energy']
    System.QCTMEPath = 'Run_0D/'
    System.PathToDiatFile = [Paths.CoarseAir_path+System.Molecule[0].Name+'/UMN/Recomputed.inp',
                             Paths.CoarseAir_path+System.Molecule[1].Name+'/UMN_ForN2O2/Recomputed.inp']
    System.PathToHDF5Fld  = Paths.Workspace_path + 'Air_Database/HDF5_Database/'

    # Plotting specifications
    System.MoleFractionXLim = [0,3e-6]

    return System
