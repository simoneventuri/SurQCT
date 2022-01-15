close all
clc
clear all

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1250 1250]) 
prev = st_set_graphics_defaults();

Input.Inel.TestNum = '9';
Input.Exch.TestNum = '6';
Input.FNN.TestNum = '55';

Syst.NameLong = 'N3_NASA';
Molecule='N2';

opts = delimitedTextImportOptions("NumVariables", 5);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["TK", "KDEq", "K_1EEq", "KDQSS", "K_1EQSS"];
opts.VariableTypes = ["double", "double", "double", "double", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
filename = strcat("/home/venturi/WORKSPACE/SurQCT/0D/Data/",Syst.NameLong,"/nondim_RunI",Input.Inel.TestNum,"_E",Input.Exch.TestNum,"_D",Input.FNN.TestNum,"/QCT_KGlobal_1_1_1_0_",Molecule,".csv");
tbl = readtable(filename, opts);
T_QCT        = tbl.TK;
KDEq_QCT     = tbl.KDEq;
K_O2EEq_QCT  = tbl.K_1EEq;
KDQSS_QCT    = tbl.KDQSS;
K_O2EQSS_QCT = tbl.K_1EQSS;
clear opts tbl

opts = delimitedTextImportOptions("NumVariables", 5);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["TK", "KDEq", "K_1EEq", "KDQSS", "K_1EQSS"];
opts.VariableTypes = ["double", "double", "double", "double", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
filename = strcat("/home/venturi/WORKSPACE/SurQCT/0D/Data/",Syst.NameLong,"/nondim_RunI",Input.Inel.TestNum,"_E",Input.Exch.TestNum,"_D",Input.FNN.TestNum,"/DNN_KGlobal_1_1_1_0_",Molecule,".csv");
tbl = readtable(filename, opts);
T_DNN        = tbl.TK;
KDEq_DNN     = tbl.KDEq;
K_O2EEq_DNN  = tbl.K_1EEq;
KDQSS_DNN    = tbl.KDQSS;
K_O2EQSS_DNN = tbl.K_1EQSS;
clear opts tbl


figure
semilogy(10000./T_QCT, KDQSS_QCT, 'o--k','LineWidth',3,'MarkerSize',15,'MarkerFaceColor','k');
hold on
semilogy(10000./T_DNN, KDQSS_DNN, '^--r','LineWidth',3,'MarkerSize',15,'MarkerFaceColor','r');
box on
set(gca,'YScale','log','tickdir','out')
xlabel('10000/T [K]')
ylabel('$k^D_{QSS}$ [cm$^3$/s]')
legend('QCT','SurQCT')
legend boxoff

figure
semilogy(10000./T_QCT, KDEq_QCT, 'o--k','LineWidth',3,'MarkerSize',15,'MarkerFaceColor','k');
hold on
semilogy(10000./T_DNN, KDEq_DNN, '^--r','LineWidth',3,'MarkerSize',15,'MarkerFaceColor','r');
box on
set(gca,'YScale','log','tickdir','out')
xlabel('10000/T [K]')
ylabel('$k^D_{Eq}$ [cm$^3$/s]')
legend('QCT','SurQCT')
legend boxoff