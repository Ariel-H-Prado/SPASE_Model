# Funcao para encontrar parametros para equacao exponencial de distribuicao de vazao de canal (no canal e na planicie) (22/02/2019)
# Saida [Discharge_central (Descarga na celula do talvegue), Factor_exp (Fator da exponencial)]


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Rotina para calcular Largura de canais em funcao da vazao (Ajuste empirico)
# Discharge em m3/sec

def Poly2(x,a,b):
	
	y = a*(x**b)
	
	return(y)

def PolyFit_Rivers():
	
	xdata = [62,126,631,376,204,285,986,446,332,48,200,3087,238,1680,720,781,478,2610,634,922,1822,174,4741,
		 1352,4178,413,1642,486,815,2457,89,17951,33588,18843,23506,32,7999,266,821,15079,6369,795,455,1362,
		 3919,2109,86767,101463,57216,46635,37344,1523,1215,150,424,544,171]
	
	ydata = [0.08,0.05,0.09,0.07,0.06,0.1,0.14,0.12,0.12,0.07,0.07,0.42,0.06,0.19,0.15,0.15,0.06,0.22,0.1,0.18,
		 0.14,0.07,0.27,0.17,0.3,0.12,0.26,0.13,0.19,0.34,0.06,0.65,1.51,0.87,1.19,0.03,0.67,0.04,0.16,0.59,
		 0.4,0.16,0.1,0.16,0.32,0.32,2.37,3.24,2.21,1.53,1.11,0.24,0.17,0.1,0.14,0.12,0.03]
	
	yarray = np.asarray(ydata)
	
	yarray = yarray*1.0e3
	
	popt, pcov = curve_fit(Poly2, xdata, yarray)
	
	return(popt)



