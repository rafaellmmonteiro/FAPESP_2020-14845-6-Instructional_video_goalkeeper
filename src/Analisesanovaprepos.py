# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 09:56:20 2021

@author: Rafael Luiz Martins Monteiro

Processamento de dados IC FAPESP 2021 - Instrução por vídeo

Análise SPM
variáveis:
0=VRSPM
1=VMLSPM
2=VRP                  1
3=VMLP                 2
4=TVRP                 3
5=TVMLP                4
6=tampernaf            5  DISTPERN
7=distcalcanharesy     6
8=passofrontal         7
9=angsaidafrontal      8
10=angjoelhospm        9
11=angjoelhomin        10

CALCULO DO SPM PARA Ângulo do joelho da perna ipsilateral ao salto
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import spm1d
import math

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

    
    #separando varáveis por grupo controle e vídeo 10 primeiros e 10 ultimos saltos
    #grupo controle
    if (saltoanalisado[0]=='A' or saltoanalisado[0]=='H' or saltoanalisado[0]=='L' or saltoanalisado[0]=='N'):
        if (int(saltoanalisado[1:3]) < 11):
            if (contcpre == 0):
                cpre= VRSPM        #controle pré
                contcpre = contcpre + 1
            else:
                cpre= np.concatenate((cpre,VRSPM))
        if (int(saltoanalisado[1:3]) > 10):
            if (contcpos == 0):
                cpos = VRSPM        #controle pos
                contcpos = contcpos + 1
            else:
                cpos = np.concatenate((cpos,VRSPM))
            if (len(cpos)== 12):
                oi = saltoanalisado

    #grupo vídeo
    if (saltoanalisado[0]=='K' or saltoanalisado[0]=='M' or saltoanalisado[0]=='O' or saltoanalisado[0]=='V'):
    #separando VRSPM pré e pós
        if (int(saltoanalisado[1:3]) < 11):
            if (contvpre == 0):
                vpre= VRSPM        #controle pré
                contvpre = contvpre + 1
            else:
                vpre= np.concatenate((vpre,VRSPM))
        if (int(saltoanalisado[1:3]) > 10):
            if (contvpos == 0):
                vpos = VRSPM        #controle pos
                contvpos = contvpos + 1
            else:
                vpos = np.concatenate((vpos,VRSPM))


    saltos=saltos+1

precontrole = cpre
poscontrole = cpos
prevideo = vpre
posvideo = vpos

distanciapernascpre = cpre[:,5]/cpre[:,4]
distanciapernascpos = cpos[:,5]/cpos[:,4]
distanciapernasvpre = vpre[:,5]/vpre[:,4]
distanciapernasvpos = vpos[:,5]/vpos[:,4]

precontrole[:,4] =  distanciapernascpre
poscontrole[:,4] = distanciapernascpos
prevideo[:,4] = distanciapernasvpre
posvideo[:,4] = distanciapernasvpos

saidaanova = np.hstack((precontrole, poscontrole, prevideo, posvideo))

saidaanovaprepos = pd.DataFrame(saidaanova)

filepath = dir_atual + '/Analise estatistica/' + 'saidaanovaprepos.xlsx'

saidaanovaprepos.to_excel(filepath, index=False)

#fmt = '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f'
#np.savetxt(dir_atual + '/Analise estatistica/' + 'saidaanova.txt', saidaanova, fmt=fmt, delimiter=',')