# -*- coding: utf-8 -*-

import pdb
import shutil
import os
from os import walk
import glob
import numpy as np
from numpy.linalg import inv
from iteration_utilities import deepflatten

dir_atual = os.getcwd()
dir_infos_calib = '/infos_calib/'
cp2d_ref_to_checkError = 'cp2d_ref_to_checkError.dat'
refcal3d = 'refcal.ref'
dir_dlt2calib = 'dlt_to_calib/'
arq_dlts = 'dlt_all_cams.cal'
dir_dat2rec = '/for3d/'
working = '/reffor3d/working/'
dir_cams1 = sorted(os.listdir(dir_atual + '/reffor3d/'))
dir_working = sorted(os.listdir(dir_atual + '/reffor3d/' + '/working/'))

for file in os.listdir(dir_atual + '/reffor3d/'):
        if file.endswith(".txt"):
            Reccalibname=file
            Reccalib=open('.' + '/reffor3d/' + file, 'r').readlines()
            nreccalib = len(Reccalib)
cont=n=0
while (cont < nreccalib/2):
    #copiando arquivos para pastas 'c1' e 'c2' dentro de 'for3d'
    cont=cont+1
    Reccalibc1=Reccalib[n]
    Reccalibc1 = Reccalibc1.replace('\n', "")
    os.chdir(dir_atual + working + Reccalibc1)
    openpose = glob.glob('*_0cm.dat')
    origem = dir_atual + working + Reccalibc1 +'/'+openpose[0]
    dircam=1
    shutil.copy(origem, dir_atual+'/for3d/c'+ str(dircam))
    n=n+1
    Reccalibc2=Reccalib[n]
    n=n+1
    Reccalibc2 = Reccalibc2.replace('\n', "")
    os.chdir(dir_atual + working + Reccalibc2)
    openpose = glob.glob('*_0cm.dat')
    origem = dir_atual + working + Reccalibc2 +'/'+openpose[0]
    dircam=2
    shutil.copy(origem, dir_atual+'/for3d/c'+ str(dircam))
    nametosave1= Reccalibc1[-3:] 
    nametosave2= Reccalibc1[3]
    nametosave3= nametosave1 + nametosave2
    
    os.chdir(dir_atual)       
    #ler arquivo openpose 2d
    def loadfile2d(alldata=True, pathfile2d='./for3d/c1/dvideow_people_0cm.dat', wframe=1, wpoint=1):
        if alldata is True:
            file2dload = np.loadtxt(pathfile2d)
            file2dload = file2dload[:, 1:]
        else:
            file2dload = np.loadtxt(pathfile2d)
            file2dload = file2dload[:, 1:]
            try:
                file2dload = file2dload[wframe-1, 2*wpoint-2:2*wpoint]
            except OSError:
                print('Frame or keypoint does not exist!')
        
        return file2dload
    
    #le os arquivos dentro da pasta  for3d
    def files2_2d():
        try:
            dir_cams = sorted(os.listdir(dir_atual + dir_dat2rec))
            ncamdir = len(dir_cams)   #sem utilização
            arq_filesdat2rec = []
            arq_foldersdat2d = []
            for i in range(len(dir_cams)):
                foldernames, _, filenames = next(
                    walk(dir_atual + dir_dat2rec + dir_cams[i]))   
                filesindir = sorted(filenames)
                arq_filesdat2rec.append(filesindir)
                arq_foldersdat2d.append(foldernames)
            matdat2r3d = np.asarray(arq_filesdat2rec)  #retorna os dois arquivos para reconstrução
        except OSError:
            print('Directory of .dat files for reconstruction not found')
        return matdat2r3d, dir_cams, arq_foldersdat2d
    
    
    try:
        dat_checkerror = np.loadtxt(dir_atual + dir_infos_calib + cp2d_ref_to_checkError)
    
        refcal = np.loadtxt(dir_atual + dir_infos_calib + refcal3d)
        refcal = refcal[:, 1:]
    except Warning:
        print(f'Calibration error check not performed. Check if the file {cp2d_ref_to_checkError} exists!')
    
    # Load file DLTs
    def loadlts(pathdir='./infos_calib/dlt_to_calib/dlt_all_cams.cal'):
        try:
            dlts = np.loadtxt(dir_atual + dir_infos_calib + dir_dlt2calib + arq_dlts)
        except OSError:
            print(f'Cannot open {dir_atual + dir_infos_calib + dir_dlt2calib + arq_dlts}')
        return dlts
    
    # Calculation 3D by pixels data and dlt
    def rec3d(DLTs, cc2ds):
        '''rec3d
            dlts: matrix MxN (M = number of cams DLT and, N = 11)
            cc2ds: matrix with 2D pixel coordinates of each keypoint - rows are the frames and 2*columns are the markers 
        '''
        DLTs = np.asarray(DLTs)
        cc2ds = np.asarray(cc2ds)
    
        m = len(DLTs)
        M = np.zeros([2 * m, 3])  # number of rows
        N = np.zeros([2 * m, 1])  # number of columns
    
        for i in range(m):
            M[i*2, :] = [DLTs[i, 0]-DLTs[i, 8]*cc2ds[i, 0], DLTs[i, 1] -
                         DLTs[i, 9]*cc2ds[i, 0], DLTs[i, 2]-DLTs[i, 10]*cc2ds[i, 0]]
    
            M[i*2+1, :] = [DLTs[i, 4]-DLTs[i, 8]*cc2ds[i, 1], DLTs[i, 5] -
                           DLTs[i, 9]*cc2ds[i, 1], DLTs[i, 6]-DLTs[i, 10]*cc2ds[i, 1]]
    
            Np1 = cc2ds[i, :].T
            Np2 = [DLTs[i, 3], DLTs[i, 7]]
            N[[i*2, i*2+1], 0] = Np1 - Np2
    
        cc3d = inv(M.T.dot(M)).dot((M.T.dot(N)))
    
        return cc3d
    
    
    # def filbutter(dat, fc=59, fs=1000, filtorder=4, typefilt='low'):
    #     from scipy import signal
    
    #     nl, nc = dat.shape
    #     # fc=59  # Cut-off frequency of the filter
    #     w = fc/(fs/2)  # Normalize the frequency
    #     b, a = signal.butter(filtorder, w, typefilt)
    
    #     datf = np.zeros([nl, nc], dtype=float)
    #     for i in range(nc):
    #         datf[:, i] = signal.filtfilt(b, a, dat[:, i])
    
    #     return datf
    
    
    if __name__ == '__main__':
        dlts = loadlts()
        ncams = len(dlts)
        npoints = len(dat_checkerror[0])//2
        cam_to_reshape = []
    
        try:
            for i in range(ncams):
                cam_to_reshape.append(np.reshape(dat_checkerror[i], (npoints, 2)))
            # pdb.set_trace()
    
            cc3d_err = []
            for i in range(npoints):
                ptorec = []
                for j in range(ncams):
                    ptorec.append(cam_to_reshape[j][i])
                cc3d_err.append(rec3d(dlts, ptorec))
            cc3d_error = list(deepflatten(cc3d_err))
    
            np.savetxt('arqchek_error.3d', np.reshape(
                np.asarray(cc3d_error), (npoints, 3)), fmt='%f')
    
            np.set_printoptions(suppress=True)
    
            # pdb.set_trace()
            mat_error = refcal - np.reshape(np.asarray(cc3d_error), (npoints, 3))
            mea_error = np.round(np.mean(np.abs(mat_error), 0), 3)
            print(f'Matrix of the errors: \n{mat_error}')
            print(
                f'Mean absolute error X: {mea_error[0]}; Y: {mea_error[1]}; Z: {mea_error[2]}; overall: {np.mean(mea_error)}')
            # pdb.set_trace()
            # with open('arqchek_error2.3d', 'w') as f:
            #     for elem in cc3d_err:
            #         for i in elem:
            #             f.write('%f ' % i)
            #         f.write('\n')
        except Warning:
            print('The reconstruction error check is not verified!')
    
        matdat2r3d, dir_cams, foldernames = files2_2d()
        # pdb.set_trace()
        
        listdatr3d = matdat2r3d.tolist()
        for i in range(len(dir_cams)):
            for j in range(np.size(matdat2r3d, 1)):
                listdatr3d[i][j] = '.' + dir_dat2rec + dir_cams[i] + '/' + matdat2r3d[i, j]
    
        # Load 1 file 2d and check the numbers of keypoints
        c1_all_to_check = loadfile2d(alldata=True, pathfile2d=listdatr3d[0][0])
        nkeyp = c1_all_to_check.shape[1] // 2
        nframeslin = c1_all_to_check.shape[0]
        nfdir = matdat2r3d.shape[1]
        # print(f'Number of keypoints is {nkeyp}')
    
        # pdb.set_trace()    
        for i_finfold in range(nfdir):
            mat_keyps = np.zeros((nframeslin, nkeyp*3))
            for i_keyp in range(nkeyp):
                conc_frames = []
                for i_frames in range(nframeslin):
                    # print(f'i_frames {i_frames}')
                    conc_cams = []
                    for i_cam in range(ncams):
                        # print(f'i_cam {i_cam}')
                        camload = loadfile2d(alldata=False, pathfile2d=listdatr3d[i_cam][i_finfold], wframe=i_frames+1, wpoint=i_keyp+1)
                        conc_cams.append(camload)
                    recpoint = rec3d(dlts, conc_cams).T
                    conc_frames.append(recpoint)
                conc_frames = np.reshape(np.asarray(conc_frames), (nframeslin, 3))
                mat_keyps[:, 3*(i_keyp+1)-3:3*(i_keyp+1)] = conc_frames
            # pdb.set_trace()
          
        nametosave = f'./working3d/{str(nametosave3)}.3d'
        try:
            np.savetxt(nametosave, mat_keyps, fmt='%f')
        except:
            os.mkdir('working3d')
            np.savetxt(nametosave, mat_keyps, fmt='%f')

