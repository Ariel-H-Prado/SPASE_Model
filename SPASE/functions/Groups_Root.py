# Programa raiz para encontrar os grupos de escoamento e lagos (pontos de minimo)
# Saida: Array com informacoes se a celula do enderco eh alagada (0 se nao. 1 se sim). Se sim tem a altura no nivel alagado e o enderaco da celula de escoamento

from Group_flow_min_sorv import *
from Find_group_borders import *
from Header_group_flow import *
from Groups_correction import *
from Lake_cells_function import *
from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
import time


def Groups_Root(Flow_dir, Minimum_address, Sorver_address, cells_neighbor, cells, hcells):
	
	# Determinar quais celulas escoam para minimo local (grupos N), ou celulas sorvedoras (grupo 1)


	Group_flow = Flow_group_sorv(Flow_dir, Minimum_address, Sorver_address, cells_neighbor, cells)

	

	# Encontrar os enderecos das celulas bordas dos grupos de minimos locais e sorvedouro


	[Group_Borders, Group_Borders_neighbor, H_Group_Borders, H_Group_Borders_neighbor] = Find_borders(Group_flow, Flow_dir, cells, Minimum_address, cells_neighbor, hcells)

	# Encontrar celulas de borda de grupo que escoam para outro grupo


	Flow_borders_groups_header = Header_borders_flow (Group_Borders, Group_Borders_neighbor, hcells, Group_flow, H_Group_Borders, H_Group_Borders_neighbor)



	# Rotina para ajustar os casos em que um grupo escoa para o outro reciprocamente, formando supergrupos que nao escoam para sorvedouro


	Flow_groups_header_final = Group_correction(Flow_borders_groups_header, Group_Borders, Group_Borders_neighbor, Group_flow, hcells, H_Group_Borders, H_Group_Borders_neighbor)


	# Rotina para gerar lista com flag para cada celula, 0 se nao alagar, 1 se alagar. (1, nivel de alagamento, endereco da celula borda para escoar)


	[Lake_cells, Lake_cells_address] = Lake_cells_function (cells, hcells, Flow_groups_header_final, Group_flow)

	
	return (Lake_cells, Lake_cells_address)