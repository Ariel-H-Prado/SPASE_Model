#Stream Power Functions

import numpy as np
from Function_Width_Channel import *
from Lateral_Erosion_Functions import *

# Funcao para calcular se canal deposita ou erode e ajudaste de alturas de celulas
def Transport_Equation(Qeqb, Qcelula, hcelula, hplanicie, Aplanicie, Acanal, AreaHex, Lf, Espx):
	
	dhcell = hcelula - hplanicie
	
	htemp = hcelula
	
	# Caso em que ocorre deposicao
	if Qeqb < Qcelula:
		
		# Deposicao em celula que nao possui vale
		if dhcell == 0:
			
			Area = AreaHex
			
			htemp += (Qcelula - Qeqb) / AreaHex
			
			hplantemp = htemp
			
			Qtemp1 = Qeqb
			
			Aplantemp = AreaHex
		
		# Deposicao em celula que possui vale
		else:
			
			dh = (Qcelula - Qeqb) / Aplanicie
			
			Vol = dh * Aplanicie
			
			# Caso que planicie e totalmente preenchida
			if dh > dhcell:
				
				Volplan = dhcell * Aplanicie
				
				Voltemp = Vol - Volplan
				
				dhtotal = Voltemp / AreaHex
				
				htemp += dhtotal
				
				hplantemp = htemp
				
				Qtemp1 = Qeqb
				
				Aplantemp = AreaHex
				
			# Caso em que planicie nao e totalmente preenchida	
			else:
				
				hplantemp = hplanicie + dh
				
				Aplantemp = Aplanicie
				
				Qtemp1 = Qeqb
			
	# Caso em que ocorre erosao			
	elif Qeqb > Qcelula:
		
		hplantemp = hplanicie + (Qcelula - Qeqb) * Espx / (Acanal * Lf)
		
		#Verifica se canal nao e do tamanho da celula
		if Acanal < AreaHex:
			
			A2 = Aplanicie - Acanal
		
			A1 = AreaHex - Aplanicie
		
			H1 = dhcell*A1/(A1 + A2)
			
			htemp += H1 - dhcell
			
		else:
			
			htemp = hplantemp
		
		
		
		Aplantemp = Acanal
		
		#if Espx/Lf > 1:
		#	print('Erro')
		
		Qtemp1 = Qcelula + (Qeqb - Qcelula) * Espx / Lf
		
		
		
	# Caso em que nao ocorre nem erosao nem deposicao	
	elif Qeqb == Qcelula:
		
		hplantemp = hplanicie
		
		Qtemp1 = Qeqb
		
		Aplantemp = Aplanicie
		
		
	
	return(Qtemp1, htemp, hplantemp, Aplantemp)

#Funcao Streampower

