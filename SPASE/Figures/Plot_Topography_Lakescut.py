# -*- coding: utf-8 -*-

# codigo para gerar imagens de topografia de entrada

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from scipy.interpolate import griddata


from Function_Width_Channel import *

import sys
x=10000
sys.setrecursionlimit(x)


#######################################################

def linewidth_from_data_units(linewidth, axis, reference='y'):
    """
    Convert a linewidth in data units to linewidth in points.

    Parameters
    ----------
    linewidth: float
        Linewidth in data units of the respective reference-axis
    axis: matplotlib axis
        The axis which is used to extract the relevant transformation
        data (data limits and size must not change afterwards)
    reference: string
        The axis that is taken as a reference for the data width.
        Possible values: 'x' and 'y'. Defaults to 'y'.

    Returns
    -------
    linewidth: float
        Linewidth in points
    """
    fig = axis.get_figure()
    if reference == 'x':
        length = fig.bbox_inches.width * axis.get_position().width
        value_range = np.diff(axis.get_xlim())[0]
    elif reference == 'y':
        length = fig.bbox_inches.height * axis.get_position().height
        value_range = np.diff(axis.get_ylim())[0]
    # Convert length to points
    length *= 72
    # Scale linewidth to value range
    return linewidth * (length / value_range)

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


# Rotina recursiva Lakes groups

def Lakes_group_rec (Lakes_groups, cells_neighbor, Lakes, Discharge, count_lake, n_groups, Lake_disch):
	
	Lakes_groups[count_lake] = n_groups
	
	count_neigh = 0
	
	while count_neigh < 6:
		
		neigh_adr = int(cells_neighbor[count_lake][count_neigh])
		
		if neigh_adr == -1:
			
			count_neigh += 1
			
			continue
			
		if Lakes[neigh_adr][0] == 0:
			
			if Discharge[neigh_adr] > Lake_disch:
				
				Lake_disch = Discharge[neigh_adr]
			
			
			count_neigh += 1
			
			continue
			
		if Lakes[neigh_adr][0] == 1 and Lakes_groups[neigh_adr] == 0:
			
			[Lakes_groups, Lake_disch] = Lakes_group_rec (Lakes_groups, cells_neighbor, Lakes, Discharge, neigh_adr, n_groups, Lake_disch)
			
			count_neigh += 1
			
			continue
			
		
		count_neigh += 1
	
	return (Lakes_groups, Lake_disch)

#######################################################

Lhex = 4000.0											# Tamanho do lado do hexagono regular
Nxhex = 129												# Numero de hexagonos na coordenada x
Nyhex = 62												# Numero de hexagonos na coordenada y

xini = 1
yini = 1

Espx = Lhex*(3.**0.5)						# Distancia entre o centro de duas celulas hexagonais
Espy = Lhex*0.5*(3)

xfin = xini  + Nxhex*Espx
yfin = yini  + Nyhex*Espy

cells = np.loadtxt('cells.txt')

cells_neighbor = np.loadtxt('cells_neighbor.txt')

LengDiscRiver = PolyFit_Rivers()							# Ajusta um exponencial aos dados de vazao vs espessura de rios amazonicos

ttotal = 1000

PassoTempohcells = 10
	
count1 = 0

meterstokm = 1.0e-3

