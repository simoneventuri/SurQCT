clear all
%close all
clc
%%
set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1250 1250]) 
prev = st_set_graphics_defaults();

global Input Syst Param

iCompOI       = 2;
Nvqn          = 45;
Syst.NameLong = 'N2O_UMN';
Molecule='N2';
dimension='nondim'
Input.Inel.TestNum = '9';
Input.Exch.TestNum = '6';
Input.FNN.TestNum = '55';

StSFldr1      = strcat('/home/venturi/WORKSPACE/SurQCT/0D/Data/',Syst.NameLong,'/',dimension,'_RunI',Input.Inel.TestNum,'_E',Input.Exch.TestNum,'_D',Input.FNN.TestNum,'/');
StSFldr2      = strcat('_Taus_',Molecule,'_0_1_0_0.csv');

SuffixFldr = [{'QCT'},{'DNN'}]

Input.SaveFigsFlgInt     = 0
Input.Paths.SaveFigsFldr = '/home/venturi/WORKSPACE/SurQCT/AviationPaper/Figures/'
Syst                     = Initialize_ChemicalSyst(Syst)
Input.FigureFormat       = 'PrePrint';
Input.iFig               = 1;
Input.SystNameLong       = Syst.NameLong;
Initialize_Parameters()

    
iS = 1;
for iSuffix = SuffixFldr

    filename = strcat(StSFldr1, char(iSuffix), StSFldr2)
    opts = delimitedTextImportOptions("NumVariables", 5);
    opts.DataLines = [2, Inf];
    opts.Delimiter = ",";
    opts.VariableNames = ["TK", "Patm", "tau_Int", "tau_Rot", "tau_Vib"];
    opts.VariableTypes = ["double", "double", "double", "double", "double"];
    opts.ExtraColumnsRule = "ignore";
    opts.EmptyLineRule = "read";
    tbl = readtable(filename, opts);
    Sim(iS).TVec         = tbl.TK;
    Sim(iS).PVec         = tbl.Patm;
    Sim(iS).EType(1).tau = tbl.tau_Int;
    Sim(iS).EType(2).tau = tbl.tau_Rot;
    Sim(iS).EType(3).tau = tbl.tau_Vib;
    clear opts tbl

    iS = iS + 1;
end

% Breen = [2000, 2.8789058871588226e-8;
% 2000, 2.6080085622394214e-8;
% 2097.412480974125, 2.401355917632704e-8;
% 2207.001522070015, 2.784429517090738e-8;
% 2438.3561643835615, 2.6056559047704765e-8;
% 2608.82800608828, 2.6919735623920724e-8;
% 2669.7108066971077, 2.8749391453493867e-8;
% 2730.593607305936, 2.7359930598276185e-8;
% 2949.7716894977166, 2.207643947854396e-8;
% 2901.065449010654, 2.0333268795966006e-8;
% 2657.5342465753424, 1.9046388919713564e-8;
% 2499.23896499239, 1.936900277146543e-8;
% 2365.296803652968, 1.937434476030935e-8;
% 2231.3546423135467, 2.0028708118289736e-8;
% 2024.3531202435313, 2.0370003356982645e-8;
% 2000, 1.7564475801582797e-8;
% 2231.3546423135467, 1.5904128500535385e-8;
% 3254.185692541857, 1.9660081471640116e-8;
% 3400.3044140030443, 2.169567259422632e-8;
% 3327.24505327245, 2.8241493276648928e-8]
% 
% Ibraguimova = [4003.2102728731943, 5.1311160315222835e-8;
% 4545.746388443018, 4.7903914350976396e-8;
% 5067.4157303370785, 4.472292179806491e-8;
% 5609.951845906901, 4.411253358926568e-8;
% 6110.7544141252, 4.351047609211189e-8;
% 6653.290529695025, 4.2330899987043385e-8;
% 7195.826645264846, 4.1183302382616954e-8;
% 7738.362760834671, 4.1183302382616954e-8;
% 8280.898876404493, 4.1183302382616954e-8;
% 8844.30176565008, 4.1183302382616954e-8;
% 9345.10433386838, 4.006681633646312e-8;
% 9908.507223113964, 4.006681633646312e-8;
% 10430.176565008025, 4.1183302382616954e-8]
% 
% Grover = [3001.6051364365967, 1.960831014766194e-8;
% 4983.9486356340285, 2.071633066139631e-8;
% 6006.420545746389, 2.158824481470722e-8;
% 7967.897271268057, 2.2189814300392475e-8;
% 9991.974317817014, 2.2808146883273158e-8;
% 11974.317817014446, 2.2808146883273158e-8;
% 15000, 2.3e-8];
%
%figure
%semilogy(Breen(:,1).^(-1/3),Breen(:,2),'ko')
%hold on
%semilogy(Ibraguimova(:,1).^(-1/3),Ibraguimova(:,2),'b')
%semilogy(Grover(:,1).^(-1/3),Grover(:,2),'r')


iPOIStr = [{'I'},{'R'},{'V'}];

    
    figure(Input.iFig)
    fig = gcf;
    screensize   = get( groot, 'Screensize' );
    %fig.Position = screensize;
    %fig.Color='None';

