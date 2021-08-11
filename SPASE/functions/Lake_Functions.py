# Drainage Lakes Function

import numpy as np

# Drainage in Lakes

def Drainage_Lake_Func(hcells, Lake_cells_address, Lake_cells, hzero, cells_neighbor, 
				   Discharge_cells, pluvCell, dt, AreaHex, Lhex, Espx, hplan, Aplan):
	
	count1 = 0
	
	while count1 < len(Lake_cells_address):			
		
		Adr_cell = Lake_cells_address[count1]
		
			
		if hcells[Adr_cell] != hplan[Adr_cell] and Lake_cells[Adr_cell][1] >= hcells[Adr_cell]:  # Lake cells leveling
			
			# New Hcell
			htemp_lake = (AreaHex - Aplan[Adr_cell]) * (hcells[Adr_cell]-hplan[Adr_cell])/AreaHex + hplan[Adr_cell]
			
			hcells[Adr_cell] = htemp_lake
			
			hplan[Adr_cell] = hcells[Adr_cell]
			
			Aplan[Adr_cell] = AreaHex
		
		Adr_overflow = Lake_cells[Adr_cell][2]
			
		Discharge_cells[Lake_cells_address[count1]] += pluvCell
		
		Discharge_cells[Adr_overflow] += Discharge_cells[Lake_cells_address[count1]]
		
		
		# Lake flows to lake case
		
		if Lake_cells[Adr_overflow][0] == 1:
			
			flag = 0
		
			while flag == 0:
			
				Next_Adr2 = Lake_cells[Adr_overflow][2]
			
				Discharge_cells[Next_Adr2] += Discharge_cells[Lake_cells_address[count1]]
				
				Adr_overflow = Next_Adr2
			
				if Lake_cells[Adr_overflow][0] == 0:
					
					flag = 1
				
		count1 += 1
	
	return(hcells, hplan, Aplan, Discharge_cells)

#######################################################

