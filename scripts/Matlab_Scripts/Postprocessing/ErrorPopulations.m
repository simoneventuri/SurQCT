function ErrorPopulations(Controls, KinQCT, KinDNN, RatesQCT, RatesDNN)
  
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
    
    for tStep = Controls.tSteps
            iStep = 1;
            while KinQCT.T(Temp.iT).t(iStep) < tStep
                iStep = iStep + 1;
            end     
            fprintf(['Plotting Time Step Nb ' num2str(iStep) ', t = ' num2str(KinQCT.T(Temp.iT).t(iStep)) ' s (' num2str(tStep) ' s)\n'] );

            KinQCT.vPop = zeros(Nvqn,1);
            LevelPopQCT_g(:,1) = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStep,:);            
            PopTotQCT_g = sum(LevelPopQCT_g)
            
            KinDNN.vPop = zeros(Nvqn,1);
            LevelPopDNN_g(:,1) = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStep,:);            
            PopTotDNN_g = sum(LevelPopDNN_g)
            
            KinQCT.vPop = KinQCT.vPop.*0.0;
            KinDNN.vPop = KinDNN.vPop.*0.0;
            for iLevels = 1:NLevels
                KinQCT.vPop(Levelvqn(iLevels)+1) = KinQCT.vPop(Levelvqn(iLevels)+1) + LevelPopQCT_g(iLevels);
                KinDNN.vPop(Levelvqn(iLevels)+1) = KinDNN.vPop(Levelvqn(iLevels)+1) + LevelPopDNN_g(iLevels);
            end

            eVibQCT = sum( vEeVVib0'    .* KinQCT.vPop )     ./ PopTotQCT_g
            eVibDNN = sum( vEeVVib0'    .* KinDNN.vPop )     ./ PopTotDNN_g
            
            LevelPopQCT(:) = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStep,:);
            LevelPopDNN(:) = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStep,:); 
            ErrorLevelPop(:) = abs(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:)-KinDNN.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:))./KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:);            
            ErrorLevelPopLog(:) = abs(log(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:))-log(KinDNN.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:)))./log(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStep,:));            

            figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );
            
            scatter(LevelEeV, LevelPopQCT, 300, '.', 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'LineWidth', 1.5)
            hold on
            scatter(LevelEeV, LevelPopDNN, 200, '.', 'MarkerEdgeColor','r', 'MarkerFaceColor', 'r', 'LineWidth', 1.5)
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

            str_y = ['$N_{i}$ $[m^{-3}]$'];
            ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            ylab.Interpreter = 'latex';
            set(gca, 'YScale', 'log')
            
            title(num2str(KinQCT.T(Temp.iT).t(iStep)))

            pbaspect([1 1 1])
            
            Input.iFig = Input.iFig + 1; 
            
                        figure(Input.iFig)
            fig = gcf;
            screensize   = get( groot, 'Screensize' );
            
            scatter(vEeVVib0, KinQCT.vPop, 300, '.', 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'LineWidth', 1.5)
            hold on
            scatter(vEeVVib0, KinDNN.vPop, 200, '.', 'MarkerEdgeColor','r', 'MarkerFaceColor', 'r', 'LineWidth', 1.5)
            hold on
            box on

            legend('QCT','SurQCT')
            legend boxoff
            xt = get(gca, 'XTick');
            set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
            yt = get(gca, 'YTick');
            set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');

            str_x = ['$\epsilon_v$ [eV]'];
            xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            xlab.Interpreter = 'latex';
            %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);

            str_y = ['$N_{v}$ $[m^{-3}]$'];
            ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
            ylab.Interpreter = 'latex';
            set(gca, 'YScale', 'log')
            
            title(num2str(KinQCT.T(Temp.iT).t(iStep)))

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
%             str_y = ['Error $N_{i} / g_{i}$ $[m^{-3}]$'];
%             ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             ylab.Interpreter = 'latex';
%             set(gca, 'YScale', 'log')
%                         
%             pbaspect([1 1 1])
% 
%             Input.iFig = Input.iFig + 1;
%             
%             figure(Input.iFig)
%             fig = gcf;
%             screensize   = get( groot, 'Screensize' );
% 
%             scatter(LevelPopQCT,LevelPopDNN, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
%             hold on
%             box on
%                     
%             xt = get(gca, 'XTick');
%             set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
%             yt = get(gca, 'YTick');
%             set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
% 
%             str_x = ['QCT $N_{i} / g_{i}$ $[m^{-3}]$'];
%             xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             xlab.Interpreter = 'latex';
%             %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);
% 
%             str_y = ['DeepONet $N_{i} / g_{i}$ $[m^{-3}]$'];
%             ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             ylab.Interpreter = 'latex';
%             set(gca,'Xscale', 'log', 'YScale', 'log')
%                         
%             pbaspect([1 1 1])
% 
%             Input.iFig = Input.iFig + 1;
                        
