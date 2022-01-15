close all
clear all
clc

set(0, 'defaultFigureRenderer', 'painters')                                     
set(0,'defaultfigurecolor',             [1 1 1]);                               
set(0,'defaultfigureposition',  [10 200 1200 900]) 

colors = distinguishable_colors(30);
prev = st_set_graphics_defaults();


%% Import data from text file.

filename = '/Users/maitreyeesharma/WORKSPACE/SurQCT/ImprovingFeatureSpace/Data/N2_DissRef.csv';
delimiter = ',';
startRow = 2;
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(fileID);
clearvars filename delimiter startRow formatSpec fileID ans;

% Allocate imported array to column variable names
vqn = dataArray{:, 1};
jqn = dataArray{:, 2};
EVib = dataArray{:, 3};
ERot = dataArray{:, 4};
rMin = dataArray{:, 5};
rMax = dataArray{:, 6};
VMin = dataArray{:, 7};
VMax = dataArray{:, 8};
Tau = dataArray{:, 9};
ri = dataArray{:, 10};
ro = dataArray{:, 11};

EVib_nd = (EVib-min(VMin))./(-min(VMin));
%EVib_nd = (EVib)./(-min(VMin));
ERot_nd = ERot./(-min(VMin));
rMin_nd = rMin./(min(rMin));
rMax_nd = rMax./(max(rMax));
VMin_nd = VMin./(-min(VMin));
VMax_nd = VMax./(-min(VMin));
Tau_nd  = Tau./(max(Tau));
ri_nd   = ri./rMin;
ro_nd   = ro./rMin;

filename = '/Users/maitreyeesharma/WORKSPACE/SurQCT/ImprovingFeatureSpace/Data/N2_nd.csv';
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'w');
fprintf(fileID,'vqn,jqn,EVib,ERot,rMin,rMax,VMin,VMax,Tau,ri,ro\n'); 

for i = 1:length(vqn)
    fprintf(fileID,'%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f\n', ...
                    vqn(i), jqn(i), EVib_nd(i), ERot_nd(i), ...
                    rMin_nd(i), rMax_nd(i), VMin_nd(i), VMax_nd(i), ...
                    Tau_nd(i), ri_nd(i), ro_nd(i));
end

    fclose(fileID);
    
    
%% Compare

filename = '/Users/maitreyeesharma/WORKSPACE/SurQCT/ImprovingFeatureSpace/Data/O2_nd.csv';
delimiter = ',';
startRow = 2;
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(fileID);
clearvars filename delimiter startRow formatSpec fileID ans;

% Allocate imported array to column variable names
vqn_o2 = dataArray{:, 1};
jqn_o2 = dataArray{:, 2};
EVib_o2 = dataArray{:, 3};
ERot_o2 = dataArray{:, 4};
rMin_o2 = dataArray{:, 5};
rMax_o2 = dataArray{:, 6};
VMin_o2 = dataArray{:, 7};
VMax_o2 = dataArray{:, 8};
Tau_o2 = dataArray{:, 9};
ri_o2 = dataArray{:, 10};
ro_o2 = dataArray{:, 11};
E_o2 = EVib_o2 + ERot_o2;

clear dataArray

filename = '/Users/maitreyeesharma/WORKSPACE/SurQCT/ImprovingFeatureSpace/Data/N2_nd.csv';
delimiter = ',';
startRow = 2;
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(fileID);
clearvars filename delimiter startRow formatSpec fileID ans;

% Allocate imported array to column variable names
vqn_n2 = dataArray{:, 1};
jqn_n2 = dataArray{:, 2};
EVib_n2 = dataArray{:, 3};
ERot_n2 = dataArray{:, 4};
rMin_n2 = dataArray{:, 5};
rMax_n2 = dataArray{:, 6};
VMin_n2 = dataArray{:, 7};
VMax_n2 = dataArray{:, 8};
Tau_n2 = dataArray{:, 9};
ri_n2 = dataArray{:, 10};
ro_n2 = dataArray{:, 11};
E_n2 = EVib_n2 + ERot_n2;

clear dataArray

