import c3d
import numpy as np
import pandas as pd
import ezc3d
import matplotlib.pyplot as plt
import os

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
dir_cams1 = sorted(os.listdir(dir_atual + '/reffor3d/'))
dir_working3d = sorted(os.listdir(dir_atual + '/working3d/'))
nworking3d = len(dir_working3d)
n=0
while (n < nworking3d):
    # lend arquivo e criando c3d vazio
    c3d = ezc3d.c3d()
    os.chdir(dir_atual + '/working3d/')
    dat = open(dir_working3d[n],'r+',)
    os.chdir(dir_atual) 
    dat = pd.read_csv(dat, sep= ' ',header=None)
    dat = dat.to_numpy()
    tdat= len(dat)
    dat=dat[:tdat-1,:]
    dat = dat*1000
    #dat = filtro(dat, fc=3, fs=120, filtorder=4, typefilt='low')
    #p18=dat[:,56:57]
    #p18f = filtro(p18, fc=6, fs=400, filtorder=4, typefilt='low')
    #plt.plot(p18)
    #plt.plot(p18f)
    
    
    # escrevendo
    c3d['parameters']['POINT']['RATE']['value'] = [tdat]
    c3d['parameters']['POINT']['LABELS']['value'] = ('point1', 'point2', 'point3', 'point4', 'point5','point6','point7','point8','point9','point10','point11','point12','point13','point14','point15','point16','point17','point18','point19','point20','point21','point22','point23','point24','point25','point26')
    c3d['data']['points'] = np.random.rand(4, 26, tdat-1)
    cont=cont1=cont2=0
    col=0
    col1=1
    col2=2
    while (cont<26):
        c3d['data']['points'][0, cont, :] = dat[:,col]
        cont=cont+1
        col=col+3
    while (cont1<26):
        c3d['data']['points'][1, cont1, :] = dat[:,col1]
        cont1=cont1+1
        col1=col1+3
    while (cont2<26):
        c3d['data']['points'][2, cont2, :] = dat[:,col2]
        cont2=cont2+1
        col2=col2+3
    nametosave= dir_working3d[n]
    nametosave = nametosave[0:4]
    c3d.write(f'./workingc3d/{str(nametosave)}')
    n=n+1






#oi = open('salto21.3d','r+',)
#dat1 = pd.read_csv(oi, sep= ' ',header=None)
#dat = dat1.to_numpy()
#dat = dat[:,2:]
#writer = c3d.Writer()
#for _ in range(1000):
#    writer.add_frames(dat)
#with open('random-points.c3d', 'wb') as h:
#    h.write(dat1) 
