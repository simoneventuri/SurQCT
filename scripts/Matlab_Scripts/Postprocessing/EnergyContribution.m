function EnergyContribution(Controls, KinQCT, KinDNN, RatesQCT, RatesDNN)
  
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

    fprintf('= Plot Energy Contribution ===================== T = %i K\n', Temp.TNow)
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
  
    for tStep = Controls.tSteps
            iStep = 1;
            while KinQCT.T(Temp.iT).t(iStep) < tStep
                iStep = iStep + 1;
            end     
            fprintf(['Plotting Time Step Nb ' num2str(iStep) ', t = ' num2str(KinQCT.T(Temp.iT).t(iStep)) ' s (' num2str(tStep) ' s)\n'] );

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

            eVibQCT = vEeVVib0'    .* KinQCT.vPop ./ PopTotQCT_g;
            eVibDNN = vEeVVib0'    .* KinDNN.vPop ./ PopTotDNN_g;
            
            % StS Energy contribution
            LevelPopQCT(:) = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStep,:).*Syst.Molecule(iMol).LevelEeV0'; 
            LevelPopDNN(:) = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStep,:).*Syst.Molecule(iMol).LevelEeV0'; 
            
            % Error in energy level contribution 
            ErrorLevelPop(:) = abs(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:)-KinDNN.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:))./KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:);            
            ErrorLevelPopLog(:) = abs(log(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:))-log(KinDNN.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:)))./log(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:));            

            figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );
            scatter(Syst.Molecule(iMol).Levelvqn, LevelPopQCT, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
            hold on
            scatter(Syst.Molecule(iMol).Levelvqn, LevelPopDNN, 100, '.', 'MarkerEdgeColor','r', 'MarkerFaceColor', 'b', 'LineWidth', 1.5)
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
            str_y = ['$N_{i} \epsilon_{i}$ $[m^{-3} eV]$'];
            ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            ylab.Interpreter = 'latex';
            set(gca, 'YScale', 'log')
            
            pbaspect([1 1 1])
            
            Input.iFig = Input.iFig + 1; 
    
            figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );
            title(num2str(KinQCT.T(Temp.iT).t(iStep)))
             
            scatter(vqn, eVibQCT, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
            hold on
            scatter(vqn, eVibDNN, 100, '.', 'MarkerEdgeColor','r', 'MarkerFaceColor', 'b', 'LineWidth', 1.5)
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
            str_y = ['$N_{i} \epsilon_{i}$ $[m^{-3} eV]$'];
            ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            ylab.Interpreter = 'latex';
            set(gca, 'YScale', 'log')
            
            pbaspect([1 1 1])
            
            Input.iFig = Input.iFig + 1; 
            
%             figure(Input.iFig)
%             fig = gcf;
%             screensize   = get( groot, 'Screensize' );
% 
%             scatter(LevelEeV, ErrorLevelPop, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
%             hold on
%             box on
%                     
%             xt = get(gca, 'XTick');
%             set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
%             yt = get(gca, 'YTick');
%             set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
% 
%             str_x = ['$\epsilon_i$ [eV]'];
%             xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             xlab.Interpreter = 'latex';
%             %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);
% 
%             str_y = ['Error $N_{i} \epsilon_{i}$ $[m^{-3} eV]$'];
%             ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             ylab.Interpreter = 'latex';
%             set(gca, 'YScale', 'log')
%                         
%             pbaspect([1 1 1])
% 
%             Input.iFig = Input.iFig + 1;
                        
    end
    
        

    fprintf('====================================================\n\n')

end