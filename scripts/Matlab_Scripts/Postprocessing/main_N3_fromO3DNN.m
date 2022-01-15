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
%close all
clc

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1000 1000]) 
prev = st_set_graphics_defaults();

global Input Syst Temp Param Kin Rates OtherSyst OtherRates


%% Input Specification
Input.WORKSPACE_PATH            = '/home/venturi/WORKSPACE/'
Input.Paths.ToQCTFldr           = strcat(Input.WORKSPACE_PATH, '/CoarseAIR/O3_ALL/Test/');
Input.Paths.ToKinMainFldrQCT    = strcat(Input.WORKSPACE_PATH, '/Air_Database/Run_0D_semi/');
Input.Paths.ToHDF5Fldr          = strcat(Input.WORKSPACE_PATH, '/Air_Database/HDF5_Database_semiClassicalApprox/');
%Input.Paths.ToHDF5Fldr          = strcat(Input.WORKSPACE_PATH, '/Air_Database/HDF5_Database/');
Input.Kin.RateSourceQCT         = 'HDF5'; % CoarseAIR / CG-QCT / HDF5 / PLATO

Input.DNN.nondim = true;
Input.DNN.nondimfldr='';
if(Input.DNN.nondim)
    Input.DNN.nondimfldr='transfer_';
end

Input.Inel.TestNum = '4';
Input.Exch.TestNum = '4';
Input.Diss.TestNum = '55';
Input.Paths.ToKinMainFldrDNN    = strcat(Input.WORKSPACE_PATH, '/Air_Database/Run_0D_surQCT/');
Input.Kin.RateSourceDNN        = 'PLATO'; % CoarseAIR / CG-QCT / HDF5 / PLATO

Input.TranVec                   = [10000];%[1500, 2500, 5000, 6000, 8000, 10000, 12000, 14000, 15000, 20000];
Input.SystNameLong              = 'N3_NASA'; 
Input.iPES                      = 0;
Input.Suffix                    = ''
Input.RunSuffix                 = '';

Input.Kin.MolResolutionIn       = [{'StS'}];                                                                                                                                                                                                                                
Input.Kin.EqNStatesIn           = [   9399];
Input.Kin.MinStateIn            = [      1];
Input.Kin.MaxStateIn            = [   9399];
Input.Kin.PathToMappingIn       = [   {''}];
Input.Kin.PathToWriteMappingIn  = [   {''}];
Input.Kin.NGroupsIn             = [      0];
Input.Kin.MolResolutionOut      = [{'StS'}];
Input.Kin.PathToMappingOut      = [   {''}];
Input.Kin.CGM_Strategy          = [{'CBM'}];
Input.Kin.ParamsGroupsOut       = [    1.0];
Input.Kin.NGroupsOut            = [     61];
Input.Kin.PathToWriteMappingOut = [{'/home/venturi/WORKSPACE/Air_Database/Run_0D/database/grouping/'}];

Input.Kin.Proc.DissFlg          = 1;
Input.Kin.NBinsSuffix           = 0;
Input.Kin.DissCorrFactor        = 1;
Input.Kin.Proc.DissInelFlg      = 0;
Input.Kin.Proc.InelFlg          = 1;
Input.Kin.Proc.DNNInelFlg       = 100;
Input.Kin.Proc.ExchFlg1         = 1;
Input.Kin.Proc.DNNExchFlg1      = 100;
Input.Kin.Proc.ExchFlg2         = 0;

Input.Kin.ReadRatesProc         = [0,0,0]%[2, 2, 2]
Input.Kin.ReadOtherSyst         = []
Input.Kin.OtherSystInHDF5       = []

Input.FigureFormat              = 'PrePrint';
Input.ReLoad                    = 1;

%% Inputs for Plotting
Input.iFig               = 101;
Input.SaveFigsFlgInt     = 0;
Input.Paths.SaveFigsFldr = strcat(Input.WORKSPACE_PATH, '/SurQCT/O3forN3/');

