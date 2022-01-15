% -- MATLAB --
%%==============================================================================================================
% 
% Surrogate Model for quasi-classical trajectory calculations using
% DeepOnet
% 
% Copyright (C) 2021 Maitreyee Sharma (University of Illinois at Urbana-Champaign). 
%
% This program is free software; you can redistribute it and/or modify it under the terms of the 
% Version 2.1 GNU Lesser General Public License as published by the Free Software Foundation. 
% 
% This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
% without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
% See the GNU Lesser General Public License for more details. 
% 
% You should have received a copy of the GNU Lesser General Public License along with this library; 
% if not, write to the Free Software Foundation, Inc. 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA 
% 
%---------------------------------------------------------------------------------------------------------------
%%==============================================================================================================

clear all 
close all
clc

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1200 1000]) 
prev = st_set_graphics_defaults();

global Input Syst Temp Param Kin Rates OtherSyst OtherRates


%% Input Specification
Input.WORKSPACE_PATH            = '/home/venturi/WORKSPACE/'
Input.Paths.ToQCTFldr           = strcat(Input.WORKSPACE_PATH, '/CoarseAIR/O3_ALL/Test/');
Input.Paths.ToKinMainFldrQCT    = strcat(Input.WORKSPACE_PATH, '/Air_Database/Run_0D');
Input.Paths.ToHDF5Fldr          = strcat(Input.WORKSPACE_PATH, '/Air_Database/HDF5_Database/');
Input.Kin.RateSourceQCT         = 'HDF5'; % CoarseAIR / CG-QCT / HDF5 / PLATO

Input.TranVec                   = [10000];%[1500, 2500, 5000, 6000, 8000, 10000, 12000, 14000, 15000, 20000];
Input.SystNameLong              = 'O3_UMN';
Input.iPES                      = 0;
Input.Suffix                    = ''
Input.RunSuffix                 = '';

Input.Kin.MolResolutionIn       = [{'StS'}];
Input.Kin.EqNStatesIn           = [   6115];
Input.Kin.MinStateIn            = [      1];
Input.Kin.MaxStateIn            = [   6115];
Input.Kin.PathToMappingIn       = [   {''}];
Input.Kin.PathToWriteMappingIn  = [   {''}];
Input.Kin.NGroupsIn             = [      0];
Input.Kin.MolResolutionOut      = [{'CGM'}];
Input.Kin.PathToMappingOut      = [   {''}];
Input.Kin.CGM_Strategy          = [{'CBM'}];
Input.Kin.ParamsGroupsOut       = [    1.0];
Input.Kin.NGroupsOut            = [     45];
Input.Kin.PathToWriteMappingOut = [{'/home/venturi/WORKSPACE/Air_Database/Run_0D/database/grouping/'}];

Input.Kin.Proc.DissFlg          = 2;
Input.Kin.NBinsSuffix           = 0;
Input.Kin.DissCorrFactor        = 16.0/3.0;
Input.Kin.Proc.DissInelFlg      = 0;
Input.Kin.Proc.InelFlg          = 1;
Input.Kin.Proc.ExchFlg1         = 0;
Input.Kin.Proc.ExchFlg2         = 0;

Input.Kin.ReadRatesProc         = [0,0,0]%[2, 2, 2]
Input.Kin.ReadOtherSyst         = []
Input.Kin.OtherSystInHDF5       = []

Input.FigureFormat              = 'PrePrint';
Input.ReLoad                    = 1;

%% Inputs for Plotting
Input.iFig               = 101;
Input.SaveFigsFlgInt     = 0;
Input.Paths.SaveFigsFldr = strcat(Input.WORKSPACE_PATH, '/SurQCT/AviationPaper/Figures/');

