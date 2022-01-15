function ErrorPopulations_PercEnergy(Controls, KinQCT, KinDNN, RatesQCT, RatesDNN)
  
    %%==============================================================================================================
    % 
    % Coarse-Grained method for Quasi-Classical Trajectories (CG-QCT) 
    % 
    % Copyright (C) 2018 Simone Venturi and Bruno Lopez (University of Illinois at Urbana-Champaign). 
    %
    % Based on "VVTC" (Vectorized Variable stepsize Trajectory Code) by David Schwenke (NASA Ames Research Center). 
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

    global Input Param Syst Temp

    fprintf('= Plot_Populations ===================== T = %i K\n', Temp.TNow)
    fprintf('====================================================\n')
    
    for iMol = Controls.MoleculesOI
        fprintf(['Molecule Nb ' num2str(iMol) ', ' Syst.Molecule(iMol).Name '\n'] );
           
    
    clear LevelToBin Levelvqn LevelEeV LevelPop
    if strcmp(Syst.Molecule(iMol).KinMthdIn, 'StS')
        LevelToBin = Syst.Molecule(iMol).LevelToGroupIn;
    else
        LevelToBin = Syst.Molecule(iMol).LevelToGroupOut;
    end
        Levelvqn   = Syst.Molecule(iMol).Levelvqn;
        LevelEeV   = Syst.Molecule(iMol).LevelEeV;
        iComp      = Syst.MolToCFDComp(iMol);

    vEeVVib0    = Syst.Molecule(iMol).vEeVVib0 ; %+ 0.1456.* ones(1,length(Syst.Molecule(iMol).vEeVVib0));    
    Nvqn        = Syst.Molecule(iMol).Nvqn;
    NLevels     = Syst.Molecule(iMol).NLevels;
    vqn = [1:1:Nvqn];
        
    for tStep = Controls.PercEnergy
            iStep = 1;
            iStepDNN = 1;
            energy_ref = tStep*KinQCT.T(Temp.iT).Molecule(iMol).eVib(end);
            while KinQCT.T(Temp.iT).Molecule(iMol).eVib(iStep) < energy_ref
                iStep = iStep + 1;
            end  
            energy_refDNN = tStep*KinDNN.T(Temp.iT).Molecule(iMol).eVib(end);
            while KinDNN.T(Temp.iT).Molecule(iMol).eVib(iStepDNN) < energy_refDNN
                iStepDNN = iStepDNN + 1;
            end  
            fprintf(['Plotting Time Step Nb ' num2str(iStep) ', t = ' num2str(KinQCT.T(Temp.iT).t(iStep)) ' s (' num2str(tStep) ' s), DNN '  num2str(iStepDNN) ', t = ' num2str(KinDNN.T(Temp.iT).t(iStepDNN)) ' s (' num2str(tStep) ' s)\n'] );

            KinQCT.vPop = zeros(Nvqn,1);
            LevelPopQCT_g(:,1) = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStep,:);            
            PopTotQCT_g = sum(LevelPopQCT_g);
            
            KinDNN.vPop = zeros(Nvqn,1);
            LevelPopDNN_g(:,1) = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStep,:);            
            PopTotDNN_g = sum(LevelPopDNN_g);
            
            KinQCT.vPop = KinQCT.vPop.*0.0;
            KinDNN.vPop = KinDNN.vPop.*0.0;
            for iLevels = 1:NLevels
                KinQCT.vPop(Levelvqn(iLevels)+1) = KinQCT.vPop(Levelvqn(iLevels)+1) + LevelPopQCT_g(iLevels);
                KinDNN.vPop(Levelvqn(iLevels)+1) = KinDNN.vPop(Levelvqn(iLevels)+1) + LevelPopDNN_g(iLevels);
            end
            
            LevelPopQCT(:) = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStep,:); 
            LevelPopDNN(:) = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStepDNN,:); 

            figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );
            
            scatter(LevelEeV, LevelPopQCT, 300, '.', 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'LineWidth', 1.5)
            hold on
            scatter(LevelEeV, LevelPopDNN, 100, '.', 'MarkerEdgeColor','b', 'MarkerFaceColor', 'b', 'LineWidth', 1.5)
            hold on
            box on

            legend('QCT','SurQCT')
            legend boxoff
            xt = get(gca, 'XTick');
            set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
            yt = get(gca, 'YTick');
            set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');

            str_x = ['$\epsilon_i$ [eV]'];
            xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            xlab.Interpreter = 'latex';
            %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);

            str_y = ['$N_{i} / g_{i}$ $[m^{-3}]$'];
            ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            ylab.Interpreter = 'latex';
            set(gca, 'YScale', 'log')
            
            title(strcat(num2str(tStep*100),' % of Final Vibrational energy'))

            pbaspect([1 1 1])
            
            Input.iFig = Input.iFig + 1; 
            
            figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );            
            scatter(vEeVVib0, KinQCT.vPop, 300, '.', 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'LineWidth', 1.5)
            hold on
            scatter(vEeVVib0, KinQCT.vPop, 200, '.', 'MarkerEdgeColor','r', 'MarkerFaceColor', 'r', 'LineWidth', 1.5)
            hold on
            box on

            legend('QCT','SurQCT')
            legend boxoff
            xt = get(gca, 'XTick');
            set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
            yt = get(gca, 'YTick');
            set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');

            str_x = ['$\epsilon_i$ [eV]'];
            xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            xlab.Interpreter = 'latex';
            %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);

            str_y = ['$N_{i} / g_{i}$ $[m^{-3}]$'];
            ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            ylab.Interpreter = 'latex';
            set(gca, 'YScale', 'log')
            
            title(strcat(num2str(tStep*100),' % of Final Vibrational energy'))

            pbaspect([1 1 1])
            
            Input.iFig = Input.iFig + 1; 
    end

    fprintf('====================================================\n\n')

end