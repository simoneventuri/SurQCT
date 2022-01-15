close all
clc
clear all

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1300 1300]) 
prev = st_set_graphics_defaults();

DataFldr = '/home/venturi/WORKSPACE/SurQCT/AviationPaper/Data/'
opts = delimitedTextImportOptions("NumVariables", 7);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["T", "C_IntEq", "C_RotEq", "C_VibEq", "C_IntQSS", "C_RotQSS", "C_VibQSS"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
tbl = readtable(strcat(DataFldr,'/QCT/EDCoeffs_O2_2_1_1_0.csv'), opts);
T_QCT        = tbl.T;
C_IntEq_QCT  = tbl.C_IntEq;
C_RotEq_QCT  = tbl.C_RotEq;
C_VibEq_QCT  = tbl.C_VibEq;
C_IntQSS_QCT = tbl.C_IntQSS;
C_RotQSS_QCT = tbl.C_RotQSS;
C_VibQSS_QCT = tbl.C_VibQSS;
clear opts tbl


opts = delimitedTextImportOptions("NumVariables", 7);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["T", "C_IntEq", "C_RotEq", "C_VibEq", "C_IntQSS", "C_RotQSS", "C_VibQSS"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
tbl = readtable(strcat(DataFldr,'/DNN/EDCoeffs_O2_2_1_1_0.csv'), opts);
T_DNN        = tbl.T;
C_IntEq_DNN  = tbl.C_IntEq;
C_RotEq_DNN  = tbl.C_RotEq;
C_VibEq_DNN  = tbl.C_VibEq;
C_IntQSS_DNN = tbl.C_IntQSS;
C_RotQSS_DNN = tbl.C_RotQSS;
C_VibQSS_DNN = tbl.C_VibQSS;
clear opts tbl

figure
h0 = plot(T_QCT,     C_IntQSS_QCT, '-k','MarkerSize',10,'LineWidth',3,'markerfacecolor','k');
hold on
plot(T_QCT,     C_IntQSS_QCT, 'ok','MarkerSize',10,'LineWidth',3,'markerfacecolor','k');
plot(T_DNN,      C_IntQSS_DNN, '^-r','MarkerSize',10,'LineWidth',3,'markerfacecolor','r');

h1 = plot(T_QCT,     C_RotQSS_QCT, ':k','MarkerSize',10,'LineWidth',3,'markerfacecolor','k');
plot(T_QCT,     C_RotQSS_QCT, 'o:k','MarkerSize',10,'LineWidth',3,'markerfacecolor','k');
plot(T_DNN,      C_RotQSS_DNN, '^:r','MarkerSize',10,'LineWidth',3,'markerfacecolor','r');

h2 = plot(T_QCT,     C_VibQSS_QCT, '--k','MarkerSize',10,'LineWidth',3,'markerfacecolor','k');
plot(T_QCT,     C_VibQSS_QCT, 'o--k','MarkerSize',10,'LineWidth',3,'markerfacecolor','k');
plot(T_DNN,      C_VibQSS_DNN, '^--r','MarkerSize',10,'LineWidth',3,'markerfacecolor','r');

legend([h0,h1,h2],'C$^{DI}$','C$^{DR}$','C$^{DV}$')
legend boxoff

box on
xlabel('T [K]');
ylabel('CE Coeffecients');
%set(gca,'XTickLabels',[0 5000 10000 15000 20000])