%             fprintf('    Writing Error Population on Diatomic Potential Properties\n')
%             FileName1 = strcat(Input.Paths.SaveDataFldr, '/Test', Input.DNN.TestNum ,'_T', Temp.TNowChar, 'K_Error_Pop',num2str(KinQCT.T(Temp.iT).t(iStep)),'_withLevels.csv');
%             fileID1   = fopen(FileName1,'w');
%             fprintf(fileID1,'#Idx,EeV,g,rIn,v,J,ECB,Error,ErrorLog\n');
% 
%             for iLevel = 1:size(LevelEeV,1)
%                 fprintf(fileID1,'%i,%e,%e,%e,%i,%i,%e,%e,%e\n',   iLevel,                                      ...
%                                                                Syst.Molecule(iMol).LevelEeV(iLevel),        ...
%                                                                Syst.Molecule(iMol).Levelg(iLevel),          ...
%                                                                Syst.Molecule(iMol).LevelrIn(iLevel),        ...
%                                                                Syst.Molecule(iMol).Levelvqn(iLevel),        ...
%                                                                Syst.Molecule(iMol).Leveljqn(iLevel),        ...
%                                                                Syst.Molecule(iMol).LevelECB(iLevel),        ...
%                                                                ErrorLevelPop(iLevel),                      ...
%                                                                ErrorLevelPopLog(iLevel));            
%             end
%             fclose(fileID1);
            
    end
    
        
    if (Input.Kin.Proc.DissFlg > 0)
            
        iStepQCT = KinQCT.T(Temp.iT).QSS.i;   
        iStepDNN = KinDNN.T(Temp.iT).QSS.i;   
        
%         fprintf(['Plotting QSS: Time Step Nb ' num2str(iStep) ', t = ' num2str(Kin.T(Temp.iT).t(iStep)) ' s\n'] );

        LevelPopQCT = KinQCT.T(Temp.iT).Molecule(iMol).Pop(iStepQCT,:);
        LevelPopDNN = KinDNN.T(Temp.iT).Molecule(iMol).Pop(iStepDNN,:);
        
        ErrorLevelPop(:) = abs(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStepQCT,:)-KinDNN.T(Temp.iT).Molecule(iMol).PopOverg(iStepDNN,:))./KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStepQCT,:);             
        ErrorLevelPopLog(:) = abs(log(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStepQCT,:))-log(KinDNN.T(Temp.iT).Molecule(iMol).PopOverg(iStepDNN,:)))./log(KinQCT.T(Temp.iT).Molecule(iMol).PopOverg(iStepQCT,:));             

        figure(Input.iFig)
        fig = gcf;
        screensize   = get( groot, 'Screensize' );
            
        scatter(LevelEeV, LevelPopQCT, 300, '.', 'MarkerEdgeColor','k', 'MarkerFaceColor', 'k', 'LineWidth', 1.5)
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

            pbaspect([1 1 1])
            
            title('QSS')
            
        Input.iFig = Input.iFig + 1;    
        
%         figure(Input.iFig)
%         fig = gcf;
%         screensize   = get( groot, 'Screensize' );
%             
%         scatter(LevelEeV, ErrorLevelPop, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
%         hold on
%         box on
%         
%         xt = get(gca, 'XTick');
%         set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
%         yt = get(gca, 'YTick');
%         set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
% 
%             str_x = ['$\epsilon_i$ [eV]'];
%             xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             xlab.Interpreter = 'latex';
%             %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);
% 
%             str_y = ['Error $N_{i} / g_{i}$ $[m^{-3}]$'];
%             ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             ylab.Interpreter = 'latex';
%             set(gca, 'YScale', 'log')
% 
%             pbaspect([1 1 1])
%             
%         Input.iFig = Input.iFig + 1;    
%         
%             
%         figure(Input.iFig)
%             fig = gcf;
%             screensize   = get( groot, 'Screensize' );
% 
%             scatter(LevelPopQCT,LevelPopDNN, 300, '.', 'MarkerEdgeColor', Syst.CFDComp(iComp).Color, 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'LineWidth', 1.5)
%             hold on
%             box on
%                     
%             xt = get(gca, 'XTick');
%             set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
%             yt = get(gca, 'YTick');
%             set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
% 
%             str_x = ['QCT $N_{i} / g_{i}$ $[m^{-3}]$'];
%             xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             xlab.Interpreter = 'latex';
%             %xlim([max(min(LevelEeV)), MinEvPlot, min(max(LevelEeV)), MaxEvPlot]);
% 
%             str_y = ['DeepONet $N_{i} / g_{i}$ $[m^{-3}]$'];
%             ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
%             ylab.Interpreter = 'latex';
%             set(gca,'Xscale', 'log', 'YScale', 'log')
%                         
%             pbaspect([1 1 1])
% 
%             Input.iFig = Input.iFig + 1;
%     
%             
%             fprintf('    Writing Error Population on Diatomic Potential Properties\n')
%             FileName1 = strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K_Error_QSSPop_withLevels.csv');
%             fileID1   = fopen(FileName1,'w');
%             fprintf(fileID1,'#Idx,EeV,g,rIn,v,J,ECB,Error,ErrorLog\n');
% 
%             for iLevel = 1:size(LevelEeV,1)
%                 fprintf(fileID1,'%i,%e,%e,%e,%i,%i,%e,%e,%e\n',   iLevel,                                      ...
%                                                                Syst.Molecule(iMol).LevelEeV(iLevel),        ...
%                                                                Syst.Molecule(iMol).Levelg(iLevel),          ...
%                                                                Syst.Molecule(iMol).LevelrIn(iLevel),        ...
%                                                                Syst.Molecule(iMol).Levelvqn(iLevel),        ...
%                                                                Syst.Molecule(iMol).Leveljqn(iLevel),        ...
%                                                                Syst.Molecule(iMol).LevelECB(iLevel),        ...
%                                                                ErrorLevelPop(iLevel),                      ...
%                                                                ErrorLevelPopLog(iLevel));            
%             end
%             fclose(fileID1);
    
    end
        
    end


    fprintf('====================================================\n\n')

end