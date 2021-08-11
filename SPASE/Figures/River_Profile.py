# -*- coding: utf-8	-*-

# codigo para gerar	graficos do	perfil da topografia dos rios


import matplotlib.pyplot as	plt
import matplotlib.colors as	colors
import numpy as	np
from scipy.interpolate import griddata

from Function_Width_Channel	import *



#######################################################

#######################################################

def	linewidth_from_data_units(linewidth, axis, reference='y'):
	"""
	Convert a linewidth in	data units to linewidth	in points.

	Parameters
	----------
	linewidth:	float
		Linewidth	in data	units of the respective	reference-axis
	axis: matplotlib axis
		The axis which is	used to	extract	the	relevant transformation
		data (data limits	and	size must not change afterwards)
	reference:	string
		The axis that	is taken as	a reference	for	the	data width.
		Possible values: 'x' and 'y'.	Defaults to	'y'.

	Returns
	-------
	linewidth:	float
		Linewidth	in points
	"""
	fig = axis.get_figure()
	if	reference == 'x':
		length = fig.bbox_inches.width * axis.get_position().width
		value_range =	np.diff(axis.get_xlim())[0]
	elif reference	== 'y':
		length = fig.bbox_inches.height *	axis.get_position().height
		value_range =	np.diff(axis.get_ylim())[0]
	# Convert length to points
	length	*= 72
	# Scale linewidth to value	range
	return	linewidth *	(length	/ value_range)

def	truncate_colormap(cmap,	minval=0.0,	maxval=1.0,	n=100):
	new_cmap =	colors.LinearSegmentedColormap.from_list(
		'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
		cmap(np.linspace(minval, maxval, n)))
	return	new_cmap

#######################################################

Nxhex = 129												# Number of hexagons on coordinate x
Nyhex = 62												# Number of hexagons on coordinate y


River1 = Nxhex*Nyhex/2

cells =	np.loadtxt('cells.txt')

cells_neighbor = np.loadtxt('cells_neighbor.txt')

ttotal = 1000
	
count1 = 0

meterstokm = 1.0e-3

while count1 < ttotal:
	
	Discharge = np.loadtxt('Discharge%d.txt' %count1)
	
	Flow_dir =	np.loadtxt('Flow_Dir%d.txt'	%count1)
	
	Lakes = np.loadtxt('Lakes%d.txt' %count1)
	
	hcells	= np.loadtxt('Planicie%d.txt' %count1)
	
	River1_h =	[]
	
	River1_dist = []
	
	River1_Discharge =	[]
	
	River1_Flow = []
	
	# Rio 1
	
	River1_h.append(hcells[River1])
	
	River1_dist.append(0)
	
	River1_Discharge.append(Discharge[River1])
	
	control = 0
	
	Next_dir =	River1
	
	while control == 0:
		
		Actual = int(Flow_dir[Next_dir])
		
		if Actual	== -2:
			
			control = 1
			
			continue
			
		if Actual	== -1:
			
			Actual = int(Lakes[Next_dir][2])
		
		River1_Flow.append(Actual)
		
		if Lakes[Actual][0] == 1:
			
			Adr_overflow	= int(Lakes[Actual][2])
			
			# Caso lago que escoa em	lago
			
			if Lakes[Adr_overflow][0] ==	1:
				
				flag = 0
		
				while flag == 0:
			
					Next_Adr2 = Lakes[Adr_overflow][2]
				
					Adr_overflow =	int(Next_Adr2)
			
					if	Lakes[Adr_overflow][0] == 0:
					
						flag = 1
			
			Actual =	Adr_overflow
		
		Dist = River1_dist[len(River1_dist) -	1] + (((cells[Actual][0] - cells[Next_dir][0])**2 +	(cells[Actual][1] -	cells[Next_dir][1])**2)**0.5)/1000.0
		
		River1_h.append(hcells[Actual])
		
		River1_dist.append(Dist)
		
		River1_Discharge.append(Discharge[Actual])
		
		Next_dir = Actual
		
	fig, ax1 =	plt.subplots()
	
	color = 'tab:green'
	color = 'tab:red'
	ax1.set_xlabel('Distance from River Head (km)')
	
	ax1.set_ylabel('Elevation (m)', color=color)
	ax1.set_xlim([0,1300])
	ax1.set_ylim([100,200])
	ax1.set_yticks(np.linspace(100,200,21))
	ax1.grid(True, alpha=0.2)
	
	ax1.plot(River1_dist, River1_h, color=color)
	
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()	# instantiate a second axes that	shares the same	x-axis

	color = 'tab:blue'
	ax2.set_ylabel('Discharge (m3/s)',	color=color)  #	we already handled the x-label with	ax1
	ax2.plot(River1_dist, River1_Discharge, color=color, alpha=0.5)
	
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()	 # otherwise the right y-label is slightly clipped
	
	
	ax1.set_title("Profile Solimoes River %d Anos" %(count1*100))
	
	##########
	#Slope Solimoes
	
	River1_dist = np.array(River1_dist)*1.0e3
	River1_Discharge = np.array(River1_Discharge)
	River1_h = np.array(River1_h)
	
	#Before Jurua
	
	Bef_Jurua_dist = River1_dist[River1_Discharge < 55000.0]
	Bef_Jurua_h    = River1_h[River1_Discharge < 55000.0]
	
	Slope_Bef = []
	
	n_slope = len(Bef_Jurua_dist)
	
	n_slope_count = 0
	
	while n_slope_count < n_slope - 1:
		
		Dist_slope = Bef_Jurua_dist[n_slope_count + 1] - Bef_Jurua_dist[n_slope_count]
		
		h_dif_slope = Bef_Jurua_h[n_slope_count + 1] - Bef_Jurua_h[n_slope_count]
		
		Slope_Bef.append(abs(h_dif_slope/Dist_slope))
		
		n_slope_count += 1
	
	text1 = "Slope Before Confluence = %f" %np.mean(Slope_Bef)
	
	#After Jurua
	
	Aft_Jurua_dist = River1_dist[River1_Discharge >= 55000.0]
	Aft_Jurua_h    = River1_h[River1_Discharge >= 55000.0]
	
	Slope_Aft = []
	
	n_slope = len(Aft_Jurua_dist)
	
	n_slope_count = 0
	
	while n_slope_count < n_slope - 1:
		
		Dist_slope = Aft_Jurua_dist[n_slope_count + 1] - Aft_Jurua_dist[n_slope_count]
		
		h_dif_slope = Aft_Jurua_h[n_slope_count + 1] - Aft_Jurua_h[n_slope_count]
		
		Slope_Aft.append(abs(h_dif_slope/Dist_slope))
		
		n_slope_count += 1
	
	text2 = "Slope After Confluence = %f" %np.mean(Slope_Aft)
	
	if len(Aft_Jurua_h) > 2:
	
		text3 = "Slope Last cell = %f" %((Aft_Jurua_h[len(Aft_Jurua_h)-2] - Aft_Jurua_h[len(Aft_Jurua_h)-1])/Dist_slope)
		
	else:
		
		text3 = "Slope Last cell = %f" %((Bef_Jurua_h[len(Bef_Jurua_h)-2] - Bef_Jurua_h[len(Bef_Jurua_h)-1])/Dist_slope)
	
	##########
	
	ax1.text(50,195,text1)
	ax1.text(50,185,text2)
	ax1.text(50,175,text3)
	
	fig.savefig('Perfil_Solimoes_%d.png' %(count1), dpi=500)
	
	plt.close()
	
	
	#######################################################
	
	count1	+= 1
	

	
	