# Function to find the neighborhood adress of each Hexagonal cell

import numpy as np

def Hex_neighbo (cells, edgetype, Nxhex):
	
	Ncells = len(cells)
	
	count1 = 1
	
	cells_neighbo = [[0,0,0,0,0,0]]*Ncells
	cells_neighbo = np.array(cells_neighbo)
	cells_neighbo[0] = [count1, Nxhex, -1, -1, -1, -1]
	
	while count1 < Ncells:
		
		if edgetype[count1] == 2:		# Tipo 2, faixa base
			
			cells_neighbo[count1] = [count1-1, count1+1, count1 + Nxhex, count1 + Nxhex -1 , -1, -1]
			
		
		if edgetype[count1] == 3:		# Tipo 3, ponta direita base
			
			cells_neighbo[count1] = [count1-1, count1 + Nxhex, count1 + Nxhex -1 , -1, -1, -1]
			
			
		if edgetype[count1] == 4:		# Tipo 4, faixa esquerda dentro
			
			cells_neighbo[count1] = [count1 - Nxhex, count1 - Nxhex + 1, count1 + 1 , count1 + Nxhex, count1 + Nxhex +1, -1]
			
			
		if edgetype[count1] == 11:		# Tipo 11, faixa esquerda fora
			
			cells_neighbo[count1] = [count1 - Nxhex, count1 + 1 , count1 + Nxhex, -1, -1, -1]
			
		
		if edgetype[count1] == 0:		# Tipo 0, internas dentro
			
			cells_neighbo[count1] = [count1 - Nxhex, count1 - Nxhex + 1 , count1 -1, count1 + 1, count1 + Nxhex, count1 + Nxhex +1]
			
			
		if edgetype[count1] == 13:		# Tipo 13, internas fora
		
			cells_neighbo[count1] = [count1 - Nxhex, count1 - Nxhex - 1 , count1 -1, count1 + 1, count1 + Nxhex, count1 + Nxhex -1]
			
			
		if edgetype[count1] == 5:		# Tipo 5, faixa direita fora
		
			cells_neighbo[count1] = [count1 - Nxhex, count1 - Nxhex - 1 , count1 -1, count1 + Nxhex, count1 + Nxhex -1, -1]
			
			
		if edgetype[count1] == 12:		# Tipo 12, faixa direita dentro
		
			cells_neighbo[count1] = [count1 - Nxhex , count1 -1, count1 + Nxhex, -1,-1,-1]
			
			
		if edgetype[count1] == 6:		# Tipo 6, ponta esquerda topo fora
			
			cells_neighbo[count1] = [count1 - Nxhex , count1 +1, -1, -1,-1,-1]
			
			
		if edgetype[count1] == 7:		# Tipo 7, ponta esquerda topo dentro
		
			cells_neighbo[count1] = [count1 - Nxhex , count1 - Nxhex +1, count1 +1, -1,-1,-1]
			
		if edgetype[count1] == 8:		# Tipo 8, faixa topo dentro
		
			cells_neighbo[count1] = [count1 - Nxhex , count1 - Nxhex +1, count1 +1, count1 - 1,-1,-1]
			
			
		if edgetype[count1] == 14:		# Tipo 14, faixa topo fora
		
			cells_neighbo[count1] = [count1 - Nxhex , count1 - Nxhex -1, count1 +1, count1 - 1,-1,-1]
			
			
		if edgetype[count1] == 9:		# Tipo 9, ponta direita topo fora
		
			cells_neighbo[count1] = [count1 - Nxhex , count1 - Nxhex-1, count1 -1, -1,-1,-1]
			
		if edgetype[count1] == 10:		# Tipo 10, ponta direita topo dentro
		
			cells_neighbo[count1] = [count1 - Nxhex , count1 -1, -1, -1,-1,-1]
			
			
		count1 +=1


	return (cells_neighbo)