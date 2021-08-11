# Calculation in one step of time of drainage, erosion, deposition and trsport of sediments on each cell. Usin Stram Pwoer equation and Lateral erosion approach. 

from Function_Width_Channel import *
from Stream_Power_Functions import *
from Lake_Functions import *
import numpy as np
import matplotlib.pyplot as plt
import time

def Stream_Power_Lateral_Erosion (hcells, hplan, Aplan, AreaHex, Decr_Adress_Cells, Flow_dir, Lake_cells, cells_neighbor, pluvCell,
								  Lake_cells_address, Extern_River, dt, Kf,Lf, LengDiscRiver, sorvtype, hzero, 
								  Lhex, Espx, Achannel, LatCoef1, LatCoef2, secpyear, Q_Extern, Lat_h_coef, m, n):
	
	ncells = len(hcells)
	
	Discharge_cells = np.zeros(ncells)							# Discharge in each cell
	
	Channel_adr = []											# Cells address that are in the edges of the lakes 
	
	count = 0
	
	while count < len(Extern_River):
		
		Discharge_cells[Extern_River[count]] = Extern_River[count + 1]
		
		count += 2
	
	#######################################################
	
	
	# Drainage Calculation in lakes
	
	[hcells, hplan, Aplan, Discharge_cells] = Drainage_Lake_Func(hcells, Lake_cells_address, Lake_cells, hzero, 
											   cells_neighbor, Discharge_cells, pluvCell, dt, AreaHex, Lhex, Espx, hplan, Aplan)
	
	
	
	
	#######################################################
	
	# Stream Power equation and Lateral erosion sediment functions
	
	
	[hcells, hplan, Aplan, Discharge_cells, Run_Lakes, Qeqb_Out, Qdif] = Streampower(hcells, hplan, Aplan, AreaHex, Decr_Adress_Cells, Flow_dir, Lake_cells, cells_neighbor, pluvCell,
														 dt, Kf,Lf, LengDiscRiver, sorvtype,Lhex, Espx, Achannel, Discharge_cells, LatCoef1, LatCoef2, secpyear, Q_Extern, Lat_h_coef, m, n)
	
	
	#######################################################
	
	
	return(hcells, hplan, Aplan, Run_Lakes, Discharge_cells, Qeqb_Out, Qdif)