%% CoarseAIR
% Recomputing Levels' Properties
Input.Tasks.ComputeLevelProps.Flg                      = false
% Writing Levels' Properties
Input.Tasks.Write_LevelInfo.Flg                        = false
Input.Tasks.Write_LevelInfo.Path                       = [{'/home/venturi/WORKSPACE/Air_Database/Run_0D/database/levels/'}]
% Plotting Diatomic Potential
Input.Tasks.Plot_DiatPot.Flg                           = false;
Input.Tasks.Plot_DiatPot.MoleculesOI                   = [1];
Input.Tasks.Plot_DiatPot.Extremes                      = [1.5, 8.0; 1.5, 6.0];
Input.Tasks.Plot_DiatPot.jqnVec                        = [0, 100, 200];
% Plotting Overall Rate Coefficients (Dissociation and Exchange)
Input.Tasks.Plot_OverallRates.Flg                      = false;
% Plotting Pair Contributions to Dissociation Rate Coefficients
Input.Tasks.Plot_DifferentDissRates.Flg                = false;
% Writing Rates for Paraview
Input.Tasks.Write_RatesParaview.Flg                    = true;
Input.Tasks.Write_RatesParaview.MinRate                = [1e-12, 1e-12, 1.e-12]
Input.Tasks.Write_RatesParaview.Proc                   = [false, true, true]
% Input.Tasks.Write_RatesParaview.vqns                   = [0, 10,  0,20,40, 30,60, 30, 20, 20,  7, 10, 30, 25, 45, 5, 10, 10]
% Input.Tasks.Write_RatesParaview.jqns                   = [0,150,240,30,60,120,10,180,150,170,120, 50,  0, 90,110,90,210,250]
% Input.Tasks.Write_RatesParaview.vqns                   = [ 0,10,  8,31, 21]
% Input.Tasks.Write_RatesParaview.jqns                   = [34,34,206,24, 138]
Input.Tasks.Write_RatesParaview.vqns                   = [ 10, 20, 15, 5]
Input.Tasks.Write_RatesParaview.jqns                   = [ 34, 102,120, 180]
Input.Tasks.Write_RatesParaview.IncludeExch            = false
% Writing Rates for Clustering
Input.Tasks.Write_RatesForClustering.Flg               = false;
Input.Tasks.Write_RatesForClustering.MinRate           = 1.e-15;
Input.Tasks.Write_RatesForClustering.WriteFldr         = strcat('/home/venturi/WORKSPACE/SpectralCluster/data/');
Input.Tasks.Write_RatesForClustering.MinState          = 1;
Input.Tasks.Write_RatesForClustering.MaxState          = 100000;
Input.Tasks.Write_RatesForClustering.IncludeExch       = true;
% Writing Rates as A Network
Input.Tasks.Write_RatesAsNetwork.Flg                   = false;
Input.Tasks.Write_RatesAsNetwork.MinRate               = 5.e-13;
Input.Tasks.Write_RatesAsNetwork.WriteFldr             = strcat('/home/venturi/WORKSPACE/SpectralCluster/data/');
Input.Tasks.Write_RatesAsNetwork.MinState              = 1;
Input.Tasks.Write_RatesAsNetwork.MaxState              = 100000;
Input.Tasks.Write_RatesAsNetwork.IncludeExch           = true;
% Compute Grouped Rate Coefficients
Input.Tasks.Compute_GroupedRates.Flg                   = false;
% Plotting Reconstructed Rate Coefficients
Input.Tasks.Plot_ReconstructedRates.Flg                = false;

%% KONIG and PLATO
% Plotting Mole Fractions
Input.Tasks.Plot_MoleFracs.Flg                         = false;
Input.Tasks.Plot_MoleFracs.CompStart                   = 1;
Input.Tasks.Plot_MoleFracs.CompEnd                     = 2;
Input.Tasks.Plot_MoleFracs.Normalize                   = 0;
% Plotting Global Rates
Input.Tasks.Plot_GlobalRates.Flg                       = false;
Input.Tasks.Plot_GlobalRates.MoleculesOI               = [1];
% Plotting Mole Fractions and Global Rates
Input.Tasks.Plot_MoleFracs_and_GlobalRates.Flg         = false;
Input.Tasks.Plot_MoleFracs_and_GlobalRates.CompStart   = 2;
Input.Tasks.Plot_MoleFracs_and_GlobalRates.CompEnd     = 2;
Input.Tasks.Plot_MoleFracs_and_GlobalRates.MoleculesOI = [1];
% Plotting Vib. Distribution Function
Input.Tasks.Plot_VDF.Flg                               = false;
Input.Tasks.Plot_VDF.MoleculesOI                       = [1];
Input.Tasks.Plot_VDF.tSteps                            = [1.e-14, 1e-12, 1e-10, 1e-8, 1e-6]%[8.94e-7]%[7.e-6, 30e-6, 100e-6, 5.e-3];
% Plotting RVS Populations
Input.Tasks.Plot_Populations.Flg                       = false;
Input.Tasks.Plot_Populations.MoleculesOI               = [1];
Input.Tasks.Plot_Populations.tSteps                    = [1e-10, 1e-8] %[1.e-13, 1e-12, 1.e-11, 1e-10, 1e-9, 1e-8]%[8.94e-7]%[7.e-6, 30e-6, 100e-6, 5.e-3];
Input.Tasks.Plot_Populations.GroupColors               = 0;
Input.Tasks.Plot_Populations.ColorIdx                  = 1;
% Plotting RVS Populations Vqn Specific
Input.Tasks.Plot_PopulationsVqnSpecific.Flg            = false;
Input.Tasks.Plot_PopulationsVqnSpecific.MoleculesOI    = [1];
Input.Tasks.Plot_PopulationsVqnSpecific.tSteps         = [1.e-14, 1.e-13, 1e-12, 1.e-11, 1e-10, 1.e-9, 1e-8, 1e-7, 1e-6, 1e-5]%[1e-10, 1e-8] %[8.94e-7]%[7.e-6, 30e-6, 100e-6, 5.e-3];
Input.Tasks.Plot_PopulationsVqnSpecific.GroupColors    = 2;
% Plotting Energies
Input.Tasks.Plot_Energies.Flg                          = false;
Input.Tasks.Plot_Energies.MoleculesOI                  = [1];
Input.Tasks.Plot_Energies.LTFlag                       = false;
% Plotting Energy Depletions
Input.Tasks.Plot_EnergyDepletions.Flg                  = false;
Input.Tasks.Plot_EnergyDepletions.MoleculesOI          = [1];
Input.Tasks.Plot_EnergyDepletions.RemovalProc          = [1];
Input.Tasks.Plot_EnergyDepletions.Proj                 = [1,1];
Input.Tasks.Plot_EnergyDepletions.Targ                 = [2];

