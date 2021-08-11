# Rotina para gerar celulas hexagonais

import numpy as np

def Hex_grid_generator (Lhex, Nxhex, Nyhex, xini, yini):
	
	Ncells = Nxhex*Nyhex			# Total number of cells

	Espx = Lhex*(3.**0.5)			# spacing between columns in x
	Espy = Lhex*0.5*(3.0)			# spacing between lines in y
	
	xfin = xini  + Nxhex*Espx		# final x position of the cells in the last column
	yfin = yini  + Nyhex*Espy		# final y position of the cells in the last row
	
	xpos = np.arange(xini, xfin, Espx)	
	ypos = np.arange(yini, yfin, Espy)
	
	xv, yv = np.meshgrid(xpos,ypos)

	xzero = xv[0][0]
	yzero = yv[0][0]

	cells = [[0.0,0.0]] *Ncells		# Array with x, y position of each hexagonal cell
	cells = np.array(cells)
	cells[0] = [xzero,yzero]			
	
	edges = [0]*Ncells						# Array to check if cell is edge (0, no; 1, yes)
	edges = np.array(edges)
	edges[0] = 1
	
	edgetype = [0]*Ncells					# Array to check the type of border (0, not border; 1, left corner base)
	edgetype = np.array(edgetype)
	edgetype[0] = 1
	
	count1 = 0						# Y line counter
	count3 = 0						# Cells counter

	while count1 < Nyhex:
		
		count2 = 0
		
		while count2 < Nxhex:
			
			if count1 != 0 or count2 != 0:
				
				if count1 == 0 or count2 == 0 or count1 == (Nyhex - 1) or count2 == (Nxhex - 1):  # Check if it's edge
					
					edges[count3] = 1
				
					if count1 == 0 and count2 != (Nxhex - 1):
					
						edgetype[count3] = 2
						# type 2, base range
				
					if count1 == 0 and count2 == (Nxhex - 1):
					
						edgetype[count3] = 3
						# type 3, right end base
					
					if count2 == 0 and count1 != (Nyhex - 1) and count1%2 !=0 :
						
						edgetype[count3] = 4
						# type 4, left band inside
					
					if count2 == 0 and count1 != (Nyhex - 1) and count1%2 ==0 :
						
						edgetype[count3] = 11
						# type 11, left lane outside
					
					if count2 == (Nxhex - 1) and count1 != (Nyhex - 1) and count1 != 0 and count1%2 == 0:
						
						edgetype[count3] = 5
						# type 5, right track outside
						
					if count2 == (Nxhex - 1) and count1 != (Nyhex - 1) and count1 != 0 and count1%2 != 0:
					
						edgetype[count3] = 12
						# type 12, right band inside
				
					if count2 == 0 and count1 == (Nyhex - 1) and count1%2 != 0:
					
						edgetype[count3] = 7
						# type 7, top left top inside
					
					if count2 == 0 and count1 == (Nyhex - 1) and count1%2 == 0:
					
						edgetype[count3] = 6
						# type 6, top left top outside
					
					if count1 == (Nyhex - 1) and count2 != (Nxhex - 1) and count2 != 0 and count1%2 != 0:
						
						edgetype[count3] = 8
						# type 8, top band inside
						
					if count1 == (Nyhex - 1) and count2 != (Nxhex - 1) and count2 != 0 and count1%2 == 0:
					
						edgetype[count3] = 14
						# type 14, top stripe outside
						
					if count2 == (Nxhex - 1) and count1 == (Nyhex - 1) and count1%2 == 0:
					
						edgetype[count3] = 9
						# type 9, top right top outside
					
					if count2 == (Nxhex - 1) and count1 == (Nyhex - 1) and count1%2 != 0:
						
						edgetype[count3] = 10
						# type 10, top right top inside
				
				else:
				
						if count1%2 != 0:
						
							
							edgetype[count3] = 0
							# Type 0, internal inside
							
						if count1%2 == 0:						
								
							edgetype[count3] = 13
							# Type 13, internal outside
			
				if count1%2.0 == 0:
				
					xpoint = xv[count1][count2]
					ypoint = yv[count1][count2]
					
					cells[count3] = [xpoint,ypoint]
					
				
				else:
				
					xpoint = xv[count1][count2] + Espx/2.0
					ypoint = yv[count1][count2]
				
					cells[count3] = [xpoint,ypoint]
					
			
			count3 += 1
			count2 += 1
	
		count1 += 1





	return (cells, edges, edgetype)