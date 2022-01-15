% -- MATLAB --
%%==============================================================================================================
% 
% Surrogate Model for quasi-classical trajectory calculations using
% DeepOnet
% 
% Copyright (C) 2021 Maitreyee Sharma (University of Illinois at Urbana-Champaign). 
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

clear all 
close all
clc

set(0,'defaultFigureRenderer',         'painters')                                     
set(0,'defaultfigurecolor',               [1 1 1])
set(0,'defaultfigureposition',  [10 200 1200 1000]) 
%prev = st_set_graphics_defaults();

%%
opts = delimitedTextImportOptions("NumVariables", 2);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["Idx", "Group"];
opts.VariableTypes = ["double", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
filename = "/home/venturi/WORKSPACE/CoarseAIR/coarseair/dtb/Molecules/N2/LeRoy/Bins_61/LevelsMap_InelAmal61.csv";
LevelsMapInelAmal = readtable(filename, opts);
LevelsMapInelAmal = table2array(LevelsMapInelAmal);
clear opts

%%
nb_groups = max(LevelsMapInelAmal(:,2));
FileName           = strcat('/home/venturi/WORKSPACE/Air_Database/Run_0D/database/levels/N2_Sampled_Inel_1SpG_1500K.csv' );
fileID = fopen(FileName,'w');
fprintf(fileID,'#iLevel\n');

for j = 1:nb_groups
    levels_group(:) = LevelsMapInelAmal(LevelsMapInelAmal(:,2)==j);
    levels_sampled(:) = datasample(levels_group(:),1);
    fprintf(fileID,'%i\n',levels_sampled(:));
    clear levels_group levels_sampled
end
    
fclose(fileID);
