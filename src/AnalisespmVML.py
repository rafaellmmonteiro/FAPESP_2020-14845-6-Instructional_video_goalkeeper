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

CALCULO DO SPM PARA VML
"""

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
    VRSPM = dat[:,1]
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

#Grupo controle
cprem=np.empty([1, 101])
cpredp=np.empty([1, 101])
cposm=np.empty([1, 101])
cposdp=np.empty([1, 101])
cont=0

while (cont<101):
    cprem[0,cont]=np.mean(cpre[:,cont])
    cposm[0,cont]=np.mean(cpos[:,cont])
    cpredp[0,cont]=np.std(cpre[:,cont])
    cposdp[0,cont]=np.std(cpos[:,cont])
    cont=cont+1


#realizando o teste SPM
#######################################################
t  = spm1d.stats.ttest_paired(cpos, cpre)
ti = t.inference(alpha=0.05, two_tailed=False)
ti.plot()
spm1d.plot.plot_spmi_p_values(ti)
print(t)
print( ti )
print( ti.clusters )
plt.xlabel('Ciclo (%)', size= '15')
plt.title('Ciclo SPM', size='20')
#######################################################

    
#Plotando gráfico
fig1, f1_axes = plt.subplots(ncols=1, nrows=1)
cprem=cprem.T
cpredp=cpredp.T
cposm=cposm.T
cposdp=cposdp.T
#f1_axes.plot(radm)
plt.plot(cprem, label = 'Grupo contole pós')
t = np.linspace(0,len(cprem),len(cprem), False)
plt.errorbar(t, cprem, color = 'r')
plt.fill_between(t, cprem[:,0]+cpredp[:,0], cprem[:,0]-cpredp[:,0], color = 'lightcoral', alpha=0.5)
plt.plot(cposm, label = 'Grupo controle pré')
plt.errorbar(t, cposm, color = 'b')
plt.fill_between(t, cposm[:,0]+cposdp[:,0], cposm[:,0]-cposdp[:,0], color = 'cornflowerblue', alpha = 0.5)
plt.xlabel('Ciclo (%)')
plt.ylabel('Velocidade do centro de massa')
plt.title('Velocidade mediolateral do grupo controle pré e pós')
plt.legend(loc=2, prop={'size': 10})


#Grupo vídeo
vprem=np.empty([1, 101])
vpredp=np.empty([1, 101])
vposm=np.empty([1, 101])
vposdp=np.empty([1, 101])
cont=0

while (cont<101):
    vprem[0,cont]=np.mean(vpre[:,cont])
    vposm[0,cont]=np.mean(vpos[:,cont])
    vpredp[0,cont]=np.std(vpre[:,cont])
    vposdp[0,cont]=np.std(vpos[:,cont])
    cont=cont+1


#realizando o teste SPM
#######################################################
t  = spm1d.stats.ttest_paired(vpos, vpre)
ti = t.inference(alpha=0.05, two_tailed=False)
plt.figure()
ti.plot()
spm1d.plot.plot_spmi_p_values(ti)
print(t)
print( ti )
print( ti.clusters )
plt.xlabel('Ciclo (%)', size= '15')
plt.title('Ciclo SPM', size='20')
#######################################################

    
#Plotando gráfico
fig1, f1_axes = plt.subplots(ncols=1, nrows=1)
vprem=vprem.T
vpredp=vpredp.T
vposm=vposm.T
vposdp=vposdp.T
#f1_axes.plot(radm)
plt.plot(vprem, label = 'Grupo vídeo pós')
t = np.linspace(0,len(vprem),len(vprem), False)
plt.errorbar(t, vprem, color = 'r')
plt.fill_between(t, vprem[:,0]+vpredp[:,0], vprem[:,0]-vpredp[:,0], color = 'lightcoral', alpha=0.5)
plt.plot(vposm, label = 'Grupo vídeo pré')
plt.errorbar(t, vposm, color = 'b')
plt.fill_between(t, vposm[:,0]+vposdp[:,0], vposm[:,0]-vposdp[:,0], color = 'cornflowerblue', alpha = 0.5)
plt.xlabel('Ciclo (%)')
plt.ylabel('Velocidade do centro de massa')
plt.title('Velocidade mediolateral do grupo vídeo pré e pós')
plt.legend(loc=2, prop={'size': 10})

#realizando o teste SPM
#######################################################
t  = spm1d.stats.ttest_paired(cpre, vpre)
ti = t.inference(alpha=0.05, two_tailed=False)
plt.figure()
ti.plot()
spm1d.plot.plot_spmi_p_values(ti)
print(t)
print( ti )
print( ti.clusters )
plt.xlabel('Ciclo (%)', size= '15')
plt.title('Ciclo SPM', size='20')
#######################################################

#realizando o teste SPM
#######################################################
t  = spm1d.stats.ttest_paired(cpos, vpos)
ti = t.inference(alpha=0.05, two_tailed=False)
plt.figure()
ti.plot()
spm1d.plot.plot_spmi_p_values(ti)
print(t)
print( ti )
print( ti.clusters )
plt.xlabel('Ciclo (%)', size= '15')
plt.title('Ciclo SPM', size='20')
#######################################################