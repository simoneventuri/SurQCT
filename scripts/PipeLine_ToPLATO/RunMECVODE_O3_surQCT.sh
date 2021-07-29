#!/bin/bash
#===============================================================================================================
# Ex. of Call: bash RunMECVODE.sh O3 10000 $WORKSPACE_PATH/neqplasma_QCT/ME_CVODE $WORKSPACE_PATH/Mars_Database/Run_0D/database/ $WORKSPACE_PATH/Mars_Database/Run_0D/ 1 1 0 -1

echo '------------------------------------------------------------------------------------------'
echo ' CoarseAIR: Coarse-Grained Quasi-Classical Trajectories                                   '
echo '------------------------------------------------------------------------------------------'
echo ' '
echo '------------------------------------------------------------------------------------------'
echo '   PipeLine for Running External Codes                                                    '
echo '------------------------------------------------------------------------------------------'
echo ' '

# source ~/.bashrc
# #module purge
# COARSEAIR_UPDATE
# COARSEAIR_release
# #PLATONORECOMB_gnu_release
# PLATO_gnu_release

export InelNNTestnum=2
export DissNNTestnum=0

export System='O3_UMN'
export FldrName='_nondim_Run1'
export Molecule_vec=('O2')
export ExchBis=0
export Tran_vec=(10000) # (1500 2500 5000 6000 8000 10000 12000 14000 15000 20000)
export T0=300
export PathToMECVODEFldr=$WORKSPACE_PATH/neqplasma_QCT/ME_CVODE
export PathToOrigDtbFldr=$WORKSPACE_PATH/Air_Database/Run_0D/database/
export PathToDtbFldr=$WORKSPACE_PATH/Air_Database/Run_0D_surQCT/database/
export PathToRunFldr=$WORKSPACE_PATH/Air_Database/Run_0D_surQCT/

export DissFlg=0
export InelFlg=1
export ExchFlg1=1
export ExchFlg2=0

ExtCode_SH_DIR=${COARSEAIR_SOURCE_DIR}"/extra/ExtCode_PipeLine/"

echo '------------------------------------------------------'
echo '  Paths:'
echo '------------------------------------------------------'
echo '  $PLATO_LIB      directory = '${PLATO_LIB}
echo '  ExtCode .sh     directory = '${ExtCode_SH_DIR}
echo '  MeCvode install directory = '${PathToMECVODEFldr}
echo '  MeCvode Dtb     directory = '${PathToDtbFldr}
echo '  MeCvode running directory = '${PathToRunFldr}
echo '------------------------------------------------------'
echo ' '

echo '------------------------------------------------------'
echo '  Inputs:'
echo '------------------------------------------------------'
echo '  System                         = '${System}
echo '  Vector of Translational Temp.s = '${Tran_vec}
echo '  Writing Dissociation?          = '${DissFlg}
echo '  Writing Inelastic?             = '${InelFlg}
echo '  Firts Exchanges to be Written? = '${ExchFlg1}
echo '  Last Exchanges  to be Written? = '${ExchFlg2}
echo '------------------------------------------------------'
echo ' '


function Load_Initialize_0D() {
  source ${ExtCode_SH_DIR}/Initialize_0D_Database_Function_ForSurQCT.sh
  Initialize_0D_Database
}


function Call_MeCvode() {
  mkdir -p ${PathToRunFldr}  
  cd ${PathToRunFldr}
  
  export OutputFldr='output_'${System}${FldrName}'_T'${TTran}'K_'${DissFlg}'_'${InelFlg}'_'${ExchFlg1}'_'${ExchFlg2}
  mkdir -p ./${OutputFldr}
  cd ./${OutputFldr} 

  export ExFldr=${PathToMECVODEFldr}/Generic_surQCT/
  echo "[RunMECVODE]: Copying MeCvode Executable from: "${ExFldr}/'exec/box_'
  scp ${ExFldr}'/exec/box_' ./

  if [ $DissFlg -eq 0 ]; then
    export InputFile=${PathToOrigDtbFldr}'/input/'${System}'/NoDiss/T'${TTran}'K.inp'
  elif [ $InelFlg -eq 0 ] && [ $ExchFlg1 -eq 0 ] && [ $ExchFlg2 -eq 0 ]; then
    export InputFile=${PathToOrigDtbFldr}'/input/'${System}'/OnlyDiss/T'${TTran}'K.inp'
  elif [ $DissFlg -eq 13 ]; then
    export InputFile=${PathToOrigDtbFldr}'/input/'${System}'/Maninder/T'${TTran}'K.inp'
  else
    export InputFile=${PathToOrigDtbFldr}'/input/'${System}'/All/T'${TTran}'K.inp'
  fi  
  echo "[RunMECVODE]: Input File: "${InputFile}
  
  echo "[RunMECVODE]: MeCvode will be executed in the Folder: "$(pwd)
  ./box_ ${OPENBLAS_NUM_THREADS} $T0 ${InputFile}
}


for TTran in "${Tran_vec[@]}"; do :
  echo "[RunMECVODE]: Translational Temperature: TTran = "${TTran}

  echo "[RunMECVODE]: Calling Load_Initialize_0D"
  Load_Initialize_0D
  echo " "

  echo "[RunMECCVODE]: Calling Call_MeCvode"
  Call_MeCvode
  echo " "

  rm -rf $PathToDtbFldr/"/kinetics/KineticsTEMP_T"$TTran"K_"$System

done
