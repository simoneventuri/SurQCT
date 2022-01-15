function ErrorRates_NNLoss_Diss(Controls,RatesQCT,RatesDNN)

    global Syst Temp Input 
    
    fprintf('= Compute_Rates_Error ================= T = %i K\n', Temp.TNow)
    fprintf('====================================================\n')
     
        
    Min_trainVal = 1.0e-18*1.0e7;
    
    KDiss_QCT = RatesQCT.T(Temp.iT).Diss;
    KDiss_DNN = RatesDNN.T(Temp.iT).Diss;
    
    ErrorDiss = abs(RatesDNN.T(Temp.iT).Diss(:,1) - RatesQCT.T(Temp.iT).Diss(:,1))./RatesQCT.T(Temp.iT).Diss(:,1);
    
    plot(Syst.Molecule(1).LevelEeV, ErrorDiss,'LineWidth',3.5)
    
end