%% Tasks Inputs
Input.Tasks.All = false

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
Input.Tasks.Write_RatesParaview.vqns                   = [ 10, 20, 15, 5, 59]
Input.Tasks.Write_RatesParaview.jqns                   = [ 34, 102,120, 180, 3]
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
Input.Tasks.Plot_VDF.tSteps                            = [1.e-14, 1e-12, 1e-10, 1e-8]%[8.94e-7]%[7.e-6, 30e-6, 100e-6, 5.e-3];
% Plotting RVS Populations
Input.Tasks.Plot_Populations.Flg                       = true;
Input.Tasks.Plot_Populations.MoleculesOI               = [1];
Input.Tasks.Plot_Populations.tSteps                    = [1e-8, 1e-7] %[1.e-13, 1e-12, 1.e-11, 1e-10, 1e-9, 1e-8]%[8.94e-7]%[7.e-6, 30e-6, 100e-6, 5.e-3];
Input.Tasks.Plot_Populations.PercEnergy                = [0.25,0.50,0.75];
Input.Tasks.Plot_Populations.GroupColors               = 0;
Input.Tasks.Plot_Populations.ColorIdx                  = 1;
% Plotting RVS Populations Vqn Specific
Input.Tasks.Plot_PopulationsVqnSpecific.Flg            = false;
Input.Tasks.Plot_PopulationsVqnSpecific.MoleculesOI    = [1];
Input.Tasks.Plot_PopulationsVqnSpecific.tSteps         = [1.e-14, 1.e-13, 1e-12, 1.e-11, 1e-10, 1.e-9, 1e-8, 1e-7, 1e-6, 1e-5]%[1e-10, 1e-8] %[8.94e-7]%[7.e-6, 30e-6, 100e-6, 5.e-3];
Input.Tasks.Plot_PopulationsVqnSpecific.GroupColors    = 2;
% Plotting Energies
Input.Tasks.Plot_Energies.Flg                          = true;
Input.Tasks.Plot_Energies.MoleculesOI                  = [1];
Input.Tasks.Plot_Energies.LTFlag                       = false;
% Plotting Energy Depletions
Input.Tasks.Plot_EnergyDepletions.Flg                  = false;
Input.Tasks.Plot_EnergyDepletions.MoleculesOI          = [1];
Input.Tasks.Plot_EnergyDepletions.RemovalProc          = [1];
Input.Tasks.Plot_EnergyDepletions.Proj                 = [1,1];
Input.Tasks.Plot_EnergyDepletions.Targ                 = [2];

Input.Kin.ReadRatesProc         = [2, 2, 2, 0]

%% NN Errors
Input.Tasks.ErrorMolFracs = false;
Input.Tasks.ErrorPopulations = false;
Input.Tasks.ErrorPopulationsOverg = true;
Input.Tasks.ErrorPopulations_PercEnergy = false;
Input.Tasks.StateEnergy = false;
Input.Tasks.StateKDiss = false;
Input.Tasks.EnergyContribution = false;
Input.Tasks.ErrorPopulationsTraining = false;
Input.Tasks.ErrorRates = false;

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

% Inputs for Saving Data
Input.Paths.SaveDataFldr = strcat(Input.WORKSPACE_PATH, '/SurQCT/0D/Data/',Input.SystNameLong,'/',Input.DNN.nondimfldr,'RunI',Input.Inel.TestNum,'_E',Input.Exch.TestNum,'_D',Input.Diss.TestNum,'/');

Input.KinDNN.Proc.OverallFlg = strcat(num2str(Input.Kin.Proc.DissFlg),'_',num2str(Input.Kin.Proc.DNNInelFlg),'_',num2str(Input.Kin.Proc.DNNExchFlg1),'_',num2str(Input.Kin.Proc.ExchFlg2));
   
            
iFigStart = Input.iFig;
% Looping On Translational Temperatures
for iT = 1:length(Temp.TranVec)
    Temp.iT       = iT;
    Temp.TNow     = Temp.TranVec(iT);
    Temp.TNowChar = num2str(Temp.TranVec(iT));
    Input.iFig    = iFigStart;
    Input.RunSuffix

    Input.Paths.ToKinRunFldr = strcat(Input.Paths.ToKinMainFldrQCT, '/output_', Syst.NameLong, Input.RunSuffix, '_T', Temp.TNowChar, 'K_', Input.Kin.Proc.OverallFlg);
    PathToKinRunFldrQCT = strcat(Input.Paths.ToKinMainFldrQCT,'/output_', Syst.NameLong, Input.RunSuffix, '_T', Temp.TNowChar, 'K_', Input.Kin.Proc.OverallFlg);
    PathToKinRunFldrDNN = strcat(Input.Paths.ToKinMainFldrDNN,'/', Input.DNN.nondimfldr,'RunI',Input.Inel.TestNum,'_E',Input.Exch.TestNum,'_D',Input.Diss.TestNum,'/output_', Syst.NameLong, Input.RunSuffix, '_T', Temp.TNowChar,'K_',Input.KinDNN.Proc.OverallFlg);
