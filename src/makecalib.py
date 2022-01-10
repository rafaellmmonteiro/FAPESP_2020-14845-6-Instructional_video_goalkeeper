# -*- coding: utf-8 -*-

import pdb
# import pandas as pd
# import scipy as sp
#import cv2
import os
import shutil
import glob
from pathlib import Path
path = Path('Pasta')
#import pyautogui
import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np
from iteration_utilities import deepflatten

dir_atual = os.getcwd()
img_dir = '/snap_calib/'
try:
    dir_images = dir_atual+img_dir
except:
    print(f'ERROR! Directory {img_dir} not found!')

os.chdir(dir_images)

for i in range(len(os.listdir('.'))):
    cam_id = 'c'+str(i+1)
    os.chdir(dir_images+cam_id)
    
    targetextension = '*.dat'
    if len(glob.glob(targetextension)) != 0:
        os.remove(f'{os.getcwd()}/{cam_id+targetextension[1:]}')
    
    xy = []

    for j in range(len(os.listdir())):
        png_files = sorted(glob.glob('*.png'))
        # Para carregar uma sequencia de imagens png de um diretorio
        img = imread(png_files[j])
        # print(img1)
        imgplot = plt.imshow(img)
        plt.title('MouseButton.LEFT: mark | MouseButton.RIGHT: unmark | MouseButton.MIDDLE: stop')
        pix_cal = plt.ginput(n=50)
#        import pdb; pdb.set_trace()
        plt.close()
        xy.append(pix_cal)
        
        globals()[cam_id] = xy
        npxy = list(deepflatten(globals()[cam_id]))

        #pdb.set_trace()

        np.savetxt(cam_id+'.dat', npxy, delimiter=' ', fmt='%1.6f')

#pdb.set_trace()
#plt.show()

# Para rodar um video
#import cv2
#import os
#cap = cv2.VideoCapture('c1_cal.mp4')
#if (cap.isOpened()== False):
#    print('Error opening video file')
#
#while (cap.isOpened()):
#    ret, frame = cap.read()
#    if ret == True:
#        cv2.imshow('Frame', frame)
#        key = cv2.waitKey(1)
#        if key == ord('q'):
#            break
#        if key == ord('p'):
#            cv2.waitKey(-1) #wait until any key is pressed
#cap.release()
#
