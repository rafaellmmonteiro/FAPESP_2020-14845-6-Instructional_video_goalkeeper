# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 09:56:20 2021

@author: Rafael Luiz Martins Monteiro

Processamento de dados IC FAPESP 2021 - Instrução por vídeo

Análise SPM
variáveis:
0=VRSPM
1=VMLSPM
2=VRP
3=VMLP
4=TVRP
5=TVMLP
6=tampernaf
7=distcalcanharesy
8=passofrontal
9=angsaidafrontal
10=angjoelhospm
11=angjoelhomin

CALCULO TESTE T PAREADO VRP, VMLP, TVRP, TVMLP, DISTCALCANHARESY, PASSOFRONTAL, ANGSAIDAFRONTAL, ANGJOELHOMIN EM RELAÇÃO A LATERALIDADE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import spm1d
import math
from scipy import stats

dir_atual = os.getcwd()
dir_working = sorted(os.listdir(dir_atual + '/workingprepos/'))
saltos = 0
contcpre = 0
contcpos =0
contvpre = 0
contvpos =0

while(saltos<len(dir_working)):
    saltoanalisado = dir_working[saltos]
    dat = np.loadtxt(dir_atual + '/workingprepos/' + saltoanalisado)
    VRSPM = dat[0,2:] 
    VRSPM = VRSPM.reshape(1,-1)

    
    #separando varáveis por perna preferida e não preferida
    #grupo perna preferida
    if (saltoanalisado[3]=='D'):
        if (saltoanalisado[0]=='H' or saltoanalisado[0]=='K' or saltoanalisado[0]=='L' or saltoanalisado[0]=='M' or saltoanalisado[0]=='N' or saltoanalisado[0]=='O'):
            if (contcpre == 0):
                cpre= VRSPM        
                contcpre = contcpre + 1
            else:
                cpre= np.concatenate((cpre,VRSPM))   #cpre = perna preferida
        else:
            if (contcpos == 0):
                cpos= VRSPM        
                contcpos = contcpos + 1
            else:
                cpos= np.concatenate((cpos,VRSPM))  #cpos =perna não preferida


    #grupo perna não preferida
    if (saltoanalisado[3]=='E'):
        if (saltoanalisado[0]=='H' or saltoanalisado[0]=='K' or saltoanalisado[0]=='L' or saltoanalisado[0]=='M' or saltoanalisado[0]=='N' or saltoanalisado[0]=='O'):
            if (contcpos == 0):
                cpos= VRSPM        
                contcpos = contcpos + 1
            else:
                cpos= np.concatenate((cpos,VRSPM))  #cpos = perna não preferida
        else:
            if (contcpre == 0):
                cpre= VRSPM        
                contcpre = contcpre + 1
            else:
                cpre= np.concatenate((cpre,VRSPM))   #cpre = perna preferida


    saltos=saltos+1

distanciapernaspf = cpre[:,5]/cpre[:,4]
distanciapernaspnf = cpos[:,5]/cpos[:,4]

pernapreferida = cpre
pernanaopreferida = cpos

mediapf = np.mean(cpre[:,0])
mediapnf = np.mean(cpos[:,0])

saidalateralidade = np.hstack((pernapreferida, pernanaopreferida))
saidalateralidade = pd.DataFrame(saidalateralidade)

filepath = dir_atual + '/Analise estatistica/' + 'saidalateralidade.xlsx'

saidalateralidade.to_excel(filepath, index=False)


#fmt = '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f'
#np.savetxt(dir_atual + '/Analise estatistica/' + 'saidalateralidade.csv', saidalateralidade, fmt=fmt)
