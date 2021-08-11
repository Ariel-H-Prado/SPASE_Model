# Topography generator simple: Plano inclinado na direcao do sorvedouro para o caso do Rio Jurua

# M , multiplicator random
# M2, inclination coefficient (na coordenada y)
# M3, inclination coefficient (na coordenada x)

import numpy as np

def Topo_gen1 (cells, M, M2, M3, hmin):

	npoints = len(cells)
	
	hcells = [[0]]*npoints
	
	count1 = 0
	
	h = 0
	
	while count1 < npoints:
		
		h = M*np.random.random_sample() + M2*cells[count1][1] + M3*cells[count1][0] + hmin
		
		hcells[count1] = h
		
		count1 +=1
	
	return (hcells)
	
