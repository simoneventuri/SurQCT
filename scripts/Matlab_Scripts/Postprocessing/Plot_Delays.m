clear all
%close all
clc

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1250 1250]) 
prev = st_set_graphics_defaults();

DepPerc = 0.50;

%T0_Vec  = [1500, 5000, 8000, 10000, 20000]; %, 12000, 15000, 20000];
T0_Vec = [10000];

Input.Inel.TestNum = '4';
Input.Exch.TestNum = '4';
Input.FNN.TestNum = '55';
Input.Dimension = 'transfer';
Input.System = 'N3_NASA'

StSFldr1 = strcat('/home/venturi/WORKSPACE/Air_Database/Run_0D_semi/output_',Input.System,'_T');
StSFldr2 = 'K_1_1_1_0/box.dat';

surQCT1    = strcat('/home/venturi/WORKSPACE/Air_Database/Run_0D_surQCT/',Input.Dimension,'_RunI',Input.Inel.TestNum,'_E',Input.Exch.TestNum,'_D',Input.FNN.TestNum,'/output_',Input.System,'_T');
%surQCT1 = '/home/venturi/WORKSPACE/Air_Database/Run_0D/output_O3_UMN_T';
surQCT2    = 'K_1_100_100_0/box.dat';

% StSFldr1 = '/home/venturi/WORKSPACE/Air_Database/Run_0D_semi/output_N3_NASA_T';
% StSFldr2 = 'K_1_1_1_0/box.dat';
% 
% surQCT1    = strcat('/home/venturi/WORKSPACE/Air_Database/Run_0D_surQCT/nondim_RunI',Input.Inel.TestNum,'_E',Input.Exch.TestNum,'_D',Input.FNN.TestNum,'/output_N3_NASA_T');
% surQCT2    = 'K_1_1_1_0/box.dat';

iTT = 0;
DelayVec_CB45   = [];
DelayVec_CB45_F = [];
DelayVec_CB20   = [];
DelayVec_CB20_F = [];
DelayVec_CB15   = [];
DelayVec_CB15_F = [];
DelayVec_CB10   = [];
DelayVec_CB10_F = [];
DelayVec_VS     = [];
DelayVec_VS_ALL = [];

