# -*- coding: utf-8 -*-

# codigo para gerar imagens de topografia de entrada

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

Lhex = 4000.0											# Tamanho do lado do hexagono regular
Nxhex = 200												# Numero de hexagonos na coordenada x
Nyhex = 200												# Numero de hexagonos na coordenada y

xini = 1
yini = 1

Espx = Lhex*(3.**0.5)						# Distancia entre o centro de duas celulas hexagonais
Espy = Lhex*0.5*(1.+3.**0.5)

xfin = xini  + Nxhex*Espx
yfin = yini  + Nyhex*Espy

cells = np.loadtxt('cells.txt')

count1 = 0

countDifu = 1000

PassoTempoDifu = 100

while count1 < countDifu:

	Difusivity_cells = np.loadtxt('Difusivity%d.txt' %count1)

	temp = []

	temp = np.asarray(Difusivity_cells)

	#grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini + 44000:yfin:1000j]
	grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini:yfin:1000j] 

	grid_z0 = griddata(cells, temp, (grid_x, grid_y), method='nearest')

	#plt.imshow(grid_z0.T, origin='lower', extent=(xini,xfin,yini + 44000,yfin), cmap='viridis')
	plt.imshow(grid_z0.T, origin='lower', extent=(xini,xfin,yini,yfin), cmap='viridis')

	plt.colorbar()

	plt.title('%d Anos' %(count1*PassoTempoDifu))

	plt.savefig('Difusivity%d.png' %count1)

	#countdif += 1
	
	plt.clf()
	
	count1 += 1

count1 = 1

counthcells = 1000

PassoTempohcells = 100

while count1 < counthcells:

	hcells = np.loadtxt('hcells%dAno.txt' %count1)

	temp = []

	temp = np.asarray(hcells)

	#grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini + 44000:yfin:1000j]
	grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini:yfin:1000j]

	grid_z0 = griddata(cells, temp, (grid_x, grid_y), method='cubic')

	plt.imshow(grid_z0.T, origin='lower', extent=(xini,xfin,yini + 44000,yfin), cmap='viridis')
	#plt.imshow(grid_z0.T, origin='lower', extent=(xini,xfin,yini,yfin), cmap='viridis')

	plt.colorbar()

	plt.title('%d Anos' %(count1*PassoTempohcells))

	plt.savefig('hcells%d.png' %(count1-1))

	#countdif += 1

	plt.clf()
	
	count1 += 1
	


Topografia_inicial = np.loadtxt('Topografia_inicial.txt')

temp = []

temp = np.asarray(Topografia_inicial)

grid_x, grid_y = np.mgrid[ xini:xfin:1000j, yini:yfin:1000j]  

grid_z0 = griddata(cells, temp, (grid_x, grid_y), method='cubic')

plt.imshow(grid_z0.T, origin='lower', extent=(xini,xfin,yini,yfin), cmap='viridis')

plt.colorbar()

plt.title('0 Anos')

plt.savefig('Topografia_inicial.png')

#countdif += 1

plt.clf()