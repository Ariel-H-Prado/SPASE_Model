# Function to find points of local minimum and create array with the flows of each cell

import numpy as np

def Flows_dir_minimum (cells, edgetype, cellsneighbor, hcelulas, sorvtype):
	
	Ncells = len(cells)
	hordarg = np.argsort(hcelulas)[::-1]		# Array com endereco das celulas ordenadas em ordem decrescente
	
	Flows_dir = np.zeros(Ncells)
	Minimum_address = [-1]
	Sorver_address = [-1]
	
	count1 = 0
	
	while count1 < Ncells:
		
		count2 = 0
		
		cell_ad = hordarg[count1]
		cell_neigh = cellsneighbor[cell_ad]
		
		hvar = hcelulas[cell_ad]
		hneigh = -1
		cell_flow = -1
		
		if sorvtype[cell_ad] != 1:				# Apenas borda tipo 1 sorvedoura
		
			while count2 < 6:				# Compara a altura dos vizinhos da celula e da propria celula
				
				if cell_neigh[count2] != -1:
					
					hneigh = hcelulas[cell_neigh[count2]]
					
					if hneigh < hvar:
						
						cell_flow = cell_neigh[count2]
						
						hvar = hneigh
		
				count2 += 1
				
			if cell_flow != -1:
				
				Flows_dir[cell_ad] = cell_flow
				
			else:
				
				Minimum_address = np.append(Minimum_address, cell_ad)
				Flows_dir[cell_ad] = -1							# -1, Minimo local
				
		else:
			
			Flows_dir[cell_ad]=-2							# -2, Borda sorvedora
			Sorver_address = np.append(Sorver_address, cell_ad)
			
		
		count1 += 1
	
	
	Minimum_address = np.delete(Minimum_address,0)
	Sorver_address = np.delete(Sorver_address,0)
	
	return (Flows_dir, Minimum_address, Sorver_address, hordarg)