# Cria um cabecalho de cada grupo de minimo local que e inundado ate a celula borda que escoa para outro grupo
# Cabecalho: [grupo que pertence, h borda , endereco da borda, grupo que vai escoar]


import numpy as np

def Header_borders_flow (Group_Borders, Group_Borders_neighbor, hcells,  Group_flow, H_Group_Borders, H_Group_Borders_neighbor):
	
	N_groups = len(Group_Borders)
	
	Flow_borders_groups_header = [[],[1]]
	
	count1 = 2
	
	while count1 < N_groups:
		
		N_border_cell = len(Group_Borders[count1])
		
		H_border = H_Group_Borders[count1]
		
		G_border = Group_Borders[count1]
		
		Ord_ad_h = np.argsort(H_border)					# endereco ordenado das menores alturas para maiores alturas das celulas bordas do grupo count1
		
		Smaller_Neigbor = []							# Altura do menor vizinho da borda  NOVO
		Smaller_Neigbor_ad = []							# Endereco do menor vizinho da borda NOVO
		
		count2 = 0
		
		while count2 < N_border_cell:
			
			temp1 = Ord_ad_h[count2]
			
			H_neighbor = H_Group_Borders_neighbor[count1][temp1]			# Altura dos vizinhos da celula borda
			
			Ord_ad_h_neighbor = np.argsort(H_neighbor)						# Endereco da altura dos vizinhos ordenados, ordem crescente
			
			H_smaller_neighbor = H_Group_Borders_neighbor[count1][temp1][Ord_ad_h_neighbor[0]]
			
			Ad_smaller_neighbor = Group_Borders_neighbor[count1][temp1][Ord_ad_h_neighbor[0]]
			

			if count2 + 1 < N_border_cell:									# Verificar proxima menor altura 
			
				H_next_board = H_Group_Borders[count1][Ord_ad_h[count2+1]]
				
			else:
				
				H_next_board = H_smaller_neighbor
				
			if count2 == 0:	# NOVO
				
				Smaller_Neigbor = H_smaller_neighbor							# Altura do menor vizinho da borda  NOVO
				Smaller_Neigbor_ad = Ad_smaller_neighbor						# Endereco do menor vizinho da borda NOVO
				
			elif Smaller_Neigbor > H_smaller_neighbor and H_smaller_neighbor > H_Group_Borders[count1][Ord_ad_h[count2]]:
				
				Smaller_Neigbor = H_smaller_neighbor							# Altura do menor vizinho da borda  NOVO
				Smaller_Neigbor_ad = Ad_smaller_neighbor						# Endereco do menor vizinho da borda NOVO
			
			
			if H_smaller_neighbor <= H_next_board and H_smaller_neighbor <= Smaller_Neigbor :
				
				group_next_flow = Group_flow[Ad_smaller_neighbor]
				
				h1 = H_border[Ord_ad_h[count2]]
				
				a1 = G_border[Ord_ad_h[count2]]
				
				h2 = H_smaller_neighbor
				
				a2 = Ad_smaller_neighbor
				
				if h1 <= h2:				# altura do nivel de escoamento e a maior
					
					hg = h2
					ag = a2
					
				else:
					
					hg = h1
					ag = a2
				
				Flow_borders_groups_header.append([count1, hg, ag, group_next_flow])
				
				count2 = N_border_cell
				
			if H_smaller_neighbor > Smaller_Neigbor and Smaller_Neigbor <= H_next_board: # NOVO if para caso em menor vizinho da celula borda atual eh maior que o menor vizinho de celular anteriores
				
				group_next_flow = Group_flow[Smaller_Neigbor_ad]
				
				h1 = H_border[Ord_ad_h[count2]]
				
				a1 = G_border[Ord_ad_h[count2]]
				
				h2 = Smaller_Neigbor
				
				a2 = Smaller_Neigbor_ad
				
				if h1 <= h2:				# altura do nivel de escoamento e a maior
					
					hg = h2
					ag = a2
					
				else:
					
					hg = h1
					ag = a2
				
				Flow_borders_groups_header.append([count1, hg, ag, group_next_flow])
				
				count2 = N_border_cell
			
			count2 += 1
		
		
		count1 += 1
	
	return (Flow_borders_groups_header)

	
