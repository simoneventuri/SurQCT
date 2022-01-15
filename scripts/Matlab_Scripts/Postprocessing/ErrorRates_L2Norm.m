function Error = ErrorRates_L2Norm(Controls,RatesQCT,RatesDNN)

    global Syst Temp Input 
    
    fprintf('= Compute_Rates_Error ================= T = %i K\n', Temp.TNow)
    fprintf('====================================================\n')
          
    iMol   = 1;
    iNBins = Syst.Molecule(iMol).EqNStatesIn;        
    
%     for iLevel = 1:size(Syst.Molecule(iMol).LevelEeV,1)
%         RatesDNN.T(Temp.iT).Inel(iLevel,iLevel) = RatesQCT.T(Temp.iT).Inel(iLevel,iLevel);  
%     end

    % Error Matrix
    Error_Mat = abs(log(RatesQCT.T(Temp.iT).Inel) - log(RatesDNN.T(Temp.iT).Inel))./log(RatesQCT.T(Temp.iT).Inel);

    % Max Error 
    Error.Rate.MaxErr = max(Error_Mat,[],2);
    Error.Rate.L1Norm = vecnorm(Error_Mat,1,2);
    Error.Rate.L2Norm = vecnorm(Error_Mat,2,2);
    
%                     
%     fprintf('    Writing Error Population on Diatomic Potential Properties\n')
%     FileName1 = strcat(Input.Paths.SaveDataFldr, '/Test', Input.DNN.TestNum ,'_T', Temp.TNowChar, 'K_Error_Rate_withLevels.csv');    
%     fileID1   = fopen(FileName1,'w');    
%     fprintf(fileID1,'#Idx,EeV,g,rIn,v,J,ECB,ErrorMax,ErrorL1,ErrorL2\n');
% 
%     for iLevel = 1:size(Syst.Molecule(iMol).LevelEeV,1)
%         fprintf(fileID1,'%i,%e,%e,%e,%i,%i,%e,%e,%e.%e\n',   iLevel,                                      ...
%                                                                Syst.Molecule(iMol).LevelEeV(iLevel),        ...
%                                                                Syst.Molecule(iMol).Levelg(iLevel),          ...
%                                                                Syst.Molecule(iMol).LevelrIn(iLevel),        ...
%                                                                Syst.Molecule(iMol).Levelvqn(iLevel),        ...
%                                                                Syst.Molecule(iMol).Leveljqn(iLevel),        ...
%                                                                Syst.Molecule(iMol).LevelECB(iLevel),        ...
%                                                                Error.Rate.MaxErr(iLevel),                   ...
%                                                                Error.Rate.L1Norm(iLevel),                   ...
%                                                                Error.Rate.L2Norm(iLevel));            
%     end
%     fclose(fileID1);
%     
    
            AddedInelFlg = false;
            KijQCT          = RatesQCT.T(Temp.iT).Inel;
            KijDNN          = RatesDNN.T(Temp.iT).Inel;
            
            for iProc = 1:length(Controls.vqns)
                vqn = Controls.vqns(iProc)
                jqn = Controls.jqns(iProc);
                
                for iLevel = 1:Syst.Molecule(iMol).NLevels

                    if ( (Syst.Molecule(iMol).Levelvqn(iLevel) == vqn) && (Syst.Molecule(iMol).Leveljqn(iLevel) == jqn) )
                        
                        [status,msg,msgID] = mkdir(strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K/'));
                        FileName           = strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K/Testing_InelRates_i',num2str(iProc),'_', Input.Kin.Proc.OverallFlg,'_vJPlots.csv' );
                        fileID = fopen(FileName,'w');
                        fprintf(fileID,'id,v,J,EeV,rIn,rOut,EeVVib,EeVRot,dCentBarr,rIn_i,J_i,EeV_i,KInelQCT,KInelDNN,ErrorKInel\n');
                        for jLevel = 1:Syst.Molecule(iMol).NLevels
                            
%                             if (Syst.Molecule(iMol).LevelEeV(iLevel) >= Syst.Molecule(iMol).LevelEeV(jLevel))
                                KInelQCT = KijQCT(iLevel,jLevel);
                                KInelDNN = KijDNN(iLevel,jLevel);
                                ErrorKInel = Error_Mat(iLevel,jLevel);
%                             else
%                                 KInel = Rates.T(Temp.iT).Inel(jLevel,iLevel) * Syst.Molecule(iMol).T(Temp.iT).Levelq(jLevel) / Syst.Molecule(iMol).T(Temp.iT).Levelq(iLevel);
%                             end
                            if (KInelDNN > 1e-15)
                                fprintf(fileID,'%i,%i,%i,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e,%e\n', jLevel,       	                ...
                                                                                  Syst.Molecule(iMol).Levelvqn(jLevel),     ...
                                                                                  Syst.Molecule(iMol).Leveljqn(jLevel),     ...
                                                                                  Syst.Molecule(iMol).LevelEeV(jLevel),     ...
                                                                                  Syst.Molecule(iMol).LevelrIn(jLevel),     ...
                                                                                  Syst.Molecule(iMol).LevelrOut(jLevel),    ...
                                                                                  Syst.Molecule(iMol).LevelEeVVib0(jLevel), ...
                                                                                  Syst.Molecule(iMol).LevelEeVRot(jLevel),  ...
                                                                                  Syst.Molecule(iMol).LevelECB(jLevel),     ...
                                                                                  Syst.Molecule(iMol).LevelrIn(iLevel),     ...
                                                                                  Syst.Molecule(iMol).Leveljqn(iLevel),     ...
                                                                                  Syst.Molecule(iMol).LevelEeV(iLevel),     ...
                                                                                  KInelQCT,                                 ...
                                                                                  KInelDNN,                                 ...
                                                                                  ErrorKInel);
                            end
                        end
                        fclose(fileID);

                    end
                    
                end
                
            end
            
    
end