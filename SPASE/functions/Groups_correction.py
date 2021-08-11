# Rotina para corrigir o problema de dois grupos escoarem entre si
# Cabecalho final: [Grupo primario, nivel que sera alagado, endereco da borda destino]	

import numpy as np
import copy
from Ad_min_Groups_correction import *
import time


def Group_correction (Flow_borders_groups_header1, Group_Borders, Group_Borders_neighbor, Group_flow, hcells, H_Group_Borders, H_Group_Borders_neighbor):
	
	N_groups = len(Group_Borders)
	
	count1 = 2
	
	
	[Classifc, Super_groups] = ad_min_correct_ini(Flow_borders_groups_header1) # Funcao para classifcar qual supergrupo cada grupo pertence
	
	
	Classifc1 = []
	Super_groups1 = []
	
	Flow_groups_header_final = copy.deepcopy(Flow_borders_groups_header1)
	
	
	
	[Flow_groups_header_final, Classifc, Super_groups] = Recurssive_routine_Group(Flow_groups_header_final, Group_Borders, Group_Borders_neighbor, Group_flow, hcells, H_Group_Borders, H_Group_Borders_neighbor, Classifc, Super_groups)

	
	return (Flow_groups_header_final)

# Funcao recursiva para gerar header final corrigido	

def Recurssive_routine_Group(Flow_groups_header_final, Group_Borders, Group_Borders_neighbor, Group_flow, hcells, H_Group_Borders, H_Group_Borders_neighbor, Classifc, Super_groups):
	
	
	N_groups = len(Flow_groups_header_final)
	
	N_min = len(Super_groups)			# Numero de supergrupos
	
	if N_min == 2:								# Se nao possui minimo de supergrupo alem do sorvedouro sai do loop
	
		return(Flow_groups_header_final, Classifc, Super_groups)
	
	Group_Borders2 = [[]]				# Variavel para armazenar novas bordas de supergrupo
	Group_Borders_neighbor2 = [[]]		# vizinhos dos supergrupos
	H_Group_Borders2 = [[]]
	H_Group_Borders_neighbor2 = [[]]
	
	count_groups = len(Group_Borders)	# Numero de grupos (Inferiores a supergrupos, e um numero maior que o de supergrupos)
	
	count1 = 1
	
	# Conjunto de lacos para encontrar a nova borda de cada supergrupo e os vizinhos de cada celula dessa borda
	# Armazena os enderecos e alturas das bordas e vizinhos das bordas do novo supergrupo
	
	while count1 < N_min:
		
		temp_gb1 = []
		temp_gb1_neighbor= []
		temp_gb1_H = []
		temp_gb1_H_neighbor = []
		
		count2 = 1
		
		while count2 < count_groups:
			
			Super_atual = Classifc[int(Group_flow[Group_Borders[count2][0]])]
			
			if Super_atual == count1:			# Ainda esta errado
				
				N_bord_g = len(Group_Borders[count2])
			
				count4 = 0
			
				while count4 < N_bord_g:
				
					N_bord_neigh = len(Group_Borders_neighbor[count2][count4])
					
					Adr_Bord = Group_Borders[count2][count4]
					
					temp_ad1 = []
					temp_ad1_h =[]
					
					flag1 = 0
					
					count5 = 0
					
					while count5 < N_bord_neigh:
						
						Adr_neigh_bor = Group_Borders_neighbor[count2][count4][count5]
						
						N_g_neigh = int(Group_flow[Adr_neigh_bor])
						
						New_group_N = Classifc[N_g_neigh]
						
						if New_group_N != count1 and ((Adr_Bord in temp_gb1) != True):		
							
							flag1 = 1
							
							temp_ad1.append(Adr_neigh_bor)
							temp_ad1_h.append(H_Group_Borders_neighbor[count2][count4][count5])
							
						count5 += 1
				
					if flag1 == 1:
						
						temp_gb1.append(Group_Borders[count2][count4])
						temp_gb1_H.append(H_Group_Borders[count2][count4])
						temp_gb1_neighbor.append(temp_ad1)
						temp_gb1_H_neighbor.append(temp_ad1_h)
						
					
					count4 += 1
			
			count2 += 1
		
		Group_Borders2.append(temp_gb1)
		H_Group_Borders2.append(temp_gb1_H)
		Group_Borders_neighbor2.append(temp_gb1_neighbor)
		H_Group_Borders_neighbor2.append(temp_gb1_H_neighbor)
		
		count1 += 1
	
	
	
	# Loop para encontrar a celula de escoamento de cada supergrupo
	
	Count_GB2 = len(Group_Borders2)
	
	New_level_flow = [0,0]				# lista com o nivel de escoamento do supergrupo [N]
	New_level_flow_ad = [0,0]			# lista com o endereco do nivel de escoamento do supergrupo [N]
	group_next_flow = [0,-1]
	count1 = 2
	
	while count1 < Count_GB2:
		
		N_border_cell2 = len(Group_Borders2[count1])
		
		H_border2 = H_Group_Borders2[count1]
		
		G_border2 = Group_Borders2[count1]
		
		Ord_ad_h2 = np.argsort(H_border2)					# endereco ordenado das celulas bordas do grupo count1
		
		Smaller_Neigbor = []							# Altura do menor vizinho da borda  NOVO
		Smaller_Neigbor_ad = []							# Endereco do menor vizinho da borda NOVO
		
		count2 = 0
		
		while count2 < N_border_cell2:
			
			temp1 = Ord_ad_h2[count2]
			
			H_neighbor2 = H_Group_Borders_neighbor2[count1][temp1]			# Altura dos vizinhos da celula borda
			
			Ord_ad_h_neighbor2 = np.argsort(H_neighbor2)						# Endereco da altura dos vizinhos ordenados, ordem crescente
			
			H_smaller_neighbor2 = H_Group_Borders_neighbor2[count1][temp1][Ord_ad_h_neighbor2[0]]
			
			Ad_smaller_neighbor2 = Group_Borders_neighbor2[count1][temp1][Ord_ad_h_neighbor2[0]]
			
			
			if count2 + 1 < N_border_cell2:
			
				H_next_board = H_Group_Borders2[count1][Ord_ad_h2[count2+1]]
				
			else:
				
				H_next_board = H_smaller_neighbor2
				
			if count2 == 0:	# NOVO
				
				Smaller_Neigbor = H_smaller_neighbor2							# Altura do menor vizinho da borda  NOVO
				Smaller_Neigbor_ad = Ad_smaller_neighbor2						# Endereco do menor vizinho da borda NOVO
				
			elif Smaller_Neigbor > H_smaller_neighbor2 and H_smaller_neighbor2 > H_Group_Borders2[count1][Ord_ad_h2[count2]]:
				
				Smaller_Neigbor = H_smaller_neighbor2							# Altura do menor vizinho da borda  NOVO
				Smaller_Neigbor_ad = Ad_smaller_neighbor2						# Endereco do menor vizinho da borda NOVO
			
			
			if H_smaller_neighbor2 <= H_next_board and  H_smaller_neighbor2 <= Smaller_Neigbor:
				
				group_next_flow1 = Classifc[int(Group_flow[Ad_smaller_neighbor2])]			# Fala para qual proximo supergrupo ira escoar
				group_next_flow.append(group_next_flow1)
				
				h1 = H_border2[Ord_ad_h2[count2]]
				
				a1 = G_border2[Ord_ad_h2[count2]]
				
				h2 = H_smaller_neighbor2
				
				a2 = Ad_smaller_neighbor2
				
				if h1 <= h2:				# altura do nivel de escoamento eh a maior
					
					hg = h2					# hg, novo nivel de escoamento
					ag = a2					# ag, endereco da celula de escoamento
					
				else:
					
					hg = h1
					ag = a2
				
				
				New_level_flow.append(hg)
				New_level_flow_ad.append(ag)
				
				count2 = N_border_cell2
			
			if H_smaller_neighbor2 > Smaller_Neigbor and Smaller_Neigbor <= H_next_board: # NOVO if para caso em menor vizinho da celula borda atual eh maior que o menor vizinho de celular anteriores
				
				group_next_flow1 = Classifc[int(Group_flow[Smaller_Neigbor_ad])]			# Fala para qual proximo supergrupo ira escoar
				group_next_flow.append(group_next_flow1)
				
				h1 = H_border2[Ord_ad_h2[count2]]
				
				a1 = G_border2[Ord_ad_h2[count2]]
				
				h2 = Smaller_Neigbor
				
				a2 = Smaller_Neigbor_ad
				
				if h1 <= h2:				# altura do nivel de escoamento eh a maior
					
					hg = h2					# hg, novo nivel de escoamento
					ag = a2					# ag, endereco da celula de escoamento
					
				else:
					
					hg = h1
					ag = a2
				
				
				New_level_flow.append(hg)
				New_level_flow_ad.append(ag)
				
				count2 = N_border_cell2
			
			
			count2 += 1
			
		count1 += 1
	
	
	count1 = 2
	
	
	while count1 < N_groups:									# while para atualizar qual supergrupo vai escoar no cabecalho final
		
		temp_next = group_next_flow[Classifc[count1]]
		
		if temp_next == -1:
			
			temp_next = 1
		
		Flow_groups_header_final[count1][3] = temp_next			
		
		count1 += 1
	
	
	# Atualizar header final antes de chamar recursao novamente, atualizar se nivel de alagamento do grupo for menor que o nivel do supergrupo.
	
	count1 = 2
	
	while count1 < N_groups:
		
		if Classifc[count1] != 1 and Classifc[count1] != 0:
			
			Supergroup_number = Classifc[count1]
			
			Lake_level_S = New_level_flow[Supergroup_number]
			
			Lake_level_group = Flow_groups_header_final[count1][1]
			
			if Lake_level_group <= Lake_level_S:
				
				Flow_groups_header_final[count1][1] = Lake_level_S
				Flow_groups_header_final[count1][2] = New_level_flow_ad[Supergroup_number]
		
		count1 += 1
	
	# Atualizar Classifc
	
	[Classifc, Super_groups] = ad_min_correct_rec(Flow_groups_header_final, Group_flow)
	
	[Flow_groups_header_final, Classifc, Super_groups] = Recurssive_routine_Group(Flow_groups_header_final, Group_Borders2, Group_Borders_neighbor2, Group_flow, hcells, H_Group_Borders2, H_Group_Borders_neighbor2, Classifc, Super_groups)
	
	return(Flow_groups_header_final, Classifc, Super_groups)

	