Input.Kin.ReadRatesProc         = [2, 2, 2, 0]

%% Initializing
Syst.NameLong = Input.SystNameLong;
Syst          = Initialize_ChemicalSyst(Syst)
Initialize_Parameters()
Initialize_Input()

%% Reading Quantities

if Input.ReLoad > 0 
    % Reading Levels Info
    Syst = Read_LevelInfo(Syst)
    for iSyst = 1:length(Input.Kin.ReadOtherSyst)
        if (Input.Kin.ReadOtherSyst(iSyst))
            OtherSyst(iSyst).Syst = Read_LevelInfo(OtherSyst(iSyst).Syst);
        end
    end
    
    if (Input.Tasks.Write_LevelInfo.Flg)
        Write_LevelInfo(Input.Tasks.Write_LevelInfo)
    end
    
    % Grouping the Levels in Output
    Group_Out()

end


%     
fileName = strcat('./',MoleculesName(iBinnedMol,:),'_Mapping_CB',num2str(NBins),'.csv');                                                                                                                                               
fileID   = fopen(fileName,'w');                                                                                                                                                                                                        
fprintf(fileID,'#Level,Bin\n');                                                                                                                                                                                                        
for iLevels = 1:NLevels                                                                                                                                                                                                                
  iBin = 1;                                                                                                                                                                                                                            
  while (DeltaEintDiss(iLevels,iBinnedMol) >= -Extr(iBin))                                                                                                                                                                             
    iBin = iBin + 1;                                                                                                                                                                                                                   
  end                                                                                                                                                                                                                                  
  iBin = iBin - 1;                                                                                                                                                                                                                     
  LevelToBin(iLevels) = iBin;                                                                                                                                                                                                          
  fprintf(fileID,'%i,%i\n',iLevels,LevelToBin(iLevels));                                                                                                                                                                               
end                                                                                                                                                                                                                                    
fclose(fileID);  

%% Writing Levels for Sur QCT
iMol = 1;
FileName           = strcat('/home/venturi/WORKSPACE/Air_Database/Run_0D/database/levels/N2_vDissRef.csv' );
fileID = fopen(FileName,'w');
fprintf(fileID,'vqn,jqn,EVib,ERot,rMin,rMax,VMin,VMax,Tau,ri,ro\n');
for jLevel = 1:Syst.Molecule(iMol).NLevels
        v = Syst.Molecule(iMol).Levelvqn(jLevel);
        fprintf(fileID,'%i,%i,%e,%e,%e,%e,%e,%e,%e,%e,%e\n', ...
          Syst.Molecule(iMol).Levelvqn(jLevel),     ...
          Syst.Molecule(iMol).Leveljqn(jLevel),     ...
          Syst.Molecule(iMol).vEeVVib(v+1),           ...
          Syst.Molecule(iMol).LevelEeVRot(jLevel),  ...
          Syst.Molecule(iMol).LevelrMin(jLevel),    ...
          Syst.Molecule(iMol).LevelrMax(jLevel),    ...
          Syst.Molecule(iMol).LevelVMin(jLevel),    ...
          Syst.Molecule(iMol).LevelVMax(jLevel),    ...
          Syst.Molecule(iMol).LevelTau(jLevel),     ...
          Syst.Molecule(iMol).LevelrIn(jLevel),     ...
          Syst.Molecule(iMol).LevelrOut(jLevel));
end
fclose(fileID);