# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 09:56:20 2021

@author: Rafael Luiz Martins Monteiro

Processamento de dados IC FAPESP 2021 - Instrução por vídeo
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import spm1d
import math

dir_atual = os.getcwd()
dir_working = sorted(os.listdir(dir_atual + '/working3d/'))
saltos = 115
#while(saltos<len(dir_working)):
saltoanalisado = dir_working[saltos]
dat = np.loadtxt(dir_atual + '/working3d/' + saltoanalisado)
framepe = np.loadtxt('framepe.txt')
cmdat=dat[:,75:]
#calculando velocidade de cada momento
cont=0  
VP=0    
VR = np.empty(len(cmdat[:,0])-1)
VML=np.empty(len(cmdat[:,0])-1)
VAP=np.empty(len(cmdat[:,0])-1)
VV=np.empty(len(cmdat[:,0])-1) 
angjoelho = np.empty(len(cmdat[:,0])-1)
                                   
while (cont <= len(cmdat[:,0])-2):
    #calculando Velocidades
    cont += 1
    DAPM=float(cmdat[cont,0])-float(cmdat[cont-1,0])  #Deslocamento AP do momento
    VAP[cont-1]=abs(DAPM)/(1/120)
    DMLM=float(cmdat[cont,1])-float(cmdat[cont-1,1])  #Deslocamento ML do momento
    VML[cont-1]=abs(DMLM)/(1/120)
    DVM=float(cmdat[cont,2])-float(cmdat[cont-1,2]) #Deslocamento V do momento
    VV[cont-1]=abs(DVM)/(1/120)
    DRM=(float(DMLM**2)+float(DVM**2)+float(DAPM**2))**0.5      #Deslocamento R do momento
    VMM=abs(DRM)/(1/120)                                           #Velocidade momentânea
    VR[cont-1] = VMM

    if (cont == framepe[saltos]+4 or cont == framepe[saltos]+6): #tem um salto em que só tem 4 frames entre o contato do pé e o fim do salto
        VMLP = max(VML[:cont])         #velocidade mediolateral pico
        VRP = max(VR[:cont])           #velocidade resultante pico
        LVMLP = VML[:cont].argmax()
        LVRP = VR[:cont].argmax()
        
    #calculando ângulo do joelho da perna relativa ao lado do salto, do momento 0 ao último contato com o solo
    #utilizando lei dos cossenos a^2=b^2+c^2-2*b*c*cos(ang)
    if(saltoanalisado[-4]=='D'):   #perna direita
        dist1011=(((dat[cont-1,27]-dat[cont-1,30])**2+(dat[cont-1,28]-dat[cont-1,31])**2+(dat[cont-1,29]-dat[cont-1,32])**2)**0.5)
        dist1012=(((dat[cont-1,27]-dat[cont-1,33])**2+(dat[cont-1,28]-dat[cont-1,34])**2+(dat[cont-1,29]-dat[cont-1,35])**2)**0.5)
        dist1112=(((dat[cont-1,30]-dat[cont-1,33])**2+(dat[cont-1,31]-dat[cont-1,34])**2+(dat[cont-1,32]-dat[cont-1,35])**2)**0.5)
        cos = ((dist1011**2)+(dist1112**2)-(dist1012**2))/(2*dist1011*dist1112)
        angjoelho[cont-1] = np.arccos(cos) 
        angjoelho[cont-1] = angjoelho[cont-1]*(180/math.pi)
    if(saltoanalisado[-4]=='E'):   #perna esquerda
        dist1314=(((dat[cont-1,36]-dat[cont-1,39])**2+(dat[cont-1,37]-dat[cont-1,40])**2+(dat[cont-1,38]-dat[cont-1,41])**2)**0.5)
        dist1315=(((dat[cont-1,36]-dat[cont-1,42])**2+(dat[cont-1,37]-dat[cont-1,43])**2+(dat[cont-1,38]-dat[cont-1,44])**2)**0.5)
        dist1415=(((dat[cont-1,39]-dat[cont-1,42])**2+(dat[cont-1,40]-dat[cont-1,43])**2+(dat[cont-1,41]-dat[cont-1,44])**2)**0.5)
        cos = ((dist1314**2)+(dist1415**2)-(dist1315**2))/(2*dist1314*dist1415)
        angjoelho[cont-1] = np.arccos(cos) 
        angjoelho[cont-1] = angjoelho[cont-1]*(180/math.pi)
        