%     PathToKinRunFldrQCT = PathToKinRunFldrDNN

    if Input.ReLoad > 0 
        %close all
        % Reading Quantities
        global Rates Kin
        % Reading Group Energies and Part Funcs
        Syst = Read_EeV_and_Q_CG(Syst) 
        for iSyst = 1:length(Input.Kin.ReadOtherSyst)
            if (Input.Kin.ReadOtherSyst(iSyst))
                OtherSyst(iSyst).Syst = Read_EeV_and_Q_CG(OtherSyst(iSyst).Syst);
            end
        end
        
        % Compute Equilibrium Constants
        Compute_EqConsts()
        
        if (Input.Tasks.Plot_OverallRates.Flg              || ...
            Input.Tasks.Plot_DifferentDissRates.Flg        || ...
            Input.Tasks.Write_RatesParaview.Flg            || ...
            Input.Tasks.Write_RatesForClustering.Flg       || ...
            Input.Tasks.Write_RatesAsNetwork.Flg           || ...
            Input.Tasks.Plot_GlobalRates.Flg               || ...
            Input.Tasks.Plot_Populations.Flg               || ...
            Input.Tasks.Plot_PopulationsVqnSpecific.Flg    || ...
            Input.Tasks.Plot_MoleFracs_and_GlobalRates.Flg || ...
            Input.Tasks.Plot_Energies.Flg                  || ...
            Input.Tasks.Plot_EnergyDepletions.Flg          || ...
            (sum(Input.Kin.ReadRatesProc)>0) || ...
        Input.Tasks.ErrorRates) 
       
            
            % Rates folder path for Plato Rates Reading
            RatesFldrI = strcat(Input.Paths.ToKinMainFldrDNN, '/database/kinetics/', Input.DNN.nondimfldr,Syst.NameLong,'_Active_Run',Input.Inel.TestNum,'/T', Temp.TNowChar, 'K/');
            RatesFldrE = strcat(Input.Paths.ToKinMainFldrDNN, '/database/kinetics/', Input.DNN.nondimfldr,Syst.NameLong,'_Active_Run',Input.Exch.TestNum,'/T', Temp.TNowChar, 'K/');
            RatesFldrD = strcat(Input.Paths.ToKinMainFldrDNN, '/database/kinetics/', Syst.NameLong,'_Active_Run',Input.Diss.TestNum,'/T', Temp.TNowChar, 'K/');
%            RatesFldrD = strcat(Input.Paths.ToKinMainFldrQCT, '/database/kinetics/',Syst.NameLong,'/T', Temp.TNowChar, 'K/');
            RateSourceQCT = Input.Kin.RateSourceQCT;
            RateSourceDNN = Input.Kin.RateSourceDNN;
            
            % Reading Rates
            Read_Rates(RatesFldrI,RatesFldrD,RatesFldrE,RateSourceQCT)
            RatesQCT = Rates;
%            Read_Rates(RatesFldrI,RatesFldrD,RatesFldrE,RateSourceDNN)
            RatesDNN = Rates; 
