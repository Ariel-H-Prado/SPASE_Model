# -*- coding: utf-8 -*-
# 10.05.2021
# Numerical Model SPASE - Sedimentay Processes and Alluvial Systems Evolution

from scipy.interpolate import griddata
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import math
import os

Dir = os.getcwd()		# Actual Directory

sys.path.append(Dir + '/functions')     # Import functions from folder /functions

from Hex_grid_generator import *
from Topography_generator_simple import *
from Hex_neighborhood import *
from Find_minima import *
from Groups_Root import *
from Stream_Power_Lateral_Erosion import *
from Function_Width_Channel import *
from Debug_Functions import *


plt.clf()

sys.setrecursionlimit(100000)

inicio = time.time()

secpyear = 60.*60.*24.*365.2564					# Seconds per year



###############################################################################################################################################
# Parameters Definition


Lhex = 4000.0											# Regular hexagon, side size  (meters)
Nxhex = 129												# Number of hexagons on coordinate x
Nyhex = 62												# Number of hexagons on coordinate y

pluvAno_mm_Ini = 1500.0 									# Rainfall rate on each cell (mm/year)
pluvAno_mm = pluvAno_mm_Ini
pluvAno = pluvAno_mm*1.0e-3								# Rainfall rate on each cell (m^3/year per m^2)


m = 1.425025e0													# m - Discharge coefficient on the Stream Power equation for sediment transport capacity
n = 1.0e0														# n - Slope coefficient on the Stream Power equation for sediment transport capacity
Kf = 0.026235													# Kf - Dimensional correction coefficient on the Stream Power equation for sediment transport capacity
Lf = 1.0e4 														# Aluvial erosion lenght scale
hzero = 1.0e3													# Constante para transporte em lagos

LatCoef1 = 15.730489249273928									# Lateral erosion coefficient
LatCoef2 = 0.301029995664										# Lateral erosion coefficient
Lat_h_coef = 1.0e1											 	# Coeficiente de erosao lateral altura

LengDiscRiver = PolyFit_Rivers()							# Exponential adjustment of discharge and width for rivers in Amazonia


dt = 1.0e-2												# Time step in years units
ti = 0													# Initial time (years)
tf = 10000												# Final time	(years)		

AreaHex = Lhex*Lhex*1.5*(3.0**0.5)						# Hexagon area

xini = 1
yini = 1

Espx = Lhex*(3.**0.5)						# Distance betwen the center of two cells in the x axis 
Espy = Lhex*1.5								# Distance betwen the center of two cells in the y axis 

xfin = xini  + Nxhex*Espx
yfin = yini  + Nyhex*Espy


###############################################################################################################################################

Ini_Wat_solim = 55522.754					# Initial Volume of water entering the external rivers (m3 /s)
Ini_Sed_solim = 8.62473401369303			# Initial Volume of sediment entering the external rivers (m3 /s)

Ini_Wat_jurua = 4970.593
Ini_Sed_jurua = 0.728528302562532

Ini_Wat_japura = 14555.073
Ini_Sed_japura = 2.24533241801648

Ini_Wat_jutai = 2301.853
Ini_Sed_jutai = 0.227014561588017

Ini_Wat_purus = 6650.166
Ini_Sed_purus = 0.882458271543512

Ini_Wat_negro = 29187.611
Ini_Sed_negro = 1.33144524926895

Extern_River = [Nxhex*Nyhex/2, Ini_Wat_solim*secpyear*dt, 22, Ini_Wat_jurua*secpyear*dt, Nxhex*(Nyhex - 2), 
				Ini_Wat_japura*secpyear*dt, Nxhex*2, Ini_Wat_jutai*secpyear*dt, 91, Ini_Wat_purus*secpyear*dt, Nxhex*Nyhex - 23, Ini_Wat_negro*secpyear*dt]	# External River entering through an edge [Edge cell number, Flow m3 at each time step]
Sed_Extern = [Nxhex*Nyhex/2, Ini_Sed_solim*secpyear*dt, 22, Ini_Sed_jurua*secpyear*dt, Nxhex*(Nyhex - 2), 
			  Ini_Sed_japura*secpyear*dt, Nxhex*2, Ini_Sed_jutai*secpyear*dt, 91, Ini_Sed_purus*secpyear*dt, Nxhex*Nyhex - 23, Ini_Sed_negro*secpyear*dt]												


###############################################################################################################################################

Slop_sink = 1.00004					# Slope for the sink cells if the sink cells height are above the minimum bedrock
	
h_min_bedrock = 100.0				# Bedrock elevation in the scenario

flag_bedrock = 1					# If flag equal to 1 all the sink cells of the model are equal to the bedrock level at time = 0

Annual_Discharge_rate = 0.0			# Annual discharge variation around the annual mean discharge

