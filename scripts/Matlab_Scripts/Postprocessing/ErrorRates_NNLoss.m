function ErrorRates_NNLoss(Controls,RatesQCT,RatesDNN)

    global Syst Temp Input 
    
    fprintf('= Compute_Rates_Error ================= T = %i K\n', Temp.TNow)
    fprintf('====================================================\n')
     
        
    Min_trainVal = 1.0e-16*1.0e9;
    KijQCT = 1.0e9.*RatesQCT.T(Temp.iT).Inel;
    KijDNN = 1.0e9.*RatesDNN.T(Temp.iT).Inel;  
    
    %TrainingError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    TotalError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    %MeuwleyError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    %vqnError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    %jqnError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    %groupError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    
end


function TrainingError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    
    global Syst Temp Input
    iMol   = 1;
    iNBins = Syst.Molecule(iMol).EqNStatesIn;     
    
    % Reading levels used in training
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
                   
    FileName           = strcat(Input.Paths.SaveDataFldr, '/Training_NNLoss_perTemp.csv' );
    if exist(FileName, 'file')
        fileID1  = fopen(FileName,'a');
    else
        fileID1  = fopen(FileName,'w');
        %fprintf(fileID,'id,v,J,EeV,rIn,rOut,EeVVib,EeVRot,dCentBarr,ErrorMax,ErrorKInel\n');
        fprintf(fileID1,'#Temp,iLevelforMaxErr, ErrorMax, ErrorKInel\n');
    end
            
    Error_sampled = 0.0;
    
    for i = 1:size(O2SampledLevels,1)
        iLevel =   O2SampledLevels(i);
        Error_max_sampled = 1e-20;
        for jLevel = 1:iLevel-1 
            if (KijQCT(iLevel,jLevel) > Min_trainVal)
                KInelQCT = KijQCT(iLevel,jLevel);
                KInelDNN = KijDNN(iLevel,jLevel);
                Error_sampled = Error_sampled + abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
                Error_max_sampled(jLevel) = abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
            end
        end        
        ErrorMax_sampled(iLevel) = max(Error_max_sampled);                         
    end
       
    [MaxError,id] = max(ErrorMax_sampled);
    
    fprintf(fileID1,'%e,%i,%e,%e\n',Temp.TNow,id,MaxError,Error_sampled);

    fclose(fileID1);

end

function TotalError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    
    global Syst Temp Input
    iMol   = 1;
    iNBins = Syst.Molecule(iMol).EqNStatesIn;     
             
    FileName           = strcat(Input.Paths.SaveDataFldr, '/Total_NNLoss_perTemp.csv' );
    if exist(FileName, 'file')
        fileID1  = fopen(FileName,'a');
    else
        fileID1  = fopen(FileName,'w');
        fprintf(fileID1,'#Temp,iLevelforMaxErr, jLevelforMaxError, ErrorMax, ErrorKInel\n');
    end
    
    Error_sampled = 0.0;
    ErrorKInel = zeros(Syst.Molecule(iMol).NLevels,1);
    
    for iLevel = 1:Syst.Molecule(iMol).NLevels
        LevelEeV_sampled(iLevel) = Syst.Molecule(iMol).LevelEeV(iLevel);
        Error_max_sampled = 1e-20;
        for jLevel = 1:iLevel-1 %Syst.Molecule(iMol).NLevels
            if (KijQCT(iLevel,jLevel) > Min_trainVal  && KijDNN(iLevel,jLevel) > 0.0)
                KInelQCT = KijQCT(iLevel,jLevel);
                KInelDNN = KijDNN(iLevel,jLevel);
                Error_sampled = Error_sampled + abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
                ErrorKInel(iLevel) = ErrorKInel(iLevel) + abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
                Error_max_sampled(jLevel) = abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
            end
        end
        
        [ErrorMax_sampled(iLevel),jid(iLevel)] = max(Error_max_sampled);                         
    end
    
    [MaxError,id] = max(ErrorMax_sampled);
    
    fprintf(fileID1,'%e,%i,%i,%e,%e\n',Temp.TNow,id,jid(id),MaxError,Error_sampled);

    fclose(fileID1);

    LevelEeV = Syst.Molecule(iMol).LevelEeV./abs(Syst.Molecule(iMol).LevelEeV(1));
    figure(Input.iFig)    
    fig = gcf;
    screensize   = get( groot, 'Screensize' );
    plot(LevelEeV, ErrorKInel,'^r','LineWidth',4)
    hold on
    box on

