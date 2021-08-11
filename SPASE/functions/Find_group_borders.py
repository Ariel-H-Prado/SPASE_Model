# Encontrar as celulas fronteiras de cada grupo de minimo local e sorvedouro
# Group_borders retorna os enderecos das celulas bordas de cada grupo onde Group_borders[1] represente os enderecos das 
#  bordas do sorvedouro, Group_borders[N] do grupo de minimo local N 


import numpy as np

def Find_borders (Group_flow, Flow_dir, cells, Minimum_address, cells_neighbor, hcells):
	
	N_cells = len(cells)
	
	N_groups = len(Minimum_address) + 2

	Group_borders = []
	
	Group_borders_neighbor = []
	
	H_Group_Borders = []
	
	H_Group_Borders_neighbor = []
	
	count1 = 0
	
	while count1 < N_groups:
		
		Group_borders.append([])
		Group_borders_neighbor.append([])
		H_Group_Borders.append([])
		H_Group_Borders_neighbor.append([])
		
		count1 += 1
	
	count1 = 0
	
	while count1 < N_cells:
		
		g_cell = Group_flow[count1]
		
		g_cell2 = int(g_cell)
		
		ad_n_cell = cells_neighbor[count1]
		
		cond1 = 0 			# Condicional para verificar se borda
		
		count2 = 0
		
		temp1 = []
		temp2 = []
		
		while count2 < 6:
			
			if ad_n_cell[count2] != -1:
				
				if Group_flow[ad_n_cell[count2]] != g_cell:
					
					temp1.append(ad_n_cell[count2])
					temp2.append(hcells[ad_n_cell[count2]])
					
					cond1 = 1
					
			
			count2 += 1
			
		if cond1 == 1:
			
			Group_borders[g_cell2].append(count1)
			
			Group_borders_neighbor[g_cell2].append(temp1)
			
			H_Group_Borders[g_cell2].append(hcells[count1])
			
			H_Group_Borders_neighbor[g_cell2].append(temp2)
			
			
		count1 += 1
	
	return (Group_borders, Group_borders_neighbor, H_Group_Borders, H_Group_Borders_neighbor)