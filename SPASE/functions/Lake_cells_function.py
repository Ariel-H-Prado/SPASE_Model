# Funcao para encontrar celulas que serao alagadas

import numpy as np

def Lake_cells_function (cells, hcells, Flow_groups_header_final, Group_flow):
	
	N_cells = len(cells)
	
	Lake_cells = []
	
	Lake_cells_address = []
	
	count1 = 0
	
	while count1 < N_cells:
		
		Grp = int(Group_flow[count1])
		
		if Grp != 1 and Grp != 0 :
			
			H_lake_grp = Flow_groups_header_final[Grp][1]
			
			H_cell = hcells[count1]
			
			if H_cell <= H_lake_grp:
				
				Ad_lake_grp = Flow_groups_header_final[Grp][2]
			
				Lake_cells.append([1,H_lake_grp,Ad_lake_grp])
				Lake_cells_address.append(count1)
				
			else: 
				
				Lake_cells.append([0,0,0])
				
		else:
			
			Lake_cells.append([0,0,0])
			
		
		count1 += 1
	
	
	
	return(Lake_cells, Lake_cells_address)