%             if (Input.Kin.Proc.DNNInelFlg == 2)
%                 Rates.T(Temp.iT).Inel = RatesQCT.T(Temp.iT).Inel;
%             end
%             if (Input.Kin.Proc.DNNExchFlg1 == 2)
%                 RatesDNN.T(Temp.iT).ExchType(1).Exch = RatesQCT.T(Temp.iT).ExchType(1).Exch;
%             end
        end
        
        if (Input.Tasks.Plot_MoleFracs.Flg                 || ...
            Input.Tasks.Plot_GlobalRates.Flg               || ...
            Input.Tasks.Plot_MoleFracs_and_GlobalRates.Flg || ...
            Input.Tasks.Plot_VDF.Flg                       || ...
            Input.Tasks.Plot_Populations.Flg               || ...
            Input.Tasks.Plot_PopulationsVqnSpecific.Flg    || ...
            Input.Tasks.Plot_Energies.Flg                  || ...
            Input.Tasks.Plot_EnergyDepletions.Flg)
        
            SemiIndicator = false;
            % Reading Thermodynamics Variables Outputted by KONIG
            Read_KONIGBox(PathToKinRunFldrQCT)
            % Reading Level/Group Population Outputted by KONIG
            Read_Pops(PathToKinRunFldrQCT,SemiIndicator)    
            QCT=Kin;
            
            SemiIndicator = false;            
            % Reading Thermodynamics Variables Outputted by KONIG
            Read_KONIGBox(PathToKinRunFldrDNN)
            % Reading Level/Group Population Outputted by KONIG
            Read_Pops(PathToKinRunFldrDNN,SemiIndicator)    
            DNN=Kin;
           
        end
                
        
        %%%% Computing Quantities %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %
        
        if (Input.Tasks.Compute_GroupedRates.Flg || Input.Tasks.Plot_ReconstructedRates.Flg)
           
           %% Grouping the Rate Coefficients
           RatesQCT = Compute_GroupedRates(RatesQCT);
           RatesDNN = Compute_GroupedRates(RatesDNN)
		
        end
        
        if ( (sum(Input.Kin.ReadRatesProc)>0) )
        
            %% Computing Thermal Rates
            RatesQCT = Compute_Rates_Thermal(RatesQCT);   
            RatesDNN = Compute_Rates_Thermal(RatesDNN);   
        
        end
        
        if ((Input.Tasks.Plot_Populations.Flg            && Input.Kin.Proc.DissFlg > 0) || ...
            (Input.Tasks.Plot_PopulationsVqnSpecific.Flg && Input.Kin.Proc.DissFlg > 0) || ...
            Input.Tasks.Plot_GlobalRates.Flg               || ...
            Input.Tasks.Plot_MoleFracs_and_GlobalRates.Flg || ...
            Input.Tasks.Plot_EnergyDepletions.Flg)

            %% Computing Thermal Rates
            RatesQCT = Compute_Rates_Global(QCT, RatesQCT);     
            RatesDNN = Compute_Rates_Global(DNN, RatesDNN);   
        
        end
        
        if ((Input.Tasks.Plot_Populations.Flg            && Input.Kin.Proc.DissFlg > 0) || ...
            (Input.Tasks.Plot_PopulationsVqnSpecific.Flg && Input.Kin.Proc.DissFlg > 0) || ...
            Input.Tasks.Plot_GlobalRates.Flg                                 || ...
            Input.Tasks.Plot_MoleFracs_and_GlobalRates.Flg                   || ...
            Input.Tasks.Plot_EnergyDepletions.Flg)

            %Computing Rate Values and Initial-Final Times for QSS 
            [RatesQCT, QCT] = Compute_QSS(RatesQCT,QCT)
            [RatesDNN, DNN] = Compute_QSS(RatesDNN,DNN)
            
        end
        
        if (Input.Tasks.Plot_Energies.Flg                  || ...
            Input.Tasks.Plot_EnergyDepletions.Flg)
        
            % Computing Energies
            SemiIndicator = false;
            QCT = Compute_Energies(Input.Tasks.Plot_EnergyDepletions,QCT,RatesQCT,SemiIndicator);
            SemiIndicator = false;
            DNN = Compute_Energies(Input.Tasks.Plot_EnergyDepletions,DNN,RatesDNN,SemiIndicator);

        end
        
        if (Input.Tasks.Plot_EnergyDepletions.Flg)
            
            %% Computing Energy Depletions
            QCT = Compute_EnergyDepletions(Input.Tasks.Plot_EnergyDepletions,QCT,RatesQCT);
            DNN = Compute_EnergyDepletions(Input.Tasks.Plot_EnergyDepletions,DNN,RatesDNN);
		 
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
      end
    
    
    %%%% Writing Quantities %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%  
    
    %% Writing Rate Coefficients for Paraview
