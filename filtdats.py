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

def filtro(dat, fc=59, fs=1000, filtorder=4, typefilt='low'):
    import numpy as np
    from scipy import signal
    
    nl, nc = dat.shape
    # fc=59  # Cut-off frequency of the filter
    w = fc/(fs/2)  # Normalize the frequency
    b, a = signal.butter(filtorder, w, typefilt)
    
    datf = np.zeros([nl, nc], dtype=float)
    for i in range(nc):
        datf[:,i] = signal.filtfilt(b, a, dat[:,i])
   
    return datf

dir_atual = os.getcwd()
dir_working = sorted(os.listdir(dir_atual + '/reffor3d/' + '/working/'))
saltos = 0
while(saltos<len(dir_working)):
    saltoanalisado = dir_working[saltos]
    dat = np.loadtxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0c.dat')
    dat = dat[:-1, 1:]
    datf = filtro(dat, fc=7, fs=120, filtorder=4, typefilt='low') 
    save = np.loadtxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0c.dat')
    save = save[:-1,:]
    save[:,1:] = datf
    fmt = '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f'
    np.savetxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0f.dat', save, fmt=fmt)
    print( f'{saltoanalisado} filtrado com sucesso')
    saltos = saltos+1


