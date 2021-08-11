# Lateral Erosion Functions

import numpy as np


# Funcao para erosao lateral dentro de uma celula
def Lateral_Erosion_cell(hcelula, hplanicie, LatCoef1, LatCoef2, AreaHex, Aplanicie, Acanal, dt, Lat_h_coef, Qeqb):
	
	randcoef = np.random.rand()
	
	Atemp = (Acanal/Aplanicie)*randcoef*LatCoef1*(Qeqb**LatCoef2)
	
	Vol_cell = Atemp*(hcelula - hplanicie) + Atemp*(Lat_h_coef)
	
	Vol_ter = (AreaHex - Aplanicie)*(hcelula - hplanicie) 
	
	if Vol_cell <= Vol_ter:		# Verifica volume total do terraco da celula para conservar a massa no modelo
		
		Atemp = Vol_cell/(hcelula - hplanicie)
		
		Qtemp = Vol_cell
		
	else:
		
		Atemp = Vol_ter/(hcelula - hplanicie)
		
		Qtemp = Vol_ter
		
	
	Atemp += Aplanicie
	
	htemp = hcelula
	
	if Atemp >= AreaHex:
		
		Atemp = AreaHex
		
		htemp = hplanicie
	
	return(Qtemp, Atemp, htemp)

# Funcao para erosao lateral em celula vizinha
def Lateral_Erosion_neig(hcelula, htemp, hplantemp, Aplantemp, Acanal, LatCoef1, LatCoef2, AreaHex, dt, Lat_h_coef, Qeqb):
	
	Nneig = len(htemp)
	
	count = 0
	
	Qtemp = 0
	
	while count < Nneig :
		
		randcoef = np.random.rand()
		
		Aeros = (Acanal/AreaHex)*randcoef*LatCoef1*(Qeqb**LatCoef2)
		
		Vol_cell = (AreaHex - Aplantemp[count])*(htemp[count] - hplantemp[count]) 
		Vol_ero = Aeros*(htemp[count] - hcelula) + Aeros*(Lat_h_coef)		# Equacao de erosao lateral entre vizinhos <<<<<<<<<<<<<<<<<<<<
		
		# verifica se o volume de sedimento disponivel que nao eh planicie e maior do que o erodido
		if Vol_cell > Vol_ero:
			
			Qtemp += Vol_ero
			
			htemp[count] += - Vol_ero/(AreaHex - Aplantemp[count])
			
			count += 1
			
			continue
		
		Vol_ero_neig = Vol_ero - Vol_cell
		
		
		Qtemp += Vol_ero
		
		htemp[count] = hplantemp[count] - Vol_ero_neig/AreaHex
		
		hplantemp[count] = htemp[count]
		
		count += 1
	
	return(Qtemp, htemp, hplantemp)