%     
%     figure(Input.iFig)    
%     fig = gcf;
%     screensize   = get( groot, 'Screensize' );
%     plot(Syst.Molecule(iMol).LevelEeV, ErrorMax,'^b','LineWidth',4,'MarkerSize',20)
%     hold on
%     plot(LevelEeV_sampled, ErrorMax_sampled,'^r','LineWidth',4,'MarkerSize',20)
%     hold on
%     box on            
%     Input.iFig = Input.iFig + 1;
%     
%     figure(Input.iFig)    
%     fig = gcf;
%     screensize   = get( groot, 'Screensize' );
%     plot(Syst.Molecule(iMol).Leveljqn, ErrorMax,'^b','LineWidth',4,'MarkerSize',20)
%     hold on
%     box on            
%     Input.iFig = Input.iFig + 1;

end

function MeuwleyError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    
    global Syst Temp Input
    iMol   = 1;
    iNBins = Syst.Molecule(iMol).EqNStatesIn;     
             
    FileName           = strcat(Input.Paths.SaveDataFldr, '/Meuwley_NNLoss_perTemp.csv' );
    if exist(FileName, 'file')
        fileID1  = fopen(FileName,'a');
    else
        fileID1  = fopen(FileName,'w');
        fprintf(fileID1,'#Temp,iLevelforMaxErr, jLevelforMaxError, ErrorMax, ErrorKInel\n');
    end
    
    Error_sampled = 0.0;
    ErrorKInel = zeros(Syst.Molecule(iMol).NLevels,1);
    
    for iLevel = 1:Syst.Molecule(iMol).NLevels
        LevelEeV_sampled(iLevel) = Syst.Molecule(iMol).LevelEeV(iLevel);
        Error_max_sampled = 1e-20;
        for jLevel = 1:iLevel-1 %Syst.Molecule(iMol).NLevels
            if (KijQCT(iLevel,jLevel) > Min_trainVal  && KijDNN(iLevel,jLevel) > 0.0)
                KInelQCT = KijQCT(iLevel,jLevel);
                KInelDNN = KijDNN(iLevel,jLevel);
                Error_sampled = Error_sampled + (log(KInelQCT) - log(abs(KInelQCT-KInelDNN)+KInelQCT)).^2;
                ErrorKInel(iLevel) = ErrorKInel(iLevel) + (log(KInelQCT) - log(abs(KInelQCT-KInelDNN)+KInelQCT)).^2;
                Error_max_sampled(jLevel) = (log(KInelQCT) - log(abs(KInelQCT-KInelDNN)+KInelQCT)).^2;
            end
        end
        
        [ErrorMax_sampled(iLevel),jid(iLevel)] = max(Error_max_sampled);                         
    end
    
    [MaxError,id] = max(ErrorMax_sampled);
    
    fprintf(fileID1,'%e,%i,%i,%e,%e\n',Temp.TNow,id,jid(id),MaxError,Error_sampled);

    fclose(fileID1);

    figure(106)    
    fig = gcf;
    screensize   = get( groot, 'Screensize' );
    plot(Syst.Molecule(iMol).LevelEeV, ErrorKInel,'^','LineWidth',4)
    hold on
    box on

%     
%     figure(Input.iFig)    
%     fig = gcf;
%     screensize   = get( groot, 'Screensize' );
%     plot(Syst.Molecule(iMol).LevelEeV, ErrorMax,'^b','LineWidth',4,'MarkerSize',20)
%     hold on
%     plot(LevelEeV_sampled, ErrorMax_sampled,'^r','LineWidth',4,'MarkerSize',20)
%     hold on
%     box on            
%     Input.iFig = Input.iFig + 1;
%     
%     figure(Input.iFig)    
%     fig = gcf;
%     screensize   = get( groot, 'Screensize' );
%     plot(Syst.Molecule(iMol).Leveljqn, ErrorMax,'^b','LineWidth',4,'MarkerSize',20)
%     hold on
%     box on            
%     Input.iFig = Input.iFig + 1;

end