figure(1)
plot(E_n2,EVib_n2,'o');
hold on
plot(E_o2,EVib_o2,'o');
box on
legend('N$_2$','O$_2$');
legend boxoff

figure(2)
plot(E_n2,ERot_n2,'o');
hold on
plot(E_o2,ERot_o2,'o');
box on
legend('N$_2$','O$_2$');
legend boxoff
xlabel('$\epsilon$/VMin')
ylabel('$\epsilon_{rot}$/VMin')

figure(3)
plot(E_n2,log(Tau_n2),'o');
hold on
plot(E_o2,log(Tau_o2),'o');
box on
legend('N$_2$','O$_2$');
legend boxoff
xlabel('$\epsilon$/VMin')
ylabel('$\tau$/$\tau_{max}$')

figure(4)
plot(E_n2,log(ro_n2),'o');
hold on
plot(E_o2,log(ro_o2),'o');
box on
legend('N$_2$','O$_2$');
legend boxoff
xlabel('$\epsilon$/VMin')
ylabel('ro/rMin')

%%

filename = '/Users/maitreyeesharma/WORKSPACE/SurQCT/ImprovingFeatureSpace/Data/O2_nd_logrotau.csv';
fileID = fopen(filename,'w');
fprintf(fileID,'vqn,jqn,EVib,ERot,rMin,rMax,VMin,VMax,Tau,ri,ro\n'); 
Tau_o2 = log(Tau_o2);
ro_o2 = log(ro_o2);

for i = 1:length(vqn_o2)
    fprintf(fileID,'%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f\n', ...
                    vqn_o2(i), jqn_o2(i), EVib_o2(i), ERot_o2(i), ...
                    rMin_o2(i), rMax_o2(i), VMin_o2(i), VMax_o2(i), ...
                    Tau_o2(i), ri_o2(i), ro_o2(i));
end

fclose(fileID);

filename = '/Users/maitreyeesharma/WORKSPACE/SurQCT/ImprovingFeatureSpace/Data/N2_nd_logrotau.csv';
fileID = fopen(filename,'w');
fprintf(fileID,'vqn,jqn,EVib,ERot,rMin,rMax,VMin,VMax,Tau,ri,ro\n'); 
Tau_n2 = log(Tau_n2);
ro_n2 = log(ro_n2);

for i = 1:length(vqn_o2)
    fprintf(fileID,'%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f\n', ...
                    vqn_n2(i), jqn_n2(i), EVib_n2(i), ERot_n2(i), ...
                    rMin_n2(i), rMax_n2(i), VMin_n2(i), VMax_n2(i), ...
                    Tau_n2(i), ri_n2(i), ro_n2(i));
end

fclose(fileID); 

%% log e vib, rot, ro and tau

filename = '/Users/maitreyeesharma/WORKSPACE/Air_Database/Run_0D/database/levels/46DPM_Sampled/O2_exch.csv';
delimiter = ',';
startRow = 2;
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(fileID);
clearvars filename delimiter startRow formatSpec fileID ans;

% Allocate imported array to column variable names
vqn = dataArray{:, 1};
jqn = dataArray{:, 2};
EVib = dataArray{:, 3};
ERot = dataArray{:, 4};
rMin = dataArray{:, 5};
rMax = dataArray{:, 6};
VMin = dataArray{:, 7};
VMax = dataArray{:, 8};
Tau = dataArray{:, 9};
ri = dataArray{:, 10};
ro = dataArray{:, 11};

ERot = log(ERot + 1e-10.*ones(length(ERot),1));

filename = '/Users/maitreyeesharma/WORKSPACE/Air_Database/Run_0D/database/levels/46DPM_Sampled/O2_LogELogR.csv';
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'w');
fprintf(fileID,'vqn,jqn,EVib,ERot,rMin,rMax,VMin,VMax,Tau,ri,ro\n'); 

for i = 1:length(vqn)
    fprintf(fileID,'%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f\n', ...
                    vqn(i), jqn(i), EVib(i), ERot(i), ...
                    rMin(i), rMax(i), VMin(i), VMax(i), ...
                    Tau(i), ri(i), ro(i));
end

    fclose(fileID);
cd 