%     iS=1; iP=1;
%     h0 = semilogy(Sim(iS).TVec, Sim(iS).EType(iP).tau, '-',  'LineWidth',   2, 'Color', Param.KCVec);
%     hold on
%     semilogy(Sim(iS).TVec,      Sim(iS).EType(iP).tau, '.',  'MarkerSize', 20, 'Color', Param.KCVec, 'markerfacecolor', Param.KCVec)
%     
%     iS=2; iP=1;
%     h1 = semilogy(Sim(iS).TVec, Sim(iS).EType(iP).tau, '-',  'LineWidth',   2, 'Color', Param.PCVec);
%     hold on
%     semilogy(Sim(iS).TVec,      Sim(iS).EType(iP).tau, 'p',  'MarkerSize', 10, 'Color', Param.PCVec, 'markerfacecolor', Param.PCVec)
% 
    iS=1;iP=2;
    %h2 = semilogy(Sim(iS).TVec, Sim(iS).EType(iP).tau, ':',  'LineWidth',   3, 'Color', Param.RCVec);
    h2 = semilogy(Sim(iS).TVec,      Sim(iS).EType(iP).tau, 'h',  'MarkerSize', 20, 'Color', Param.RCVec, 'markerfacecolor', Param.RCVec)

    iS=2;iP=2;
    %h3 = semilogy(Sim(iS).TVec, Sim(iS).EType(iP).tau, '-.', 'LineWidth',   3, 'Color', Param.BCVec);
    h3 =semilogy(Sim(iS).TVec,      Sim(iS).EType(iP).tau, '^',  'MarkerSize',  20, 'Color', Param.BCVec, 'markerfacecolor', Param.BCVec)

    iS=1;iP=3;
    %h4 = semilogy(Sim(iS).TVec, Sim(iS).EType(iP).tau, '-.', 'LineWidth',   3, 'Color', Param.GCVec);
    h4 = semilogy(Sim(iS).TVec,      Sim(iS).EType(iP).tau, 's',  'MarkerSize',  20, 'Color', Param.GCVec, 'markerfacecolor', Param.GCVec)

    iS=2;iP=3;
    %h5 = semilogy(Sim(iS).TVec, Sim(iS).EType(iP).tau, '-.', 'LineWidth',   3, 'Color', Param.YCVec);
    h5 = semilogy(Sim(iS).TVec,      Sim(iS).EType(iP).tau, 'o',  'MarkerSize', 20, 'Color', Param.YCVec, 'markerfacecolor', Param.YCVec)
    
%     h6 = semilogy(Breen(:,1),Breen(:,2),'ko','MarkerSize',20,'LineWidth',3,'markerfacecolor', 'k');
%     h7 = semilogy(Ibraguimova(:,1),Ibraguimova(:,2),'^b','MarkerSize',20,'LineWidth',3,'markerfacecolor', 'b')
%     semilogy(Ibraguimova(:,1),Ibraguimova(:,2),'-b','LineWidth',3)
%     h8 = semilogy(Grover(:,1),Grover(:,2),'sr','MarkerSize',20,'LineWidth',3,'markerfacecolor', 'r');
%     semilogy(Grover(:,1),Grover(:,2),'-r','LineWidth',3)

%    clab = legend([h0,h1,h2,h3,h4,h5,h7,h8], '$\tau_{int}$ QCT', '$\tau_{int}$ SurQCT', '$\tau_{rot}$ QCT', '$\tau_{rot}$ SurQCT', '$\tau_{vib}$ QCT', '$\tau_{vib}$ SurQCT','Ibraguimova et al.','Grover et al.');
        clab = legend([h2,h3,h4,h5], '$\tau_{rot}$ QCT', '$\tau_{rot}$ SurQCT', '$\tau_{vib}$ QCT', '$\tau_{vib}$ SurQCT');
    clab.Interpreter = 'latex';
    set(clab,'FontSize', Param.LegendFontSz, 'FontName', Param.LegendFontNm, 'Interpreter', 'latex');
    legend boxoff

    xt = get(gca, 'XTick');
    set(gca,'FontSize',30, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
    yt = get(gca, 'YTick');
    set(gca,'FontSize',30, 'FontName', Param.AxisFontNm, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');

    str_x = ['T [K]'];
    xlab             = xlabel(str_x, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
    xlab.Interpreter = 'latex';
    xlim([min(Sim(1).TVec-500), max(Sim(1).TVec+500)]);

    str_y = ['$\tau$ [atm*s]'];
    ylab             = ylabel(str_y, 'Fontsize', Param.AxisLabelSz, 'FontName', Param.AxisLabelNm);
    ylab.Interpreter = 'latex';
    ylim([1.d-9, 1.d-6]);
    set(gca, 'YScale', 'log')

    box on
    
    pbaspect([1 1 1])

    if Input.SaveFigsFlgInt > 0
        [status,msg,msgID]  = mkdir(Input.Paths.SaveFigsFldr);
        FolderPath = strcat(Input.Paths.SaveFigsFldr, '/', Syst.NameLong, '/');
        [status,msg,msgID] = mkdir(FolderPath);
        FileName = strcat(Syst.Molecule(1).Name,'_Tau_', char(iPOIStr(iP)) );
        if Input.SaveFigsFlgInt == 1
            FileName   = strcat(FolderPath, FileName);
            export_fig(FileName, '-pdf');
        elseif Input.SaveFigsFlgInt == 2
            FileName   = strcat(FolderPath, strcat(FileName,'.fig'));
            savefig(FileName);
        end
        close
    end
    Input.iFig = Input.iFig + 1;

