# Funcoes de debug

import numpy as np


def Debug_Discharge(hplan, Decr_Adress_Cells, Lake_cells, pluvCell, Flow_dir, Extern_River,dt, sorvtype, Lake_cells_address):
	
	secpyear = 60.*60.*24.*365.2564					# Segundos em um ano
	
	N_cells = len(hplan)
	
	
	Discharge = np.zeros(N_cells)
	
	Discharge[Extern_River[0]] = Extern_River[1]			# Rio externo 1 (Rio Solimoes)
	Discharge[Extern_River[2]] = Extern_River[3]		# Rio externo 2 (Rio Jurua)
	
	count_lake = 0
	
	N_lakes = len(Lake_cells_address)
	
	while count_lake < N_lakes:
		
		actual_lake = Lake_cells_address[count_lake]
		
		Discharge[actual_lake] += pluvCell
		
		Next_Adr = Lake_cells[actual_lake][2]
		
		if Lake_cells[Next_Adr][0] == 0:
			
			Discharge[Next_Adr] += Discharge[actual_lake]
			
			count_lake += 1
			
			continue
		
		Discharge[Next_Adr] += Discharge[actual_lake]
		
		flag = 0
		
		while flag == 0:
				
			Next_Adr2 = Lake_cells[Next_Adr][2]
				
			Discharge[Next_Adr2] += Discharge[actual_lake]
				
			Next_Adr = Next_Adr2
				
			if Lake_cells[Next_Adr][0] == 0:
					
				flag = 1
		
		
		count_lake += 1
	
	
	count1 = 0
	
	while count1 < N_cells:
		
		actual_cell = Decr_Adress_Cells[count1]
		
		Discharge[actual_cell] += pluvCell
		
		if sorvtype[actual_cell] == 1 or Lake_cells[actual_cell][0] == 1:
			
			count1 += 1
			
			continue
		
		if Lake_cells[int(Flow_dir[actual_cell])][0] == 0:
			
			Discharge[int(Flow_dir[actual_cell])] += Discharge[actual_cell]
			
			count1 += 1
			
			continue
		
		Discharge[Lake_cells[int(Flow_dir[actual_cell])][2]] += Discharge[actual_cell]
		
		Next_Adr = Lake_cells[int(Flow_dir[actual_cell])][2]
		
		if Lake_cells[Next_Adr][0] == 1:
			
			flag = 0
			
			while flag == 0:
				
				Next_Adr2 = Lake_cells[Next_Adr][2]
				
				Discharge[Next_Adr2] += Discharge[actual_cell]
				
				Next_Adr = Next_Adr2
				
				if Lake_cells[Next_Adr][0] == 0:
					
					flag = 1
		
		
		count1 += 1
	
	return(Discharge)