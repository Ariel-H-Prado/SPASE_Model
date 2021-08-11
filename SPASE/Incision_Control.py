# -*- coding: utf-8 -*-

# codigo para gerar imagens de topografia de entrada

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from scipy.interpolate import griddata

from Function_Width_Channel import *



#######################################################

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

#######################################################

#######################################################

Lhex = 4000.0											# Tamanho do lado do hexagono regular
Nxhex = 100												# Numero de hexagonos na coordenada x
Nyhex = 100												# Numero de hexagonos na coordenada y

xini = 1
yini = 1

Espx = Lhex*(3.**0.5)						# Distancia entre o centro de duas celulas hexagonais
Espy = Lhex*0.5*(1.+3.**0.5)

xfin = xini  + Nxhex*Espx
yfin = yini  + Nyhex*Espy

cells = np.loadtxt('cells.txt')

cells_neighbor = np.loadtxt('cells_neighbor.txt')

LengDiscRiver = PolyFit_Rivers()							# Ajusta um exponencial aos dados de vazao vs espessura de rios amazonicos

ttotal = 100

PassoTempohcells = 10
	
count1 = 1

meterstokm = 1.0e-3

while count1 < ttotal:
	
	#######################################################
	
	
	hcells = np.loadtxt('Topografia%d.txt' %(count1))
	
	hplan = np.loadtxt('Planicie%d.txt' %count1)
	
	hcells0 = np.loadtxt('Topografia%d.txt' %(count1-1))
	
	hplan0 = np.loadtxt('Planicie%d.txt' %(count1-1))
	
	hdif = hcells - hcells0

	temp = []
	
	temp = np.asarray(hplan)
	
	grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini:yfin:1000j]

	grid_z0 = griddata(cells, temp, (grid_x, grid_y), method='nearest')
	
	cmap = plt.get_cmap('terrain')
	
	new_cmap = truncate_colormap(cmap, 0.0, 0.8)

	plt.imshow(grid_z0.T, origin='lower', extent=(xini*meterstokm,xfin*meterstokm,yini*meterstokm,yfin*meterstokm), vmin = 45.0, vmax = 200.0, cmap=new_cmap)
	
	plt.colorbar(label='meters')
	
	plt.title('%d Anos' %((count1)*100))
	
	plt.ylabel('kilometers')
	plt.xlabel('kilometers')
	
	count2 = 0
	
	Min_dif = abs(min(hdif))
	
	
	while count2 < len(hcells):
		
		if hdif[count2] < 0 and abs(hdif[count2])/Min_dif > 0.03:
			print(count2)
			
			#Alfa = abs(hdif[count2])/Min_dif
			Alfa = 1.0
			
			plt.plot(cells[count2][0]*meterstokm, cells[count2][1]*meterstokm, 'ro', markersize = 0.4, alpha = Alfa)
			
		count2 += 1
	
	
	plt.tight_layout()
	plt.savefig('Incision_Control%d.png' %(count1), dpi=500)
	
	plt.close()
	
	count1 += 1
	

plt.clf()