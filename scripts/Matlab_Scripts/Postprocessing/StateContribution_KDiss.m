function StateContribution_KDiss(Controls, KinQCT, KinDNN, RatesQCT, RatesDNN)
  
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
        LevelEeV0   = Syst.Molecule(iMol).LevelEeV0;
        iComp      = Syst.MolToCFDComp(iMol);
        
    for tStep = Controls.tSteps
            iStep = 1;
            while KinQCT.T(Temp.iT).t(iStep) < tStep
                iStep = iStep + 1;
            end     
            fprintf(['Plotting Time Step Nb ' num2str(iStep) ', t = ' num2str(KinQCT.T(Temp.iT).t(iStep)) ' s (' num2str(tStep) ' s)\n'] );

            LevelPopQCT(:) = KinQCT.T(Temp.iT).Molecule(iMol).DF(iStep,:)'.* RatesQCT.T(Temp.iT).Diss(:,1) ; 
            LevelPopDNN(:) = KinDNN.T(Temp.iT).Molecule(iMol).DF(iStep,:)'.* RatesDNN.T(Temp.iT).Diss(:,1) ; 
                     
            % Plotting state energy population of QCT and DNN on top of
            % each other
            figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );
            
            scatter(LevelEeV, LevelPopQCT, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
            hold on
            scatter(LevelEeV, LevelPopDNN, 150, '.', 'MarkerEdgeColor','r', 'MarkerFaceColor', 'r', 'LineWidth', 1.5)
            hold on
            box on

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
            title(num2str(KinQCT.T(Temp.iT).t(iStep)))

            pbaspect([1 1 1])
            
            Input.iFig = Input.iFig + 1; 
        
            % Plotting error in the state energies 
 
    end
        
    if (Input.Kin.Proc.DissFlg > 0)
            
        iStepQCT = KinQCT.T(Temp.iT).QSS.i;   
        iStepDNN = KinDNN.T(Temp.iT).QSS.i;   
        
%         fprintf(['Plotting QSS: Time Step Nb ' num2str(iStep) ', t = ' num2str(Kin.T(Temp.iT).t(iStep)) ' s\n'] );

        LevelPopQCT = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStepQCT,:)'.* RatesQCT.T(Temp.iT).Diss(:,1);
        LevelPopDNN = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStepDNN,:)'.* RatesDNN.T(Temp.iT).Diss(:,1);
        
      
        figure(Input.iFig)
        fig = gcf;
        screensize   = get( groot, 'Screensize' );
            
        scatter(LevelEeV, LevelPopQCT, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
        hold on
        scatter(LevelEeV, LevelPopDNN, 100, '.', 'MarkerEdgeColor','b', 'MarkerFaceColor', 'b', 'LineWidth', 1.5)
        hold on
        box on
        
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
            title('KQSS State contribution')
            pbaspect([1 1 1])
            
        Input.iFig = Input.iFig + 1;    
    
    end
        
    end


    fprintf('====================================================\n\n')

    
end
