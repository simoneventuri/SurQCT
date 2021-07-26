# SurQCT
Machine-Learning-Based Surrogate Models for Quasi-Classical Trajectory Method



### Running the Code:

	- Execute the SurQCT.py script (/SurQCT/surqct/exec/SurQCT.py) passing the folder containing the input file as argument
		E.g.: python3 SurQCT.py ../input/O3_UMN/KInel/



### Additional Scripts:


	- /SurQCT/surqct/scripts/running_QCT/Active_Learning.ipynb
		Script for:
			- Simulating active learning based on scattering probabilities

	- /SurQCT/surqct/scripts/running_QCT/Generate_InitialLevelList.ipynb
		Script for:
			- Sampling initial levels from molecule's groups

	- /SurQCT/surqct/scripts/running_QCT/Check_LevelsAndGroups.ipynb
		Script for:
			- Checking for consistency between sampled levels and groups


	- /SurQCT/surqct/scripts/preprocessing/Preprocess_Variables.py
		Script for:
			- Preprocessing levels' quantities
			- Writing data files to be used as surrogate's input data
			- Creating scatter plot for checking correlations between variables