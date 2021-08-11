# Funcao para corrigir o ad_groups_min para econtrar grupos minimos que ficam em ciclos de mais de dois

import numpy as np
import time


def ad_min_correct_ini (Flow_borders_groups_header1):

	N_groups = len(Flow_borders_groups_header1)
	
	Classifc_corr = N_groups*[0]		# Classificacao de supergrupo o grupo N pertence
	
	Classifc_corr[1] = 1				
	
	Super_groups = [[0],[1]]				# supergrupos com enderecos dos seus grupos
	
	count1 = 2
	
	
	while count1 < N_groups:
	
		temp1 = Classifc_corr[count1]
		
		Classifc_corr_temp = N_groups*[0]
		
		Classifc_corr_temp[1] = 1
		
		if temp1 == 0:
		
			[Classifc_corr, Super_groups] = Func_ad_min_ini (Flow_borders_groups_header1, Classifc_corr, Super_groups, Classifc_corr_temp, count1)
		
		count1 += 1
	
	return (Classifc_corr, Super_groups)
	
	
	

def Func_ad_min_ini (Flow_borders_groups_header1, Classifc_corr, Super_groups, Classifc_corr_temp, N):
	
	count_g = N
	
	Classifc_corr_temp[N] = 2		#  Lista temporaria para verificacao de ciclo de grupos, PARA VERIFICAR SE O SUPERGRUPO ANALISADO E SORVEDOURO OU NAO
	
	count2 = 0						# Flag para sair do loop
	
	ad_new_group = [N]				# endereco dos grupos novos no supergrupo
	
	while count2 == 0 :
		
		
		Next_group = int(Flow_borders_groups_header1[count_g][3])
		
		temp2 = Classifc_corr[Next_group]
		
		
		if temp2 != 0 or Classifc_corr_temp[Next_group] != 0 :
			
			if temp2 != 0 :
				
				new_size = len(ad_new_group)
				
				count4 = 0
				
				while count4 < new_size:
					
					Super_groups[temp2].append(ad_new_group[count4])
					
					Classifc_corr[ad_new_group[count4]] = temp2
					
					count4 += 1
				
			else:
				
				num_super = len(Super_groups)
				
				temp3 = num_super 
				
				Super_groups.append([])
				
				new_size = len(ad_new_group)
				
				count4 = 0
				
				while count4 < new_size:
					
					Super_groups[temp3].append(ad_new_group[count4])
					
					Classifc_corr[ad_new_group[count4]] = temp3
					
					count4 += 1
				
			count2 = 1
			
		else :
			
			ad_new_group.append(Next_group)			# endereco dos grupos novos no supergrupo
			
			Classifc_corr_temp[Next_group] = 2		#	SE O NEXT_GROUP PARA O PROXIMO COUNT_G JA TIVER A FLAG 2 E UM SUPERGRUPO QUE NAO E SORVEDOURO
			
			count_g = Next_group
		
	return(Classifc_corr, Super_groups)



##################################################################### Dentro da Recursao

def ad_min_correct_rec (Flow_borders_groups_header1, Gflow):

	N_groups = len(Flow_borders_groups_header1)
	
	Classifc_corr = N_groups*[0]		# Classificacao de supergrupo o grupo N pertence
	
	Classifc_corr[1] = 1				
	
	Super_groups = [[0],[1]]				# supergrupos com enderecos dos seus grupos
	
	count1 = 2
	
	
	while count1 < N_groups:
	
		temp1 = Classifc_corr[count1]
		
		Classifc_corr_temp = N_groups*[0]
		
		Classifc_corr_temp[1] = 1
		
		if temp1 == 0:
		
			[Classifc_corr, Super_groups] = Func_ad_min_rec (Flow_borders_groups_header1, Classifc_corr, Super_groups, Classifc_corr_temp, count1, Gflow)
		
		count1 += 1
	
	return (Classifc_corr, Super_groups)
	
	
	

def Func_ad_min_rec (Flow_borders_groups_header1, Classifc_corr, Super_groups, Classifc_corr_temp, N, Gflow):
	
	count_g = N
	
	Classifc_corr_temp[N] = 2		#  Lista temporaria para verificacao de ciclo de grupos, PARA VERIFICAR SE O SUPERGRUPO ANALISADO E SORVEDOURO OU NAO
	
	count2 = 0						# Flag para sair do loop
	
	ad_new_group = [N]				# endereco dos grupos novos no supergrupo
	
	while count2 == 0 :
		
		
		Next_group = int(Gflow[Flow_borders_groups_header1[count_g][2]])
		
		temp2 = Classifc_corr[Next_group]
		
		
		if temp2 != 0 or Classifc_corr_temp[Next_group] != 0 :
			
			if temp2 != 0 :
				
				new_size = len(ad_new_group)
				
				count4 = 0
				
				while count4 < new_size:
					
					Super_groups[temp2].append(ad_new_group[count4])
					
					Classifc_corr[ad_new_group[count4]] = temp2
					
					count4 += 1
				
			else:
				
				num_super = len(Super_groups)
				
				temp3 = num_super 
				
				Super_groups.append([])
				
				new_size = len(ad_new_group)
				
				count4 = 0
				
				while count4 < new_size:
					
					Super_groups[temp3].append(ad_new_group[count4])
					
					Classifc_corr[ad_new_group[count4]] = temp3
					
					count4 += 1
				
			count2 = 1
			
		else :
			
			ad_new_group.append(Next_group)			# endereco dos grupos novos no supergrupo
			
			Classifc_corr_temp[Next_group] = 2		#	SE O NEXT_GROUP PARA O PROXIMO COUNT_G JA TIVER A FLAG 2 E UM SUPERGRUPO QUE NAO E SORVEDOURO
			
			count_g = Next_group
		
	return(Classifc_corr, Super_groups)