function vqnError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    
    global Syst Temp Input
    iMol   = 1;
    iNBins = Syst.Molecule(iMol).EqNStatesIn;     
         
    [status,msg,msgID] = mkdir(strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K/'));
    FileName           = strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K/', '/vqn_NNLoss.csv' );
%     fileID1  = fopen(FileName,'w');
%     fprintf(fileID1,'#vqn, jqnforMaxError, ErrorMax, ErrorKInel\n');
    
    Error_sampled = zeros(max(Syst.Molecule(iMol).Levelvqn)+1,1);
    Error_max_sampled = zeros(Syst.Molecule(iMol).NLevels, max(Syst.Molecule(iMol).Levelvqn)+1);

    for iLevel = 1:Syst.Molecule(iMol).NLevels
        for jLevel = 1:Syst.Molecule(iMol).NLevels
            if (KijQCT(iLevel,jLevel) > Min_trainVal  && KijDNN(iLevel,jLevel) > 0.0)
                KInelQCT = KijQCT(iLevel,jLevel);
                KInelDNN = KijDNN(iLevel,jLevel);
                Error_sampled(Syst.Molecule(iMol).Levelvqn(iLevel)+1) = Error_sampled(Syst.Molecule(iMol).Levelvqn(iLevel)+1) + abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
                Error_max_sampled(jLevel,Syst.Molecule(iMol).Levelvqn(iLevel)+1) = abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
            end
        end                       
    end
    
    for i = 1:max(Syst.Molecule(iMol).Levelvqn)+1
        MaxError(i) = max(Error_max_sampled(:,i));  
%         fprintf(fileID1,'%i,%i,%e,%e\n',i,Syst.Molecule(iMol).Leveljqn(jid)+1,MaxError,Error_sampled(i));
    end
    

    vqn = [1:(max(Syst.Molecule(iMol).Levelvqn)+1)];
    figure(Input.iFig)    
    fig = gcf;
    screensize   = get( groot, 'Screensize' );
    plot(vqn, Error_sampled,'^b','LineWidth',4,'MarkerSize',20)
    hold on
    box on            
    xlabel('vqn')
    ylabel('Error')
    Input.iFig = Input.iFig + 1;
    
    figure(Input.iFig)    
    fig = gcf;
    screensize   = get( groot, 'Screensize' );
    plot(vqn, MaxError,'^b','LineWidth',4,'MarkerSize',20)
    hold on
    box on  
    xlabel('vqn')
    ylabel('Max Error')

%     fclose(fileID1);

end

function jqnError_perTemperature(KijQCT,KijDNN,Min_trainVal)
    
    global Syst Temp Input
    iMol   = 1;
    iNBins = Syst.Molecule(iMol).EqNStatesIn;     
         
    [status,msg,msgID] = mkdir(strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K/'));
    FileName           = strcat(Input.Paths.SaveDataFldr, '/T', Temp.TNowChar, 'K/', '/jqn_NNLoss.csv' );
    fileID1  = fopen(FileName,'w');
    fprintf(fileID1,'#jqn, vqnforMaxError, ErrorMax, ErrorKInel\n');
    
    Error_sampled = zeros(max(Syst.Molecule(iMol).Leveljqn)+1,1); 

    for iLevel = 1:Syst.Molecule(iMol).NLevels
        Error_max_sampled = 1e-20;
        for jLevel = 1:iLevel-1 
            if (KijQCT(iLevel,jLevel) > Min_trainVal  && KijDNN(iLevel,jLevel) > 0.0)
                KInelQCT = KijQCT(iLevel,jLevel);
                KInelDNN = KijDNN(iLevel,jLevel);
                Error_sampled(Syst.Molecule(iMol).Leveljqn(iLevel)+1) = Error_sampled(Syst.Molecule(iMol).Leveljqn(iLevel)+1) + abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
                Error_max_sampled(jLevel,Syst.Molecule(iMol).Leveljqn(iLevel)+1) = abs((log(KInelQCT)-log(KInelDNN))/log(KInelQCT));
            end
        end                       
    end
    
    for i = 1:max(Syst.Molecule(iMol).Leveljqn)+1
        [MaxError,jid] = max(Error_max_sampled(:,i));  
        fprintf(fileID1,'%i,%i,%e,%e\n',i,Syst.Molecule(iMol).Levelvqn(jid)+1,MaxError,Error_sampled(i));
    end
    
    fclose(fileID1);

end