angjoelho = angjoelho[:int(framepe[saltos])]
angjoelhomin = min(angjoelho)                 #encontrando menor ângulo do joelho
angjoelhospm = spm1d.util.interp(angjoelho, Q=101)  #normalizando na série temporal (0-100%) 

plt.plot(angjoelho)
plt.figure()
plt.plot(angjoelhospm)

#calculando espaçamento entre as pernas
#No artigo de Ibrahim, 2019 ele utiliza "palpated greater trochanter to the ground"
#Para adaptação da medida da perna será utilizada a dist entre os pontos 10-11-12; porém o 12 estará com a medida z estrapolada para o menor ponto do pé do atleta que neste caso é o z o ponto 25 que é o calcanhar do atleta
tamperna = (((dat[0,27]-dat[0,30])**2+(dat[0,28]-dat[0,31])**2+(dat[0,29]-dat[0,32])**2)**0.5) + (((dat[0,30]-dat[0,33])**2+(dat[0,31]-dat[0,34])**2+(dat[0,32]-dat[0,74])**2)**0.5)
tampernae = (((dat[0,36]-dat[0,39])**2+(dat[0,37]-dat[0,40])**2+(dat[0,38]-dat[0,41])**2)**0.5) + (((dat[0,39]-dat[0,42])**2+(dat[0,40]-dat[0,43])**2+(dat[0,41]-dat[0,65])**2)**0.5)
tampernaf = (tamperna + tampernae)/2  #média do tamanho de ambas as pernas. Para evitar variação fazer a média do tamanho da perna de todos os saltos do mesmo sujeito 

#calculando distância entre os calcanhares no eixo y (mediolateral) na preparação para o salto
#distpernas = (((dat[0,33]-dat[0,42])**2+(dat[0,34]-dat[0,43])**2+(dat[0,35]-dat[0,44])**2)**0.5)
distcalcanharesy = abs(dat[0,73] - dat[0,64])

#calculando a realização do passo frontal pela distância no eixo x (anteroposterior) no frame 0 e no 'framepe'(último momento de contato do pé ipsilateral ao salto)
if(saltoanalisado[-4]=='E'):
    passofrontal = abs(dat[0,57]-dat[int(framepe[saltos]),57]) #ponto 20
if(saltoanalisado[-4]=='D'):
    passofrontal = abs(dat[0,66]-dat[int(framepe[saltos]),66]) #ponto 23

#calculando ângulo de saída frontal (ângulo do CM entre o momento de saída inicial e o local da velocidade resultante pico)
xycmdat=cmdat[0,0:2]
xycmdatvp=cmdat[LVRP,0:2]
valory=xycmdatvp[1]
valorx=xycmdat[0]
dist12=(((xycmdat[0]-valorx)**2+(xycmdat[1]-valory)**2)**0.5)
dist13=(((xycmdat[0]-xycmdatvp[0])**2+(xycmdat[1]-xycmdatvp[1])**2)**0.5)
cos = dist12/dist13
angsaidafrontal= np.arccos(cos) 
angsaidafrontal = angsaidafrontal*(180/math.pi)

fig = plt.figure()

plt.subplot(2, 2, 1)
plt.plot(VR)
plt.title('VR')

plt.subplot(2, 2, 2)
plt.plot(VAP)
plt.title('VAP')

plt.subplot(2, 2, 3)
plt.plot(VML)
plt.title('VML')

plt.subplot(2, 2, 4)
plt.plot(VV)
plt.title('VV')

#variáveis para salvar em cada salto
VRSPM = spm1d.util.interp(VR[:LVRP+1], Q=101)      #normalizando temporalmente (0-100%)
VMLSPM = spm1d.util.interp(VML[:LVMLP+1], Q=101)
VRP
VMLP
TVRP=(LVRP+1)/120                   #tempo para atingir velocidade pico
TVMLP=(LVMLP+1)/120                 #tempo para atingir velocidade pico
tampernaf
distcalcanharesy
passofrontal
angsaidafrontal
angjoelhospm
angjoelhomin

#fazer um save para cada dado e guardar na pasta workingprocessados

    #saltos = saltos+1
#plt.figure()
#plt.plot(cmdat[:,0])
#plt.figure()
#plt.plot(cmdat[:,1])
#plt.figure()
#plt.plot(cmdat[:,2])
    
#saida = np.hstack((dat,CM))
#fmt = '%d', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f'     
#np.savetxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0cm.dat', saida, fmt=fmt)
#print( 'Centro de massa do' f'{saltoanalisado} calculado com sucesso')
#saltos = saltos+1