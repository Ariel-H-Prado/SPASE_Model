# Funcao para determinar qual grupo de sorvedouro uma celula pertence, 1 para sorvedouro de borda, N !=1 para minimo local.

import numpy as np

def Flow_group_sorv (Flow_dir, Minimum_address, Sorver_address, cells_neighbor, cells):
	
	Ncells = len(cells)							# Numero total de celulas
	
	Group_flow = np.zeros(Ncells)				# Array com classificacao do grupo de escoamento
	
	n_sorv = len(Sorver_address)				# quantidade de celulas sorvedouro
	
	n_min = len(Minimum_address)				# quantidade de minimos locais
	
	count1 = 0
	
	while count1 < n_sorv:						# Loop para todas as celulas sorvedouras
		
		S_ad = Sorver_address[count1]			# endereco da celular sorvedoura atual
		
		Group_flow[S_ad] = 1					# Celula sorvedoura pertence a grupo 1
		
		Ne_ad = cells_neighbor[S_ad]
		
		count3 = 0								# 
		
		while count3 < 6:						# Loop para verificar vizinhos de celula sorvedoura	
			
			
			if Ne_ad[count3] != -1:		# Condicional para verificar vizinho
				
				NCell_ad = Ne_ad[count3]	# endereco da celula vizinha
				
				if Flow_dir[NCell_ad] == S_ad:	# condicional para verificar se celula vizinha escoa para sorvedouro
					
					Group_flow[NCell_ad] = 1
					
					Group_flow = Flow_group_recur(Group_flow, NCell_ad, 1, cells_neighbor, Flow_dir)		# FUNCAO RECURSIVA PARA BUSCAR GRUPO PERTECENCENTE AO SORVEDOURO
		
		
			count3 += 1
		
		count1 += 1
	
	
	
	count2 = 0
	
	# Loop para encontrar grupos de minimos locais
	
	Min_group = 2
	
	while count2 < n_min:
		
		M_ad = Minimum_address[count2]			# endereco da celular sorvedoura atual
		
		Group_flow[M_ad] = Min_group					# Celula sorvedoura pertence a grupo 1
		
		Ne_ad = cells_neighbor[M_ad]
		
		count6 = 0								# 
		
		while count6 < 6:						# Loop para verificar vizinhos de celula sorvedoura	
			
			
			if Ne_ad[count6] != -1:		# Condicional para verificar vizinho
				
				NCell_ad = Ne_ad[count6]	# endereco da celula vizinha
				
				if Flow_dir[NCell_ad] == M_ad:	# condicional para verificar se celula vizinha escoa para sorvedouro
					
					Group_flow[NCell_ad] = Min_group
					
					Group_flow = Flow_group_recur(Group_flow, NCell_ad, Min_group, cells_neighbor, Flow_dir)		# FUNCAO RECURSIVA PARA BUSCAR GRUPO PERTECENCENTE AO SORVEDOURO
		
		
			count6 += 1
		
		Min_group += 1
		count2 += 1
	
	
	return (Group_flow)
	
	
def Flow_group_recur (Group_flow, NCell_ad, ntype, cells_neighbor, Flow_dir):
	
	count5 = 0
	
	Ne_ad = cells_neighbor[NCell_ad]
	
	while count5 < 6:
		
		
		if Ne_ad[count5] != -1:
			
			NCell_ad2 = Ne_ad[count5]
			
			if Flow_dir[NCell_ad2] == NCell_ad:
			
				Group_flow[NCell_ad2] = ntype
				
				Group_flow = Flow_group_recur(Group_flow, NCell_ad2, ntype, cells_neighbor, Flow_dir)
				
		count5 += 1
	
	
	return(Group_flow)







	