def Streampower(hcells, hplan, Aplan, AreaHex, Decr_Adress_Cells, Flow_dir, Lake_cells, cells_neighbor, pluvCell,
														 dt, Kf,Lf, LengDiscRiver, sorvtype,Lhex, Espx, Achannel, Discharge_cells, 
															LatCoef1, LatCoef2, secpyear, Q_Extern, Lat_h_coef, m, n):
	
	
	Run_Lakes = 0 			# Controlador para verificar se e nescessario calcular lagos
	
	#hcells_ini = np.copy(hcells)
	
	#hplan_ini = np.copy(hplan)
	
	#Aplan_ini  = np.copy(Aplan)
	
	Ncells = len(hcells)
	
	Qcells = np.zeros(Ncells)
	
	Qeqb_Out = np.zeros(Ncells)
	
	Qdif = np.zeros(Ncells)
	
	########################################
	# Aporte sedimentar dos rios externos
	
	Total_Extern_Sediment = 0
	
	count = 0
	
	while count < len(Q_Extern):
	
		Qcells[Q_Extern[count]] = Q_Extern[count + 1]
		
		Total_Extern_Sediment += Q_Extern[count + 1]
		
		count += 2
	
	
	########################################
	
	count1 = 0
	
	# Verificar conservacao de massa
	
	Vol_ero = 0.0
	Vol_dep = 0.0
	Vol_bord = 0.0
	
	
	while count1 < Ncells:
		
		
		
		actual_cell = Decr_Adress_Cells[count1]
		
		
		# Check if it is a lake cell and if it is flooded or if it is a sink
		if Lake_cells[actual_cell][0] == 1:
			
			h_lake_dep = Qcells[actual_cell]/Aplan[actual_cell]			# It deposits sediment that the current cell receives
				
			Vol_dep += Qcells[actual_cell] # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			
			if h_lake_dep + hplan[actual_cell] < hcells[actual_cell]:
				
				hplan[actual_cell] += h_lake_dep
			
			elif Aplan[actual_cell] == AreaHex:
			
				hcells[actual_cell] += h_lake_dep
			
				hplan[actual_cell] = hcells[actual_cell]
				
			else:
				
				h_lake_dep = (Qcells[actual_cell] - (hcells[actual_cell] - hplan[actual_cell])*Aplan[actual_cell])/AreaHex
				
				hcells[actual_cell] += h_lake_dep
				
				hplan[actual_cell] = hcells[actual_cell]
			
			count1 +=1
			
			continue
		
		if sorvtype[actual_cell] == 1:
			
			Vol_bord += Qcells[actual_cell] 
			
			count1 += 1
				
			continue
		
		# Verfica se e um minimo local que nao esta alagado
		#if Flow_dir[actual_cell] == -1:
			
		#	Run_Lakes = 1
			
		#	hcells = np.copy(hcells_ini)
			
		#	hplan = np.copy(hplan_ini)
			
		#	Aplan = np.copy(Aplan_ini)
			
		#	break
		
		
		Discharge_cells[actual_cell] += pluvCell
		
		# Vizinho de escoamento recebe a descarga do atual
		if Lake_cells[int(Flow_dir[actual_cell])][0] == 0:
			
			Discharge_cells[int(Flow_dir[actual_cell])] += Discharge_cells[actual_cell]
		
		# Se for lago descarga vai para celula de transbordamento
		else:
			
			Adr_overflow = Lake_cells[int(Flow_dir[actual_cell])][2]
			
			Discharge_cells[Adr_overflow] += Discharge_cells[actual_cell]
			
			# Caso lago que escoa em lago
			
			if Lake_cells[Adr_overflow][0] == 1:
				
				flag = 0
		
				while flag == 0:
			
					Next_Adr2 = Lake_cells[Adr_overflow][2]
			
					Discharge_cells[Next_Adr2] += Discharge_cells[actual_cell]
				
					Adr_overflow = Next_Adr2
			
					if Lake_cells[Adr_overflow][0] == 0:
					
						flag = 1
		
		Achannel[actual_cell] = Poly2(Discharge_cells[actual_cell]/(secpyear*dt), LengDiscRiver[0], LengDiscRiver[1])*Espx
		
		# Se area do canal for maior que a celula, recebe a area da celula
		if Achannel[actual_cell] > AreaHex:
			
			Achannel[actual_cell] = AreaHex
		
		
		
		# Verifica se area da planicie eh menor que area do canal e atualizada
		# Se for menor o sedimento para abrir espaco em Aplan eh enviado para o Qcells da celula atual
		if Aplan[actual_cell] < Achannel[actual_cell]:
			
			Q_channel = (Achannel[actual_cell] - Aplan[actual_cell])*(hcells[actual_cell] - hplan[actual_cell])
			
			Qcells[actual_cell] += (Achannel[actual_cell] - Aplan[actual_cell])*(hcells[actual_cell] - hplan[actual_cell]) #!!!!!!!!!!!!
			
			Vol_ero += (Achannel[actual_cell] - Aplan[actual_cell])*(hcells[actual_cell] - hplan[actual_cell]) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			
			Aplan[actual_cell] = Achannel[actual_cell]
		
		
		#######################################################
		
		if Lake_cells[int(Flow_dir[actual_cell])][0] == 1:
			
			h_next = Lake_cells[int(Flow_dir[actual_cell])][1]
			
		else:
			
			h_next = hplan[int(Flow_dir[actual_cell])]
		
		# Stream Power Equation
		
		
		# Maximo de volume de sedimento que a celula atual pode transportar
		Qeqb = Kf * ((Discharge_cells[actual_cell]/(dt*secpyear))**m) * ((hplan[actual_cell] - h_next)**n)/Espx
		
		Qeqb_Out[actual_cell] = Qeqb
		
		
		Qeqb = Qeqb*(secpyear*dt)
		
		if Qeqb < 0:
			#print('Erro')
			#print(actual_cell)
			Qeqb = 0.0
		
		# Erosao Lateral
		
		
		if hcells[actual_cell] > hplan[actual_cell] and (Discharge_cells[actual_cell]/(dt*secpyear)) > 500.0:
			
			# Erosao Lateral dentro da celula
			[Qtemp, Atemp, htemp] = Lateral_Erosion_cell(hcells[actual_cell], hplan[actual_cell], LatCoef1, LatCoef2, AreaHex, Aplan[actual_cell], Achannel[actual_cell], dt, Lat_h_coef, Qeqb)
		
			hcells[actual_cell] = htemp
			
			Aplan[actual_cell] = Atemp
			
			Qcells[actual_cell] += Qtemp
			
			Vol_ero +=  Qtemp  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!
			
			
		if hcells[actual_cell] == hplan[actual_cell] and (Discharge_cells[actual_cell]/(dt*secpyear)) > 500.0:
			
			# Separar vizinhos que sofrem erosao lateral
			
			actneig = cells_neighbor[actual_cell]
			
			neigtemp = []
			
			htemp = []
			
			hplantemp = []
			
			Aplantemp = []
			
			
			count2 = 0
			
			while count2 < 6:
				
				# Verifica se existe vizinho
				if actneig[count2] == -1:
					
					count2 += 1
					
					continue
				
				# Verifica se nao eh celula de escoamento
				if actneig[count2] == int(Flow_dir[actual_cell]):
					
					count2 += 1
					
					continue
				
				# Verifica se nao eh celula mais baixa ( Se for pode causar problemas nos calculos do streampower)
				if hplan[actneig[count2]] <= hplan[actual_cell]:
					
					count2 += 1
					
					continue
				
				# Verifica se celula vizinha nao fornece mais que 0.3 da descarga do canal atual
				if int(Flow_dir[actneig[count2]]) == actual_cell and Discharge_cells[actneig[count2]] > Discharge_cells[actual_cell]*0.3 :
					
					count2 += 1
					
					continue
				
				# Verifica se vizinho nao e lago
				if Lake_cells[actneig[count2]][0] == 1 :
					
					count2 += 1
					
					continue
				
				# Verifica se nao e sorvedouro
				if sorvtype[actneig[count2]] == 1:
					
					count2 += 1
					
					continue
				
				neigtemp.append(actneig[count2])
				
				htemp.append(hcells[actneig[count2]])
				
				hplantemp.append(hplan[actneig[count2]])
				
				Aplantemp.append(Aplan[actneig[count2]])
				
				count2 += 1
			
			if len(neigtemp) > 0:
				
				# Erosao lateral celula Vizinha
				[Qtemp, htemp, hplantemp] = Lateral_Erosion_neig(hcells[actual_cell], htemp, hplantemp, Aplantemp, Achannel[actual_cell], LatCoef1, LatCoef2, AreaHex, dt, Lat_h_coef, Qeqb)
			
				Qcells[actual_cell] += Qtemp
				
				Vol_ero += Qtemp #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				
				
				count2 = 0
			
				while count2 < len(htemp):
					
					hcells[neigtemp[count2]] = htemp[count2] 
				
					hplan[neigtemp[count2]] = hplantemp[count2]
				
					count2 += 1
		
		#######################################################
		
		
		# Stream Power Equation Aplication
		
		
		
		# Application of the transport and erosion equation in the current cell
		[Qtemp, htemp, hplantemp, Aplantemp] = Transport_Equation(Qeqb, Qcells[actual_cell], hcells[actual_cell], hplan[actual_cell], 
																  Aplan[actual_cell], Achannel[actual_cell], AreaHex, Lf, Espx)
		
		Qdif[actual_cell] = Qcells[actual_cell] - Qtemp
		
		if Qtemp > Qcells[actual_cell]:
			
			Vol_ero += Qtemp - Qcells[actual_cell] #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			
			
		if Qtemp < Qcells[actual_cell]:
			
			Vol_dep += Qcells[actual_cell] - Qtemp #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		
		if Lake_cells[int(Flow_dir[actual_cell])][0] == 0:
		
			Qcells[int(Flow_dir[actual_cell])] += Qtemp
		
		hcells[actual_cell] = htemp
		
		hplan[actual_cell] = hplantemp
		
		Aplan[actual_cell] = Aplantemp
		
		
		
		# Checks whether run-off cell is lake to deposit
		if Lake_cells[int(Flow_dir[actual_cell])][0] == 1:
			
			
			lake_depth = Lake_cells[int(Flow_dir[actual_cell])][1] - hplan[int(Flow_dir[actual_cell])]
			
			if lake_depth <= 0:
				
				
				Qcells[Lake_cells[int(Flow_dir[actual_cell])][2]] += Qtemp
				
				count1 += 1
				
				continue
				
			
			flag1 =0
			
			h_lake_dep = Qtemp/Aplan[int(Flow_dir[actual_cell])] + hplan[int(Flow_dir[actual_cell])]
			
			# In which case the flooded cell has a lower level and flatness than the current cell, but when clogged it gets bigger
			
			if hcells[int(Flow_dir[actual_cell])] < hplan[actual_cell] and h_lake_dep > hcells[int(Flow_dir[actual_cell])]:
				
				flag1 = 1
				
				Q_cells = Qtemp - (hcells[int(Flow_dir[actual_cell])] - hplan[int(Flow_dir[actual_cell])])*Aplan[int(Flow_dir[actual_cell])]
				
				h_lake_dep = hcells[int(Flow_dir[actual_cell])] + Q_cells/AreaHex
				
				Aplan[int(Flow_dir[actual_cell])] = AreaHex
				
				if h_lake_dep > hplan[actual_cell]:
					
					Qcells[Lake_cells[int(Flow_dir[actual_cell])][2]] += (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])]
					
					if hplan[actual_cell] - hcells[int(Flow_dir[actual_cell])] - 1.0e-4 < 0:
						
						print('Valor Negativo 1')
					
					hcells[int(Flow_dir[actual_cell])] += hplan[actual_cell] - hcells[int(Flow_dir[actual_cell])] - 1.0e-4
					
					hplan[int(Flow_dir[actual_cell])] = hcells[int(Flow_dir[actual_cell])]
					
					#Vol_dep += (hplan[actual_cell] - hcells[int(Flow_dir[actual_cell])] - 1.0e-4)*AreaHex #!!!!!!!!!!!!!!!!!!!!
					Vol_dep += Qtemp - (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])] #!!!!!!!!!!!!!!!!!!!!
					
				else:
					
					if h_lake_dep - hcells[int(Flow_dir[actual_cell])]  < 0:
						
						print('Valor Negativo 2: %f' %(h_lake_dep - hcells[int(Flow_dir[actual_cell])] ))
					
					hcells[int(Flow_dir[actual_cell])] += h_lake_dep - hcells[int(Flow_dir[actual_cell])] 
					
					hplan[int(Flow_dir[actual_cell])] = hcells[int(Flow_dir[actual_cell])]
					
					Vol_dep += Qtemp # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				
				count1 += 1
				
				continue
			
			# Outros casos
			
			if h_lake_dep > hplan[actual_cell] and flag1 == 0:
				
				Qcells[Lake_cells[int(Flow_dir[actual_cell])][2]] += (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])]
				
				if Aplan[int(Flow_dir[actual_cell])] == AreaHex :
					
					if hplan[actual_cell] - hcells[int(Flow_dir[actual_cell])] - 1.0e-4 < 0:
						
						print('Valor Negativo 3')
						
						Qcells[Lake_cells[int(Flow_dir[actual_cell])][2]] += Qtemp - (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])]
						
					else:	
					
						hcells[int(Flow_dir[actual_cell])] += hplan[actual_cell] - hcells[int(Flow_dir[actual_cell])] - 1.0e-4
					
						hplan[int(Flow_dir[actual_cell])] = hcells[int(Flow_dir[actual_cell])]
						
						Vol_dep += Qtemp - (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])] #!!!!!!!!!!!!!!!!!!!!
					
				elif hcells[int(Flow_dir[actual_cell])] >= hplan[actual_cell]:
					
					if hplan[actual_cell] - hplan[int(Flow_dir[actual_cell])] - 1.0e-4 < 0:
						
						print('Valor Negativo 4')
						
						Qcells[Lake_cells[int(Flow_dir[actual_cell])][2]] += Qtemp - (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])]
						
					else:
						
						hplan[int(Flow_dir[actual_cell])] += hplan[actual_cell] - hplan[int(Flow_dir[actual_cell])] - 1.0e-4
						
						Vol_dep += Qtemp - (h_lake_dep - hplan[actual_cell])*Aplan[int(Flow_dir[actual_cell])] #!!!!!!!!!!!!!!!!!!!!
				
			else:
				
				if Aplan[int(Flow_dir[actual_cell])] == AreaHex:
					
					if Qtemp/Aplan[int(Flow_dir[actual_cell])] < 0:
						
						print('Valor Negativo 5')
					
					hcells[int(Flow_dir[actual_cell])] += Qtemp/Aplan[int(Flow_dir[actual_cell])]
				
					hplan[int(Flow_dir[actual_cell])] = hcells[int(Flow_dir[actual_cell])]
					
				else:
					
					if Qtemp/Aplan[int(Flow_dir[actual_cell])] < 0:
						
						print('Valor Negativo 6')
					
					hplan[int(Flow_dir[actual_cell])] += Qtemp/Aplan[int(Flow_dir[actual_cell])]
			
				Vol_dep += Qtemp # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		
		
		count1 += 1
	
	count_ext = 0
	
	print('Volume - Erosion')
	print(Vol_ero)
	print('Volume - Deposition')
	print(Vol_dep)
	print('Volume - Output')
	print(Vol_bord)
	print('Balance: %f' %(Vol_bord - Total_Extern_Sediment - (Vol_ero - Vol_dep)))
	
	if(int(Vol_bord - Total_Extern_Sediment - (Vol_ero - Vol_dep)) != 0):
		
		print("Sediment Balance ERROR!")
		
		exit()
	
	return(hcells, hplan, Aplan, Discharge_cells, Run_Lakes, Qeqb_Out, Qdif)