for T = T0_Vec
  iTT  = iTT+1;
  Epst = 1.e-4; 
  T
  filename = strcat(StSFldr1, num2str(T), StSFldr2)
  formatSpec = '%20f%*20f%20f%[^\n\r]';
  fileID = fopen(filename,'r');
  dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'TextType', 'string',  'ReturnOnError', false);
  fclose(fileID);
  time_StS     = dataArray{:, 1};
  MoleFrac_StS = dataArray{:, 2};
  clearvars filename formatSpec fileID dataArray ans;
  if MoleFrac_StS(end) > MoleFrac_StS(1)
    RecFlg = true;
  else
    RecFlg = false;
  end
  i_StS = 1
  while abs( (MoleFrac_StS(i_StS) - MoleFrac_StS(1)) / (MoleFrac_StS(1) - MoleFrac_StS(end)) ) < DepPerc
    i_StS = i_StS + 1;
  end
  Deltat =         time_StS(i_StS) - time_StS(i_StS-1);
  DeltaM = abs(MoleFrac_StS(i_StS) - MoleFrac_StS(i_StS-1));
  if RecFlg 
    TempM  = DepPerc*abs(MoleFrac_StS(1) - MoleFrac_StS(end)) + MoleFrac_StS(1) - MoleFrac_StS(i_StS-1);
  else
    TempM  = DepPerc*abs(MoleFrac_StS(1) - MoleFrac_StS(end)) + MoleFrac_StS(i_StS-1) - MoleFrac_StS(1);
  end
  t_StS  = time_StS(i_StS-1) + Deltat * TempM / DeltaM;
  
  
  filename = strcat(surQCT1, num2str(T), surQCT2)
  formatSpec = '%20f%*20f%20f%[^\n\r]';
  fileID = fopen(filename,'r');
  dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'TextType', 'string',  'ReturnOnError', false);
  fclose(fileID);
  time_CB45     = dataArray{:, 1};
  MoleFrac_CB45 = dataArray{:, 2};
  clearvars filename formatSpec fileID dataArray ans;
  i_CB45 = 1
  while abs( (MoleFrac_CB45(i_CB45) - MoleFrac_CB45(1)) / (MoleFrac_CB45(1) - MoleFrac_CB45(end)) ) < DepPerc
    i_CB45 = i_CB45 + 1;
  end
  Deltat =         time_CB45(i_CB45) - time_CB45(i_CB45-1);
  DeltaM = abs(MoleFrac_CB45(i_CB45) - MoleFrac_CB45(i_CB45-1));
  if RecFlg 
    TempM  = DepPerc*abs(MoleFrac_CB45(1) - MoleFrac_CB45(end)) + MoleFrac_CB45(1) - MoleFrac_CB45(i_CB45-1);
  else
    TempM  = DepPerc*abs(MoleFrac_CB45(1) - MoleFrac_CB45(end)) + MoleFrac_CB45(i_CB45-1) - MoleFrac_CB45(1);
  end
  t_CB45 = time_CB45(i_CB45-1) + Deltat * TempM / DeltaM;
  DelayVec_CB45(iTT) = (t_CB45 - t_StS)/t_StS;
  
  
  figure(iTT)
  semilogx(time_StS,MoleFrac_StS,'k','LineWidth',3)
  hold on
  %semilogx(t_StS, MoleFrac_StS(1) - DepPerc*(MoleFrac_StS(1) - MoleFrac_StS(end)), 'ko')
 
  semilogx(time_CB45,MoleFrac_CB45,'b','LineWidth',3)
  %semilogx(t_CB45,MoleFrac_CB45(1) - DepPerc*(MoleFrac_CB45(1) - MoleFrac_CB45(end)),'bo')
  set(gca,'tickdir','out')
  xlabel('t [s]')
  ylabel('X')
  box on
  legend('QCT','SurQCT')
  legend boxoff

  clear time_StS MoleFrac_StS time_CB45 MoleFrac_CB45 time_CB45_F MoleFrac_CB45_F time_CB10 MoleFrac_CB10 time_CB10_F MoleFrac_CB10_F time_VS MoleFrac_VS time_VS_ALL MoleFrac_VS_ALL
end


figure(1000)
plot(T0_Vec,-100.0.*DelayVec_CB45,'b','LineWidth',3)
hold on

plot(T0_Vec,-100.0.*DelayVec_CB45,'bo','MarkerSize',20,'LineWidth',3)
box on
xlabel('T [K]');
ylabel('O$_2$ Depletion Delay [\%]');

    xt = get(gca, 'XTick');
    set(gca,'FontSize',30, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');
    yt = get(gca, 'YTick');
    set(gca,'FontSize',30, 'TickDir', 'out', 'TickLabelInterpreter', 'latex');


% figure
% plot(T0_Vec,DelayVec_CB45_F,'b')
% hold on
% plot(T0_Vec,DelayVec_CB20_F,'g')
% plot(T0_Vec,DelayVec_CB15_F,'c')
% plot(T0_Vec,DelayVec_CB10_F,'y')
% plot(T0_Vec,DelayVec_VS,'r')
% plot(T0_Vec,DelayVec_VS_ALL,'m')
% 
% plot(T0_Vec,DelayVec_CB45_F,'bo')
% plot(T0_Vec,DelayVec_CB20_F,'go')
% plot(T0_Vec,DelayVec_CB15_F,'co')
% plot(T0_Vec,DelayVec_CB10_F,'yo')
% plot(T0_Vec,DelayVec_VS,'ro')
% plot(T0_Vec,DelayVec_VS_ALL,'mo')
