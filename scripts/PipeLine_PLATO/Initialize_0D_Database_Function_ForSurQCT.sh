#===============================================================================================================
function Initialize_0D_Database {



  echo "Units=cm^3/s" > $PathToDtbFldr"/kinetics/KineticsTEMP_T"$TTran"K_"$System



  #######################################################################################################3
  #### Adding Dissociation Processes
  #### 
  if [ $DissFlg -eq 1 ] || [ $DissFlg -eq 13 ]; then
    echo "  [Initialize_0D_Database]: Adding Dissociation Kinetics to File "$PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
    cat $PathToDtbFldr"/kinetics/"${System}${FldrName}"/T"$TTran"K/Diss.dat" >> $PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System

  ############################################################## For O2+O     
  elif [ $DissFlg -eq 2 ]; then
    echo "  [Initialize_0D_Database]: Adding Corrected Dissociation Kinetics to File "$PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
    cat $PathToOrigDtbFldr"/kinetics/"${System}"/T"$TTran"K/Diss_Corrected.dat" >> $PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System

  fi
      


  #######################################################################################################3
  #### Adding Inelastic Processes
  #### 
  iInel=${InelFlg}
  if [ ${iInel} -eq 1 ]; then
    echo "  [Initialize_0D_Database]: Adding Inelastic Kinetics to File "$PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
    cat $PathToDtbFldr"/kinetics/"${System}${FldrName}"/T"$TTran"K/Inel.dat" >> $PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
  fi



  #######################################################################################################3
  #### Adding Exchange Processes
  #### 
  iExch=${ExchFlg1}
  if [ ${iExch} -eq 1 ]; then
    echo "  [Initialize_0D_Database]: Adding Exchange Kinetics to File "$PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System 
    cat $PathToDtbFldr"/kinetics/"${System}${FldrName}"/T"$TTran"K/Exch_Type1.dat" >> $PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
  fi

  iExch=${ExchFlg2}
  if [ ${iExch} -eq 1 ]; then
    echo "  [Initialize_0D_Database]: Adding Exchange Kinetics to File "$PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
    cat $PathToDtbFldr"/kinetics/"${System}${FldrName}"/T"$TTran"K/Exch_Type2.dat" >> $PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System
  fi



  #######################################################################################################3
  #### Adding Molecules Info
  #### 
  for Molecule in "${Molecule_vec[@]}"; do :

    echo "  [Initialize_0D_Database]: Copying Thermo File "$PathToDtbFldr/"/thermo/"${Molecule}"_T"${TTran}"K"
    cat $PathToOrigDtbFldr"/thermo/"${System}"/"${Molecule}"_T"${TTran}"K" > $PathToDtbFldr/"/thermo/"${Molecule}"_T"${TTran}"K"

    echo "  [Initialize_0D_Database]: Copying Initial Mole Fraction File "$PathToDtbFldr/"/thermo/"${Molecule}"_T"${T0}"K"
    cat $PathToOrigDtbFldr"/thermo/"${System}"/"${Molecule}"_InitialMoleFracs_T"${T0}"K.dat" > $PathToDtbFldr/"/thermo/"${Molecule}"_InitialMoleFracs_T"${T0}"K.dat"

  done

}
