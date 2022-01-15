clear all
close all
clc

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1250 1250]) 
prev = st_set_graphics_defaults();

        Syst.CFDComp(1).Name   = 'N';
        Syst.CFDComp(2).Name   = 'O';
        Syst.CFDComp(3).Name   = 'N2';
        Syst.CFDComp(4).Name   = 'NO';


        Syst.CFDComp(1).Color   = [ 102, 102, 102] ./ 256;
        Syst.CFDComp(2).Color   = [   0,   0,   0] ./ 256;
        Syst.CFDComp(3).Color   = [ 204,   0,   0] ./ 256;
        Syst.CFDComp(4).Color   = [   0,   0, 234] ./ 256;

T = 15000;

StSFldr1 = '/home/venturi/WORKSPACE/Air_Database/Run_0D_surQCT/FromSungMin/output_NON_UMN_T';
StSFldr2 = 'K_1_1_0_1/box.dat';

  filename = strcat(StSFldr1, num2str(T), StSFldr2)
  formatSpec = '%20f%20f%20f%20f%20f%20f%20f%20f%20f%f%[^\n\r]';
  %formatSpec = '%14f%14f%14f%14f%14f%14f%14f%14f%14f%f%[^\n\r]';
  fileID = fopen(filename,'r');
  dataArray = textscan(fileID, formatSpec, 'Delimiter', '', 'WhiteSpace', '', 'TextType', 'string',  'ReturnOnError', false);
  fclose(fileID);
  time_StS     = dataArray{:, 1};
  
  for i =1:10
    DATA(:,i) = dataArray{:, i};
  end
  
  filename2=strcat(StSFldr1, num2str(T), StSFldr2,'_new');
  fileID = fopen(filename2,'w');

for i = 1:length(time_StS)
    fprintf(fileID,'%14e%14e%14e%14e%14e%14e%14e%14e%14e%14e\n',DATA(i,:));
end

fclose(fileID)