while count1 < ttotal:
	
	#######################################################
	
	
	hcells = np.loadtxt('Topografia%d.txt' %(count1))
	

	temp = []
	
	temp = np.asarray(hcells)
	
	grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini:yfin:1000j]

	grid_z0 = griddata(cells, temp, (grid_x, grid_y), method='nearest')
	
	cmap = plt.get_cmap('terrain')
	
	new_cmap = truncate_colormap(cmap, 0.0, 0.8)
	'''
	plt.imshow(grid_z0.T, origin='lower', extent=(xini*meterstokm,xfin*meterstokm,yini*meterstokm,yfin*meterstokm), vmin = 80.0, vmax = 200.0, cmap=new_cmap)
	
	plt.colorbar(label='meters')
	
	plt.title('%d Years' %((count1)*100))
	
	plt.ylabel('kilometers')
	plt.xlabel('kilometers')
	
	plt.tight_layout()
	plt.savefig('Topografia%d.png' %(count1), dpi=500)
	plt.savefig('Topografia%d.pdf' %(count1), dpi=500)
	'''
	plt.close()
	
	
	#######################################################
	
	#######################################################
	
	#hcells = np.loadtxt('Planicie%d.txt' %count1)
	hcells = np.loadtxt('Topografia%d.txt' %(count1))
	
	hcells = hcells - 100.0
	
	Discharge = np.loadtxt('Discharge%d.txt' %count1)
	
	Flow_dir = np.loadtxt('Flow_Dir%d.txt' %count1)
	
	Lakes = np.loadtxt('Lakes%d.txt' %count1)
	
	temp = []
	
	temp = np.asarray(hcells)
	
	grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini:yfin:1000j]

	grid_z0 = griddata(cells, temp, (grid_x, grid_y), method='nearest')
	
	cmap2 = plt.get_cmap('terrain')
	
	new_cmap2 = truncate_colormap(cmap2, 0.1, 0.8)

	im1 = plt.imshow(grid_z0.T, origin='lower', extent=(xini*meterstokm,xfin*meterstokm,yini*meterstokm,yfin*meterstokm), vmin = 0.0, vmax = 120.0,cmap=new_cmap2)
	
	plt.colorbar(label='meters')
	
	plt.ylabel('kilometers')
	plt.xlabel('kilometers')
	
	Ncells = len(Discharge)
	
	actual_cell = 0
	
	alpha = 0.3
	
	Lake_Large = linewidth_from_data_units(Lhex*10.*meterstokm, plt.axes(), 'y')
	
	plt.scatter(xini*meterstokm, 0, color='b', alpha=0.0, s=Lake_Large, marker='h', edgecolor='')
	
	plt.scatter(xfin*meterstokm, 0, color='b', alpha=0.0, s=Lake_Large, marker='h', edgecolor='')
	
	# Grupos de lagos
	
	n_lakes = len(Lakes)
	
	Lakes_groups = np.zeros(n_lakes)
	
	Disch_Lakes_groups = [0]
	
	count_lake = 0
	
	n_groups = 1
	
	while count_lake < n_lakes:
		
		if Lakes[count_lake][0] == 1 and Lakes_groups[count_lake] == 0:
			
			Lake_disch = 0
			
			[Lakes_groups, Lake_disch] = Lakes_group_rec (Lakes_groups, cells_neighbor, Lakes, Discharge, count_lake, n_groups, Lake_disch)
			
			Disch_Lakes_groups.append(Lake_disch)
			
			n_groups += 1
		
		count_lake += 1
	
	
	# Testando o Lago bonito
	
	Lakes_array = np.array(Lakes)[:,0]
	
	disch_cut = max(Discharge)/1000.0
	
	count_x = 0
	
	while count_x < len(Lakes_array):
		
		
		if Lakes_array[count_x] == 1 and Disch_Lakes_groups[int(Lakes_groups[count_x])] < disch_cut:
			
			
			Lakes_array[count_x] = 0.0
		
		count_x += 1
	
	
	grid_z_Lake = griddata(cells, Lakes_array, (grid_x, grid_y), method='linear')
	
	Lake_array2 = np.copy(grid_z_Lake.T)
	
	Lake_array2 = np.ma.masked_where(Lake_array2 == 0, Lake_array2)
	
	cmap = plt.get_cmap('Blues')
	
	new_cmap = truncate_colormap(cmap, 0.5, 1.0)
	
	im2 = plt.imshow(Lake_array2, origin='lower', extent=(xini*meterstokm,xfin*meterstokm,yini*meterstokm,yfin*meterstokm), cmap=new_cmap, alpha=0.6)
	
	while actual_cell < Ncells:
		
		#if Lakes[actual_cell][0] == 1:
			
		#	plt.scatter(cells[actual_cell][0]*meterstokm, cells[actual_cell][1]*meterstokm, color=[alpha, alpha, 1.], s=Lake_Large, marker='h', edgecolor='')
			
		#	actual_cell += 1
			
		#	continue
		
		if Flow_dir[actual_cell] < 0:
			
			actual_cell += 1
			
			continue
		
		coord1 = cells[actual_cell]
		
		coord2 = cells[int(Flow_dir[actual_cell])]
		
		Disch = Discharge[actual_cell]
		
		Lchanel = Poly2(Disch, LengDiscRiver[0], LengDiscRiver[1])*meterstokm
		
		if Lchanel < 10*meterstokm:
			
			actual_cell += 1
			
			continue
			
		
		if Lchanel > Lhex:
			
			print('erro')
		
		River_Large = linewidth_from_data_units(Lchanel - Lchanel*0.8, plt.axes(), 'y')
		
		plt.plot([coord1[0]*meterstokm,coord2[0]*meterstokm],[coord1[1]*meterstokm,coord2[1]*meterstokm], linewidth = River_Large, alpha = 1.0, solid_capstyle="round", color='b')
		
		
		countneig = 0
		
		while countneig < 6:
			
			actneig = int(cells_neighbor[actual_cell][countneig])
			
			if actneig == -1 or Lakes[actneig][0] == 0:
				
				countneig += 1
				
				continue
				
			if Lakes[actneig][0] == 1 and Lakes[actneig][2] == actual_cell:
				
				coord2 = cells[actneig]
				
				plt.plot([coord1[0]*meterstokm,coord2[0]*meterstokm],[coord1[1]*meterstokm,coord2[1]*meterstokm], linewidth = River_Large, alpha = 1.0, solid_capstyle="round", color='b')
				
				break
			
			countneig += 1
		
		actual_cell += 1
	
	plt.title('%d Years' %(count1*100))
	
	plt.tight_layout()
	
	plt.savefig('Topografia%d.png' %count1, dpi=500)
	plt.savefig('Topografia%d.pdf' %count1, dpi=500)
	
	plt.close()
	
	
	
	#######################################################
	
	
	
	count1 += 1
	


plt.clf()