Expoent_Sed_Water = 0.5 			# Expoent for water and sediment flux ratio

###############################################################################################################################################

# Grid creation for hexagonal cells

inicio_temp = time.time()

[cells, edges, edgetype] = Hex_grid_generator(Lhex, Nxhex, Nyhex, xini, yini)

fim_temp = time.time()

Tempo_temp = fim_temp - inicio_temp
print('Hex_grid_generator')
print(Tempo_temp)

np.savetxt(Dir + '/Figures/cells.txt', cells)

# Creation of neigbohr adress of the cells array

inicio_temp = time.time()

cells_neighbor = Hex_neighbo (cells, edgetype, Nxhex)

np.savetxt(Dir + '/Figures/cells_neighbor.txt', cells_neighbor)

fim_temp = time.time()

Tempo_temp = fim_temp - inicio_temp
print('Hex_neighbo')
print(Tempo_temp)

# Define the sink cells (sorvtype = 1.0)

sorvtype = np.zeros(len(cells))

count1 = 0

while count1 < Nyhex:
	
	sorvtype[Nxhex*count1 + Nxhex - 1] = 1
	
	count1 += 1

###############################################################################################################################################
# Synthetic topography creation

# Topography generator simple: Inclinated plan in the direction of sink cells
# M , multiplicator random
# M2, inclination coefficient


hmin = 100.0

M = 0.5

M2 = 0.0

M3 = 0.00001

inicio_temp = time.time()

hcells = Topo_gen1(cells, M, M2, M3, hmin)

fim_temp = time.time()

Tempo_temp = fim_temp - inicio_temp
print('Topo_gen1')
print(Tempo_temp)

hcells = np.asarray(hcells)

hcells[sorvtype ==1] += 0.5

hplan = np.copy(hcells) 	# Elevation of floodplain on each cell

Aplan = [1]*len(cells)

Achannel = np.zeros(len(cells))

######################################

# Previous Topography

hcells = np.loadtxt('Topografia100.txt')

hplan = np.loadtxt('Planicie100.txt')

Aplan = np.loadtxt('Area_plan100.txt')

if flag_bedrock == 1:

	hcells[sorvtype ==1] = h_min_bedrock

	hplan[sorvtype ==1] = h_min_bedrock

######################################

temp = []
	
temp = np.asarray(hcells)

np.savetxt(Dir + '/Figures/Topografia_inicial.txt', temp)


#####################################################################################################################################################
# Part 1 first calculation of drainage and lakes

inicio_temp = time.time()
	
# Routine for the first step of calculating drainage in a topography
# Edge sink cells are those of the type base (sorvtype == 1), -2. Local minimum, -1
[Flow_dir, Minimum_address, Sorver_address, Decr_Adress_Cells] = Flows_dir_minimum (cells, edgetype, cells_neighbor, hplan, sorvtype) 

fim_temp = time.time()

Tempo_temp = fim_temp - inicio_temp
print('Flows_dir_minimum')
print(Tempo_temp)
	
inicio_temp = time.time()
	
# Root program to find drainage groups and lakes (regions with minimum locality)
[Lake_cells, Lake_cells_address] = Groups_Root(Flow_dir, Minimum_address, Sorver_address, cells_neighbor, cells, hplan)

fim_temp = time.time()

Tempo_temp = fim_temp - inicio_temp
print('Groups_Root')
print(Tempo_temp)

#############################################################################################################################################
# Inicio do loop

counttime = ti + dt				# Time counter
countimage = 0
countdif = 0

pluvCell = pluvAno*AreaHex*dt				# Rain volume of each cell (Discharge m3 at each time step (dt in years))

temp = np.asarray(hcells)

np.savetxt(Dir + '/Figures/Topografia0.txt', temp)

temp = np.asarray(hplan)

np.savetxt(Dir + '/Figures/Planicie0.txt', temp)
		
temp = np.asarray(Flow_dir)
		
np.savetxt(Dir + '/Figures/Flow_Dir0.txt', temp)
		
temp = np.array(Lake_cells)#[:,0]
		
np.savetxt(Dir + '/Figures/Lakes0.txt', temp)

temp = np.asarray(Aplan)
		
np.savetxt(Dir + '/Figures/Area_plan0.txt', temp)

#####################################################################
# Initial sink cells elevation

Flag_slope = 1

Sink_neig = np.linspace(Nxhex - 2, Nxhex*Nyhex - 1, Nyhex).astype(int)	# Adress of neighbor cells of sink cells

