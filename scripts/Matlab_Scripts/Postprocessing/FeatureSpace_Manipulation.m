% Feature Space modification

fprintf('    Writing Diatomic Potential Properties\n')
FileName1 = strcat('~/WORKSPACE/Air_Database/Run_0D/database/levels/N2_LogER_ro_tau_rMax.csv');
fileID1   = fopen(FileName1,'w');
fprintf(fileID1,'ECB,vqn,jqn,EVib,ERot,rMin,rMax,VMin,VMax,Tau,ri,ro\n');
            
iMol = 1; 
vqn = Syst.Molecule(iMol).Levelvqn;
VMin = Syst.Molecule(iMol).LevelVMin(1) - Syst.Molecule(iMol).LevelEeV(1);
%LevelEVib = log(Syst.Molecule(iMol).LevelEeVVib0(:) + 1.0e-10 .* ones(1, length(vqn)) + VMin .* ones(1, length(vqn)));
LevelEVib = log(Syst.Molecule(iMol).LevelEeVVib0(:) + 1.0e-10 .* ones(1, length(vqn)));
LevelERot = log(Syst.Molecule(iMol).LevelEeVRot(:) + 1.0e-10 .* ones(1, length(vqn)));
LevelrMax = log(Syst.Molecule(1).LevelrMax);
LevelrOut = log(Syst.Molecule(1).LevelrOut);
LevelTau = log(Syst.Molecule(1).LevelTau);


for iLevel = 1:size(LevelEVib,1)
fprintf(fileID1,'%e,%i,%i,%e,%e,%e,%e,%e,%e,%e,%e,%e\n', Syst.Molecule(iMol).LevelECB(iLevel),   ...
                 Syst.Molecule(iMol).Levelvqn(iLevel),        ...
                 Syst.Molecule(iMol).Leveljqn(iLevel),        ...
                 LevelEVib(iLevel),        ...
                 LevelERot(iLevel),        ...
                 Syst.Molecule(iMol).LevelrMin(iLevel),       ...
                 LevelrMax(iLevel), ...
                 Syst.Molecule(iMol).LevelVMin(iLevel),        ...                
                 Syst.Molecule(iMol).LevelVMax(iLevel),        ...
                 LevelTau(iLevel), ...
                 Syst.Molecule(iMol).LevelrIn(iLevel),        ...                
                 LevelrOut(iLevel));
                                                                    
end
fclose(fileID1);

%% Non dimensionalization

fprintf('    Writing Diatomic Potential Properties\n')
FileName1 = strcat('~/WORKSPACE/Air_Database/Run_0D/database/levels/O2_nd_rTau_only_withrMinforr.csv');
fileID1   = fopen(FileName1,'w');
fprintf(fileID1,'vqn,jqn,EVib,ERot,ECB,rMin,rMax,VMin,VMax,Tau,ri,ro\n');
            
iMol = 1; 
vqn = Syst.Molecule(iMol).Levelvqn;
VMin = Syst.Molecule(iMol).LevelVMin(1) - Syst.Molecule(iMol).LevelEeV(1);
%LevelEVib = log(Syst.Molecule(iMol).LevelEeVVib0(:) + 1.0e-10 .* ones(1, length(vqn)) + VMin .* ones(1, length(vqn)));
LevelEVib = log(Syst.Molecule(iMol).LevelEeVVib0(:) + 1.0e-10 .* ones(1, length(vqn)));
LevelERot = log(Syst.Molecule(iMol).LevelEeVRot(:) + 1.0e-10 .* ones(1, length(vqn)));
LevelrMin = (Syst.Molecule(1).LevelrMin./min(Syst.Molecule(1).LevelrMin));
LevelrMax = log(Syst.Molecule(1).LevelrMax./max(Syst.Molecule(1).LevelrMax));
LevelrIn = (Syst.Molecule(1).LevelrIn./min(Syst.Molecule(1).LevelrMin));
LevelrOut = log(Syst.Molecule(1).LevelrOut./Syst.Molecule(1).LevelrMin);
LevelTau = log(Syst.Molecule(1).LevelTau./max(Syst.Molecule(1).LevelTau));


for iLevel = 1:size(LevelEVib,1)
fprintf(fileID1,'%i,%i,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e\n', Syst.Molecule(iMol).Levelvqn(iLevel),        ...
                 Syst.Molecule(iMol).Leveljqn(iLevel),        ...
                 LevelEVib(iLevel),        ...
                 LevelERot(iLevel),        ...
                 Syst.Molecule(iMol).LevelECB(iLevel),   ...
                 LevelrMin(iLevel),       ...
                 LevelrMax(iLevel), ...
                 Syst.Molecule(iMol).LevelVMin(iLevel),        ...                
                 Syst.Molecule(iMol).LevelVMax(iLevel),        ...
                 LevelTau(iLevel), ...
                 LevelrIn(iLevel),        ...                
                 LevelrOut(iLevel));
                                                                    
end
fclose(fileID1);

%%

fprintf('    Writing Diatomic Potential Properties\n')
FileName1 = strcat('~/WORKSPACE/Air_Database/Run_0D/database/levels/N2_nd_rTau_only_withrMinforr.csv');
fileID1   = fopen(FileName1,'w');
fprintf(fileID1,'vqn,jqn,EVib,ERot,ECB,rMin,rMax,VMin,VMax,Tau,ri,ro\n');
            
iMol = 1; 
vqn = Syst.Molecule(iMol).Levelvqn;
VMin = Syst.Molecule(iMol).LevelVMin(1) - Syst.Molecule(iMol).LevelEeV(1);
%LevelEVib = log(Syst.Molecule(iMol).LevelEeVVib0(:) + 1.0e-10 .* ones(1, length(vqn)) + VMin .* ones(1, length(vqn)));
LevelEVib = log(Syst.Molecule(iMol).LevelEeVVib0(:) + 1.0e-10 .* ones(1, length(vqn)));
LevelERot = log(Syst.Molecule(iMol).LevelEeVRot(:) + 1.0e-10 .* ones(1, length(vqn)));
LevelrMin = (Syst.Molecule(1).LevelrMin./min(Syst.Molecule(1).LevelrMin));
LevelrMax = log(Syst.Molecule(1).LevelrMax./max(Syst.Molecule(1).LevelrMax));
LevelrIn = (Syst.Molecule(1).LevelrIn./min(Syst.Molecule(1).LevelrMin));
LevelrOut = log(Syst.Molecule(1).LevelrOut./Syst.Molecule(1).LevelrMin);
LevelTau = log(Syst.Molecule(1).LevelTau./max(Syst.Molecule(1).LevelTau));


for iLevel = 1:size(LevelEVib,1)
fprintf(fileID1,'%i,%i,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e\n', Syst.Molecule(iMol).Levelvqn(iLevel),        ...
                 Syst.Molecule(iMol).Leveljqn(iLevel),        ...
                 LevelEVib(iLevel),        ...
                 LevelERot(iLevel),        ...
                 Syst.Molecule(iMol).LevelECB(iLevel),   ...
                 LevelrMin(iLevel),       ...
                 LevelrMax(iLevel), ...
                 Syst.Molecule(iMol).LevelVMin(iLevel),        ...                
                 Syst.Molecule(iMol).LevelVMax(iLevel),        ...
                 LevelTau(iLevel), ...
                 LevelrIn(iLevel),        ...                
                 LevelrOut(iLevel));
                                                                    
end
fclose(fileID1);