function Error = ErrorMolFracs(Controls,KinQCT, KinDNN)

    global Input Syst Temp Param
    Error.MolFracsRel = abs(KinQCT.T(Temp.iT).MolFracs - KinDNN.T(Temp.iT).MolFracs)./(KinQCT.T(Temp.iT).MolFracs);
    Error.MolFracs = abs(KinQCT.T(Temp.iT).MolFracs - KinDNN.T(Temp.iT).MolFracs);
    
    figure(Input.iFig)
    fig = gcf;
    screensize   = get( groot, 'Screensize' );
    
    for iComp = Controls.CompStart:Controls.CompEnd
%           semilogx(KinQCT.T(Temp.iT).t(:), KinQCT.T(Temp.iT).MolFracs(:,iComp), 'Color', Syst.CFDComp(iComp).Color, 'linestyle', Syst.CFDComp(iComp).LineStyle, 'LineWidth', Param.LineWidth)  
%           hold on
%           semilogx(KinDNN.T(Temp.iT).t(:), KinDNN.T(Temp.iT).MolFracs(:,iComp), 'Color', Syst.CFDComp(iComp).Color, 'linestyle', Syst.CFDComp(iComp).LineStyle, 'LineWidth', Param.LineWidth)  
%           hold on
          semilogx(KinQCT.T(Temp.iT).t(:), Error.MolFracsRel(:,iComp), 'Color', Syst.CFDComp(iComp).Color, 'linestyle', Syst.CFDComp(iComp).LineStyle, 'LineWidth', Param.LineWidth)
          hold on
    end
    hold on

        if (Input.Tasks.Plot_Populations.Flg)
            jStep = 1;
            for tStep = Input.Tasks.Plot_Populations.tSteps
                iStep = 1;
                while KinQCT.T(Temp.iT).t(iStep) < tStep
                    iStep = iStep + 1;
                end  
                Controls.iSteps(jStep) = iStep;
                jStep = jStep + 1;
            end
            Controls.iSteps(jStep) = KinQCT.T(Temp.iT).QSS.i;

            for iMol = Input.Tasks.Plot_Populations.MoleculesOI
                iComp = Syst.MolToCFDComp(iMol);
                semilogx(KinQCT.T(Temp.iT).t(Controls.iSteps), Error.MolFracsRel(Controls.iSteps,iComp), 'o', 'MarkerFaceColor', Syst.CFDComp(iComp).Color, 'MarkerEdgeColor', Syst.CFDComp(iComp).Color)
            end
        end

        xt = get(gca, 'XTick');
        set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
        yt = get(gca, 'YTick');
        set(gca,'FontSize', Param.AxisFontSz, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');

        clab             = legend(Syst.CFDComp(Controls.CompStart:Controls.CompEnd).Name, 'Location', 'Best');
        clab.Interpreter = 'latex';
        set(clab,'FontSize', Param.LegendFontSz, 'FontName', Param.LegendFontNm, 'Interpreter', 'latex');

        str_x = ['t [s]'];
        xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
        xlab.Interpreter = 'latex';
        %xlim(XLimPlot);

        str_y = ['Error Mole Fraction'];
        ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
        ylab.Interpreter = 'latex';
        %ylim(YLimPlot);

        pbaspect([1 1 1])
        
    Input.iFig = Input.iFig + 1;

    
    fprintf('====================================================\n\n')

end
