# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:18:12 2021

@author: Rafael Monteiro
"""
import pdb
import shutil
import os
from os import walk
import glob
import numpy as np
import scipy as sp
from scipy import interpolate
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from numpy.linalg import inv
from iteration_utilities import deepflatten

dir_atual = os.getcwd()
dir_working = sorted(os.listdir(dir_atual + '/reffor3d/' + '/working/'))
saltos = 0
while(saltos<len(dir_working)):
    saltoanalisado = dir_working[saltos]
    dat = np.loadtxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0.dat')
    dat = dat[:, 1:]
    y=0                                #seleciona qual coluna do dat ele vai processar
    while (y<dat.shape[1]):
        n=0
        #plt.figure()
        #plt.plot(dat[:,y])
        while (n<len(dat[:,y])-1):
            if (dat[n,y] != 0):
                erro = dat[n+1,y]-dat[n,y]
                erro = abs(erro)
                if (erro>20):
                    n1 = n
                    n=n+1
                    while (erro>20 and n<len(dat[:,y])-1):
                        erro = dat[n,y]-dat[n1,y]
                        erro = abs(erro)
                        if (erro>20):
                            dat[n,y]= 0
                            n=n+1 
            n=n+1
        
        fzero = np.where(dat[:,y]!=0)
        fzero = fzero[0] #transforma em np array
        try:
            fzeroi = fzero[0] #seleciona o valor inicial diferente de zero
            fzerof = fzero[len(fzero)-1]
        except:
            print(f'{saltoanalisado} contém coluna somente com zeros')
        y1 = dat[fzeroi:fzerof+1,y]       #selecionando o range de interpolação, excluindo inicio e fim com zeros
        x = np.arange(len(y1))
        idx = np.where(y1!=0)        #or np.nonzero(y) -- thanks DanielF
        try:
            f = interp1d(x[idx],y1[idx], kind = 'cubic')
        except:
            print(f'{saltoanalisado} apresentou erro na interpolação')
        ynew = f(x)
        cori = np.full((fzeroi, 1), 0)        #correção para quando começar os dados em zero
        tamcorf = len(dat[:,y])-fzerof-1
        corf = np.full((tamcorf, 1), 0)        #correção quando dados acabam em zero
        y1 = np.concatenate((cori[:,0], y1))
        y1 = np.concatenate((y1, corf[:,0]))
        ynew = np.concatenate((cori[:,0], ynew))
        ynew = np.concatenate((ynew, corf[:,0]))
        dat[:,y] = ynew
        y=y+1   
        #plt.plot(y1)
        #plt.plot(ynew)
        #plt.show()
    save = np.loadtxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0.dat')
    save[:,1:] = dat
    fmt = '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f'
    np.savetxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0.dat', save, fmt=fmt)
    print( f'{saltoanalisado} interpolado com sucesso')
    saltos = saltos+1


