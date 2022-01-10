# -*- coding: utf-8 -*-
"""Realiza a extração de coordenadas de tela em pixel
    Paulo R. P. Santiago
"""

import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
import glob
from iteration_utilities import deepflatten

dir_atual = os.getcwd()
img_dir = '/snap_calib/'

try:
    dir_images = dir_atual + img_dir
except:
    print(f'ERROR! Directory {img_dir} not found!')

os.chdir(dir_images)

for i in range(len(os.listdir('.'))):
    cam_id = 'c' + str(i + 1)
    os.chdir(dir_images + cam_id)

    targetextension = '*.dat'
    try:
        os.remove(f'{os.getcwd()}/{cam_id+targetextension[1:]}')
        print(
            f'All *.dat files have been removed from the {os.getcwd()}/{cam_id+targetextension[1:]}')
    except:
        pass

    xy = []
    png_files = sorted(glob.glob('*.png'))
    for j in range(len(os.listdir())):
        # Para carregar uma sequencia de imagens png de um diretorio
        img = imread(png_files[j])
        imgplot = plt.imshow(img)
        plt.title('Mouse.LEFT: mark | Mouse.RIGHT: unmark | Mouse.MIDDLE: stop')
        pix_cal = plt.ginput(n=50, timeout=500)
        # import pdb; pdb.set_trace()
        plt.close()
        xy.append(pix_cal)

        locals()[cam_id] = xy

        npxy = list(deepflatten(locals()[cam_id]))

    with open(cam_id + '.dat', 'w') as f:
        for item in npxy:
            f.write('%d ' % item)

        # np.savetxt(cam_id+'.dat', npxy, delimiter=' ', fmt='%1.6f')