%     if (Input.Tasks.Write_RatesParaview.Flg)
%         Write_RatesForParaview(Input.Tasks.Write_RatesParaview)
%     end
    
    %% Writing Rate Coefficients for Paraview
    if (Input.Tasks.Write_RatesAsNetwork.Flg)
        Write_RatesAsNetwork(Input.Tasks.Write_RatesAsNetwork)
    end
        
    %% Writing Rate Coefficients for Clustering
    if (Input.Tasks.Write_RatesForClustering.Flg)
        Write_RatesForClustering(Input.Tasks.Write_RatesForClustering)
    end
    
    
    %%%% Plotting Quantities %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%   
    
    %% Plotting Diatomic Potential
    if (Input.Tasks.Plot_DiatPot.Flg)
        Plot_DiatPot(Input.Tasks.Plot_DiatPot)
    end
    
    %% Plotting Overall Rate Coefficients (Dissociation and Exchange)
    if (Input.Tasks.Plot_OverallRates.Flg)
        Plot_OverallRates()    
    end
    
    %% Plotting Pair Contributions to Dissociation Rate Coefficients
    if (Input.Tasks.Plot_DifferentDissRates.Flg)
        Plot_DifferentDissRates()
    end
    
    %% Plotting Reconstructed Rate Coefficients
    if (Input.Tasks.Plot_ReconstructedRates.Flg)
        Plot_ReconstructedRates()
    end
    
    
    %% Plotting Mole Fractions
    if (Input.Tasks.Plot_MoleFracs.Flg)
        Plot_MoleFracs(Input.Tasks.Plot_MoleFracs,QCT)
        Plot_MoleFracs(Input.Tasks.Plot_MoleFracs,DNN)
        Input.iFig = Input.iFig + 1;
    end
    
    %% Plotting Global Rates (Dissociation and Exchange)
    if (Input.Tasks.Plot_GlobalRates.Flg)
        Plot_GlobalRates(Input.Tasks.Plot_GlobalRates, QCT, RatesQCT)    
        Plot_GlobalRates(Input.Tasks.Plot_GlobalRates, DNN, RatesDNN) 
    end
    
    %% Plotting Global Rates (Dissociation and Exchange) on top of Mole Fractions
    if (Input.Tasks.Plot_MoleFracs_and_GlobalRates.Flg)
        Plot_MoleFracs_and_GlobalRates(Input.Tasks.Plot_MoleFracs_and_GlobalRates, QCT, RatesQCT)
        Plot_MoleFracs_and_GlobalRates(Input.Tasks.Plot_MoleFracs_and_GlobalRates, DNN, RatesDNN)
    end
    
    %% Plotting Vib. Distr. Function
    if (Input.Tasks.Plot_VDF.Flg)
       Plot_VDF(Input.Tasks.Plot_VDF) 
    end
        
    %% Plotting RVS Populations
%     if (Input.Tasks.Plot_Populations.Flg)
%        Plot_Populations(Input.Tasks.Plot_Populations, QCT, RatesQCT) 
%        Plot_Populations(Input.Tasks.Plot_Populations, DNN, RatesDNN) 
%     end
    
    %% Plotting RVS Populations
    if (Input.Tasks.Plot_PopulationsVqnSpecific.Flg)
       Plot_PopulationsVqnSpecific(Input.Tasks.Plot_PopulationsVqnSpecific) 
    end
            
    %% Plotting Energies
    if (Input.Tasks.Plot_Energies.Flg)
        Plot_Energies(Input.Tasks.Plot_Energies,QCT,DNN)
    end
    
    %% Plotting Energy Depletions
    if (Input.Tasks.Plot_EnergyDepletions.Flg)
        Plot_EnergyDepletions(Input.Tasks.Plot_EnergyDepletions)
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    if (Input.Tasks.ErrorMolFracs)
        Error = ErrorMolFracs(Input.Tasks.Plot_MoleFracs,QCT,DNN);
    end

    if (Input.Tasks.ErrorPopulationsTraining)
        ErrorPopulationsTraining(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end
    
    if (Input.Tasks.ErrorPopulations)
        ErrorPopulations(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end
    
    if (Input.Tasks.ErrorPopulationsOverg)
        ErrorPopulationsOverg(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end
    
    if (Input.Tasks.ErrorPopulations_PercEnergy)
        ErrorPopulations_PercEnergy(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end 
    
    if (Input.Tasks.StateEnergy)
        StateEnergyPopulations(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end
    
    if (Input.Tasks.StateKDiss)
        StateContribution_KDiss(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end
    
    if (Input.Tasks.EnergyContribution)
        EnergyContribution(Input.Tasks.Plot_Populations,QCT,DNN,RatesQCT,RatesDNN);
    end
    
    if (Input.Tasks.ErrorRates)
        %ErrorRates_L2Norm(Input.Tasks.Write_RatesParaview,RatesQCT,RatesDNN);
        ErrorRates_NNLoss(Input.Tasks.Write_RatesParaview,RatesQCT,RatesDNN);
    end
    
    %pause
    clear Kin Rates %RatesQCT RatesDNN DNN QCT
end

