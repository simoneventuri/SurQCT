function Sampled_states_onDiatPot()          
    
    global Input Param Syst Temp
    
    iMol = 1;
    Temp.TNow = 20000;
    
    FileName = strcat(Input.Paths.ToKinMainFldrQCT,'/database/levels/46DPM_Sampled/',Syst.Molecule(iMol).Name,'_Sampled_',num2str(Temp.TNow),'K.csv');
    opts = delimitedTextImportOptions("NumVariables", 1);
    opts.DataLines = [2, Inf];
    opts.Delimiter = ",";
    opts.VariableNames = "iLevel";
    opts.VariableTypes = "double";
    opts.ExtraColumnsRule = "ignore";
    opts.EmptyLineRule = "read";
    O2SampledLevelsTable = readtable(FileName, opts);
    O2SampledLevels = table2array(O2SampledLevelsTable);
    clear opts

    
    
fprintf('    Writing Sampled States on Diatomic Potential Properties\n')
FileName1 = strcat(Input.Paths.SaveDataFldr,'/', Syst.Molecule(iMol).Name,'_Sampled_T',num2str(Temp.TNow), 'K_paraview.csv');
fileID1   = fopen(FileName1,'w');
fprintf(fileID1,'#Idx,EeV,g,rIn,v,J,ECB,Sample\n');

a = 1;
for i = 1:size(O2SampledLevels,1)
    iLevel =   O2SampledLevels(i);  
    fprintf(fileID1,'%i,%e,%e,%e,%i,%i,%e,%i\n',   iLevel,                                      ...
                                                               Syst.Molecule(iMol).LevelEeV(iLevel),        ...
                                                               Syst.Molecule(iMol).Levelg(iLevel),          ...
                                                               Syst.Molecule(iMol).LevelrIn(iLevel),        ...
                                                               Syst.Molecule(iMol).Levelvqn(iLevel),        ...
                                                               Syst.Molecule(iMol).Leveljqn(iLevel),        ...
                                                               Syst.Molecule(iMol).LevelECB(iLevel),        ...
                                                               a); 
end
fclose(fileID1);
end