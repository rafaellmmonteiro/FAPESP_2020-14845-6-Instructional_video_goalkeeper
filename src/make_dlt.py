# -*- coding: utf-8 -*-
import os
from glob import glob
import numpy as np
from numpy.linalg import inv

dir_atual = os.getcwd()     #encontra o caminho
img_dir = '/snap_calib/'
dir_atual = os.getcwd()            #pq tem dois?
dir_dat2d = dir_atual + img_dir      #adiciona ao caminho
dir_cams = sorted(os.listdir(dir_dat2d))     #procura e faz uma lista com oq tem dentro do caminho

alist = []

for i in dir_cams:
    dir_1 = dir_dat2d + i          #vai rodando a lista, i é cada linha do dir_cams, ou seja C1 e C2
    full_path = os.path.join(dir_1, '*.dat')    #junta o c1 com o *.dat     

    for fname in sorted(glob(full_path)):              # o glob faz uma lista de todos os aquivos .dat do diretório
        alist.append(np.loadtxt(fname, dtype=int))     # lendo os dois arquivos C1 e C2

cp2d = np.asarray(alist)                               # transforma o arquivo lido em np array

try:
    np.savetxt(dir_atual+'/infos_calib/cp2d_ref_to_checkError.dat',
               cp2d, fmt='%d')                                           #tenta salvar arquivo no arquivo cp2dcheckerror
except Warning:
    print('WARNING!!! cp2d_ref_to_checkError.dat has not been copied to the directory ./infos_calib') #nao existe o arquivo para ser salvo

ref_dir = '/infos_calib/'           #define caminho
dir_3dref = glob(os.path.join(dir_atual + ref_dir, '*.ref'))[0]       #procura todos os arquivos .ref na pasta info calib
cp3d = np.loadtxt(dir_3dref)          #abre o arquivo de referencia

try:
    cp2d = np.loadtxt(dir_atual + ref_dir + 'cp2d_ref_to_checkError.dat')   # tenta abrir o check error
except:
    print('WARNING!!! infos_calib directory .dat file was not loaded')     #não tem checkerror

try:
    os.mkdir(dir_atual + ref_dir + 'dlt_to_calib/')              #cria pasta nova chamada dlt_to_calib
    print(f'Directory dlt_cal create in: {dir_atual + ref_dir}')
except:
    # print(f'Directory dlt_cal exist in {dir_atual + ref_dir}')
    pass


def dlt_calib(cp3d, cp2d):
    '''Calibration DLT
    =============================================================================
    DLT 3D
    Calcula os parametros do DLT
    para executá-la, digite os comandos abaixos
    import rec3d
    DLT = rec3d.dlt_calib(cp3d, cd2d)
    onde:
    DLT  = vetor linha com os parametros do DLT calculados
    [L1,L2,L3...L11]
    cp3d = matriz retangular com as coordenadas 3d (X, Y, Z) dos pontos (p) do calibrador
    Xp1 Yp1 Zp1
    Xp2 Yp2 Zp2
    Xp3 Yp3 Zp3
    .   .   .
    .   .   .
    Xpn Ypn Zpn
    cp2d = matriz retangular com as coordenadas de tela (X, Y) dos pontos (p) do calibrador
    xp1 yp1
    xp2 yp2
    xp3 yp3
    .   .
    .   .
    xpn ypn
    =============================================================================
    '''
    cp3d = np.asarray(cp3d)       #transforma em np array
    if np.size(cp3d, 1) > 3:      
        cp3d = cp3d[:, 1:]        #reetira a primeira coluna pois é o numero de pontos

    m = np.size(cp3d[:, 0], 0)    #aqui pode ser m = np.size(cp3d, 0), da na mesma
    M = np.zeros([m * 2, 11])
    N = np.zeros([m * 2, 1])
    cp2d = np.asarray(cp2d)
    if np.size(cp2d, 1) > 1:
        DLTs = []
        for j in range(np.size(cp2d, 0)):
            cp2d_a = cp2d[j, :]
            cp2d_a = np.reshape(cp2d_a, (m, 2))

            for i in range(m):
                M[i*2, :] = [cp3d[i, 0], cp3d[i, 1], cp3d[i, 2], 1, 0, 0, 0, 0, -cp2d_a[i, 0]
                             * cp3d[i, 0], -cp2d_a[i, 0] * cp3d[i, 1], -cp2d_a[i, 0] * cp3d[i, 2]]

                M[i*2+1, :] = [0, 0, 0, 0, cp3d[i, 0], cp3d[i, 1], cp3d[i, 2], 1, -
                               cp2d_a[i, 1] * cp3d[i, 0], -cp2d_a[i, 1] * cp3d[i, 1], -cp2d_a[i, 1] * cp3d[i, 2]]

                N[[i*2, i*2+1], 0] = cp2d_a[i, :]

            Mt = M.T
            M1 = inv(Mt.dot(M))
            MN = Mt.dot(N)

            DLT = (M1).dot(MN).T
            DLTs.append(DLT.tolist())
            # np.savetxt(dir_atual + ref_dir + f'cam{j+1}.cal', DLT, fmt='%.6f')

    DLTs_save = np.array(DLTs).reshape((len(DLTs), -1))
    path2save_dlt = dir_atual + ref_dir + 'dlt_to_calib/'
    np.savetxt(path2save_dlt + 'dlt_all_cams.cal', DLTs_save, fmt='%.6f')

    return DLTs


if __name__ == '__main__':
    dlt_calib(cp3d, cp2d)
    print('File \"dlt_all_cams.cal\" saved in directory: ./infos_calib/dlt_to_calib')