if Flag_slope == 1:
	
	
	h_Min_Sink_neig = min(hplan[Sink_neig])
	
	Adr_h_Min_Sink_neig = np.argmin(hplan[Sink_neig])
	
	Adr_h_Min_Sink_neig = Sink_neig[Adr_h_Min_Sink_neig]
	
	h_sink = h_Min_Sink_neig - Slop_sink*Espx
	
	if h_sink > h_min_bedrock:
	
		hcells[sorvtype ==1] = h_sink
	
		hplan[sorvtype ==1] = h_sink
		
		
	else:
		
		hcells[sorvtype ==1] = h_min_bedrock
	
		hplan[sorvtype ==1] = h_min_bedrock
	
	print("H sink : %f" %h_sink)
	print("H sink cell : %f" %hplan[Nxhex -1])
	print("Slope min : %f" %((hplan[Adr_h_Min_Sink_neig] - hplan[Nxhex -1])/Espx))
	print("Adress : %f" %(Adr_h_Min_Sink_neig))

#####################################################################

countimage = 0

countimage2 = 1

countlake = 0

inicio_temp_total = time.time()

while counttime < tf:
	
	Run_Lakes = 0
	
	print(counttime)
	
	
	########################
	# Seasonal Changes in rainfall and water discharges input
	
	#Rainfall changes
	
	pluvAno_mm = pluvAno_mm_Ini + pluvAno_mm_Ini*Annual_Discharge_rate*np.sin(2*np.pi*counttime)								# Rainfall rate in each cell (mm/year)
	
	pluvAno = pluvAno_mm*1.0e-3	
	
	pluvCell = pluvAno*AreaHex*dt
	
	print("Rainfall: %f" %pluvAno_mm)
	
	# Discharges changes
	
	Actual_Discharge_rate = Annual_Discharge_rate*np.sin(2*np.pi*counttime)
	Actual_Discharge_rate_phase2 = Annual_Discharge_rate*np.sin(2*np.pi*(counttime + 0.5))
	
	Wat_solim = Ini_Wat_solim + Ini_Wat_solim*Actual_Discharge_rate												# Volume of water entering the external rivers (m3 /s)
	Sed_solim = (Ini_Sed_solim / (Ini_Wat_solim ** Expoent_Sed_Water))*(Wat_solim ** Expoent_Sed_Water)			# Volume of sediment entering the external rivers (m3 /s)
	
	Extern_River[1] = Wat_solim*secpyear*dt
	Sed_Extern[1] = Sed_solim*secpyear*dt

	Wat_jurua = Ini_Wat_jurua + Ini_Wat_jurua*Actual_Discharge_rate
	Sed_jurua = (Ini_Sed_jurua / (Ini_Wat_jurua ** Expoent_Sed_Water))*(Wat_jurua ** Expoent_Sed_Water)
	
	Extern_River[3] = Wat_jurua*secpyear*dt
	Sed_Extern[3] = Sed_jurua*secpyear*dt

	Wat_japura = Ini_Wat_japura + Ini_Wat_japura*Actual_Discharge_rate
	Sed_japura = (Ini_Sed_japura / (Ini_Wat_japura ** Expoent_Sed_Water))*(Wat_japura ** Expoent_Sed_Water)	
	
	Extern_River[5] = Wat_japura*secpyear*dt
	Sed_Extern[5] = Sed_japura*secpyear*dt

	Wat_jutai = Ini_Wat_jutai + Ini_Wat_jutai*Actual_Discharge_rate
	Sed_jutai = (Ini_Sed_jutai / (Ini_Wat_jutai ** Expoent_Sed_Water))*(Wat_jutai ** Expoent_Sed_Water)
	
	Extern_River[7] = Wat_jutai*secpyear*dt
	Sed_Extern[7] = Sed_jutai*secpyear*dt

	Wat_purus = Ini_Wat_purus + Ini_Wat_purus*Actual_Discharge_rate
	Sed_purus = (Ini_Sed_purus / (Ini_Wat_purus ** Expoent_Sed_Water))*(Wat_purus ** Expoent_Sed_Water)
	
	Extern_River[9] = Wat_purus*secpyear*dt
	Sed_Extern[9] = Sed_purus*secpyear*dt

	Wat_negro = Ini_Wat_negro + Ini_Wat_negro*Actual_Discharge_rate_phase2
	Sed_negro = (Ini_Sed_negro / (Ini_Wat_negro ** Expoent_Sed_Water))*(Wat_negro ** Expoent_Sed_Water)
	
	Extern_River[11] = Wat_negro*secpyear*dt
	Sed_Extern[11] = Sed_negro*secpyear*dt
	
	
	########################
	
	# Stream Power Lateral Erosion and Drainage functions

	inicio_temp = time.time()
	
	[hcells, hplan, Aplan, Run_Lakes, Discharge_cells, Qeqb_Out, Qdif] = Stream_Power_Lateral_Erosion(hcells, hplan, Aplan, AreaHex, Decr_Adress_Cells, Flow_dir, Lake_cells, 
														  cells_neighbor, pluvCell, Lake_cells_address, Extern_River, dt, Kf,Lf, 
														  LengDiscRiver, sorvtype, hzero, Lhex, Espx, Achannel, LatCoef1, LatCoef2, secpyear, Sed_Extern, Lat_h_coef, m, n)
	
	fim_temp = time.time()

	Tempo_temp = fim_temp - inicio_temp
	
	####################
	# Slope constant in sink cells
	
	# Final cell slope constant with the biggest discharge neighbor
	
	Adr_h_Min_Sink_neig = np.argmax(np.asarray(Discharge_cells[Sink_neig]))
	
	Adr_h_Min_Sink_neig = Sink_neig[Adr_h_Min_Sink_neig]
	
	h_Min_Sink_neig = hplan[Adr_h_Min_Sink_neig]
	
	h_sink = h_Min_Sink_neig - Slop_sink*Espx
	
	# Put gradual variation of base level
	
	Dep_Const = 0.05
	
	Dep_Const_incision = 0.1
	
	if h_sink > 130.0:
		
		Dep_Const = 0.005
	
	h_control = hcells[Nxhex -1]
	
	if h_sink > h_control + Dep_Const*dt and (Discharge_cells[Adr_h_Min_Sink_neig]/(secpyear*dt)) > 50000.0 :
		
		hcells[sorvtype ==1] += Dep_Const*dt
	
		hplan[sorvtype ==1] += Dep_Const*dt
		
		print("1: Deposition")
	
	if h_sink > h_min_bedrock and h_sink < h_control + Dep_Const*dt and h_sink > h_control :
		
		print("2: Deposition")
	
		hcells[sorvtype ==1] = h_sink
	
		hplan[sorvtype ==1] = h_sink
		
	elif h_sink > h_min_bedrock and h_sink < h_control :
		
		print ("3: Erosion")
		
		hcells[sorvtype ==1] += - Dep_Const_incision*dt
	
		hplan[sorvtype ==1] += - Dep_Const_incision*dt
			
	elif h_sink < h_control + Dep_Const*dt:
		
		hcells[sorvtype ==1] = h_min_bedrock
	
		hplan[sorvtype ==1] = h_min_bedrock
		
		print("4: Bedrock")
	
	print("H sink : %f" %h_sink)
	print("H sink cell : %f" %hplan[Nxhex -1])
	print("Max discharge border : %f" %(Discharge_cells[Adr_h_Min_Sink_neig]/(secpyear*dt)))
	print("Slope min : %f" %((hplan[Adr_h_Min_Sink_neig] - hplan[Nxhex -1])/Espx))
	
	
	########################
	
	# Drainage calculation on each 0.1 year
	
	if countlake >= 0.1/dt or counttime < 0.5:
		
		
		[Flow_dir, Minimum_address, Sorver_address, Decr_Adress_Cells] = Flows_dir_minimum (cells, edgetype, cells_neighbor, hplan, sorvtype)	
		
		[Lake_cells, Lake_cells_address] = Groups_Root(Flow_dir, Minimum_address, Sorver_address, cells_neighbor, cells, hplan)	
		
		countlake = 0
	
	if countimage2 == 1:
		
		temp = []
		
		temp = np.asarray(Discharge_cells/(secpyear*dt))

		np.savetxt(Dir + '/Figures/Discharge%d.txt' %(countimage), temp)
	
	if countimage2 == tf*0.01/dt:
		
		temp = []

		temp = np.asarray(hcells)

		np.savetxt(Dir + '/Figures/Topografia%d.txt' %(countimage+1), temp)

		temp = np.asarray(hplan)

		np.savetxt(Dir + '/Figures/Planicie%d.txt' %(countimage+1), temp)
		
		temp = np.asarray(Flow_dir)
		
		np.savetxt(Dir + '/Figures/Flow_Dir%d.txt' %(countimage+1), temp)
		
		temp = np.array(Lake_cells)#[:,0]
		
		np.savetxt(Dir + '/Figures/Lakes%d.txt' %(countimage+1), temp)
		
		temp = np.asarray(Aplan)
		
		np.savetxt(Dir + '/Figures/Area_plan%d.txt' %(countimage+1), temp)
		
		temp = np.asarray(Qeqb_Out)
		
		np.savetxt(Dir + '/Figures/Qeqb_Out%d.txt' %(countimage+1), temp)
		
		temp = np.asarray(Qdif)
		
		np.savetxt(Dir + '/Figures/Qdif%d.txt' %(countimage+1), temp)
		
		countimage += 1
		
		countimage2 = 0
		
		print(counttime)
	
	countimage2 += 1
	counttime += dt
	countlake += 1
	
fim_temp_total = time.time()

Tempo_temp_total = fim_temp_total - inicio_temp_total	

print('Tempo Total')
print(Tempo_temp_total)

