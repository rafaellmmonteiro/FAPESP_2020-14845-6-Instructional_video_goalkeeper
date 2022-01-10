#!/bin/env python3.8
# -*- coding: utf-8 -*-
'''
#########################################################################
Tabela de massas relativas e localizacao dos centros de gravidade de cada
segmento (de Leva P.)
de Leva P. Adjustments to Zatsiorsky-Seluyanov's segment inertia parameters.
J Biomech. 1996 Sep;29(9):1223-30.
doi: 10.1016/0021-9290(95)00178-6. PMID: 8872282.
http://oregonstate.edu/instruct/exss323/CM_Lab/Center%20of%20Mass.htm
http://oregonstate.edu/instruct/exss323/CM_Lab/bsp_deleva.htm

#########################################################################		
Segment Length Percents (from proximal endpoint):			
Segment         Males	Females	    Endpoints
Head & Neck     50.02	48.41	    Top of Head - C7
Trunk	        43.10	37.82	    MidS - MidH
Upper Arm	    57.72	57.54	    SJC - EJC
Forearm	        45.74	45.59	    EJC - WJC
Hand	        79.00	74.74	    WJC - MCPIII
Thigh	        40.95	36.12	    HJC - KJC
Shank	        43.95	43.52	    KJC - AJC
Foot	        44.15	40.14	    Heel - Toe
#########################################################################
Segment Mass Percents:		
Segment	        Males	Females
Head & Neck	    6.94	6.68
Trunk	        43.46	42.58
Upper Arm	    2.71	2.55
Forearm	        1.62	1.38
Hand	        0.61	0.56
Thigh	        14.16	14.78
Shank	        4.33	4.81
Foot	        1.37	1.29
'''
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pdb

def main(dat=sys.argv[1:]):
    dat = np.loadtxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0f.dat')
    dat = dat[:,1:]

    cg_cab = dat[:,0:2] #Nose
    olho_d = dat[:,30:32] #REye
    olho_e = dat[:,32:34] #LEye
    orelha_d = dat[:,34:36] #REar
    orelha_e = dat[:,36:38] #LEar
    neck = dat[:,2:4] #pescoco
    midhip = dat[:,16:18] #MidHip
    ombro_d = dat[:,4:6] #RShoulder
    ombro_e = dat[:,10:12] #LShoulder
    cotovelo_d = dat[:,6:8] #RElbow
    cotovelo_e = dat[:,12:14] #LElbow
    punho_d = dat[:,8:10] #RWrist
    punho_e = dat[:,14:16] #LWrist
    quadril_d = dat[:,18:20] #RHip
    quadril_e = dat[:,24:26] #LHip
    joelho_d = dat[:,20:22] #RKnee
    joelho_e = dat[:,26:28] #LKnee
    tornozelo_d = dat[:,22:24] #RAnkle
    tornozelo_e = dat[:,28:30] #LAnkle
    calcanhar_d = dat[:,48:50] #RHell
    calcanhar_e = dat[:,42:44] #LHell
    bigtoe_d = dat[:,44:46] #right big toe
    bigtoe_e = dat[:,38:40] #left big toe
    smalltoe_d = dat[:,46:48] #left small toe
    smalltoe_e = dat[:,40:42] #right small toe
    pontape_d = (bigtoe_d + smalltoe_d) / 2 #mean point between RBigToe and RSmallToe
    pontape_e = (bigtoe_e + smalltoe_e) / 2 #mean point between LBigToe and LSmallToe

    cg_perc = {'cabeca':[1, 1], 'tronco':[.431, .3782], 'braco':[.5772, .5754],
                 'antebraco':[.4574, .4559], 'coxa':[.4095, .3612], 
                 'perna':[.4395, .4352], 'pe':[.4415, .4014]}

    if len(sys.argv) > 2 and sys.argv[2] == '1':
        sexo = 1
        modelo = 'mulher'
    else:
        sexo = 0
        modelo = 'homen'
    
    print(f'Modelo Antropométrico: {modelo}')
    # Tronco
    cg_tronco = neck + cg_perc['tronco'][sexo] * (midhip - neck) #tronco
    #  braco 
    cg_braco_e = ombro_e + cg_perc['braco'][sexo] * (cotovelo_e - ombro_e) #braco esquerdo
    cg_braco_d = ombro_d + cg_perc['braco'][sexo] * (cotovelo_d - ombro_d) #braco direito
    # antebraco
    cg_antebraco_e = cotovelo_e + cg_perc['antebraco'][sexo] * (punho_e - cotovelo_e) #antebraco esquerdo
    cg_antebraco_d = cotovelo_d + cg_perc['antebraco'][sexo] * (punho_d - cotovelo_d) #antebraco direito
    # coxa
    cg_coxa_e = quadril_e + cg_perc['coxa'][sexo] * (joelho_e - quadril_e) #coxa esquerda
    cg_coxa_d = quadril_d + cg_perc['coxa'][sexo] * (joelho_d - quadril_d) #coxa direita
    # perna
    cg_perna_e = joelho_e + cg_perc['perna'][sexo] * (tornozelo_e - joelho_e)
    cg_perna_d = joelho_d + cg_perc['perna'][sexo] * (tornozelo_d - joelho_d)
    # pe
    cg_pe_e = calcanhar_e + cg_perc['pe'][sexo] * (pontape_e - calcanhar_e)
    cg_pe_d = calcanhar_d + cg_perc['pe'][sexo] * (pontape_d - calcanhar_d)
    
    # Center of mass / center of gravity 
    cg_total = ((0.081 * cg_cab)   + (0.497 * cg_tronco)  + (0.028 * cg_braco_d)   + (0.028 * cg_braco_e) + 
    (0.022 * cg_antebraco_d) + (0.022 * cg_antebraco_e) + (0.1 * cg_coxa_d) + (0.1 * cg_coxa_e) +
    (0.047 * cg_perna_d) + (0.047 * cg_perna_e) + (0.014 * cg_pe_d)   + (0.014 * cg_pe_e)) / 1
    
    showfig = len(sys.argv)
    if showfig > 3:
        frame = int(sys.argv[3])
        segcab = np.stack((cg_cab[frame,:], neck[frame,:]), axis=0)
        segtronco = np.stack((ombro_e[frame,:], ombro_d[frame,:], quadril_d[frame,:], quadril_e[frame,:], ombro_e[frame,:]))	
        segbracod = np.stack((ombro_d[frame,:], cotovelo_d[frame,:]))
        segbracoe = np.stack((ombro_e[frame,:], cotovelo_e[frame,:]))
        segabracod = np.stack((cotovelo_d[frame,:], punho_d[frame,:]))
        segabracoe = np.stack((cotovelo_e[frame,:], punho_e[frame,:]))
        segcoxad = np.stack((quadril_d[frame,:], joelho_d[frame,:]))
        segcoxae = np.stack((quadril_e[frame,:], joelho_e[frame,:]))
        segpernad = np.stack((joelho_d[frame,:], tornozelo_d[frame,:]))
        segpernae = np.stack((joelho_e[frame,:], tornozelo_e[frame,:]))
        segped = np.stack((calcanhar_d[frame,:], pontape_d[frame,:]))
        segpee = np.stack((calcanhar_e[frame,:], pontape_e[frame,:]))   
        fig1, ax = plt.subplots()
        ax.plot(segcab[:,0], segcab[:,1])
        ax.plot(segtronco[:,0], segtronco[:,1])
        ax.plot(segbracod[:,0], segbracod[:,1])
        ax.plot(segbracoe[:,0], segbracoe[:,1])
        ax.plot(segabracod[:,0], segabracod[:,1])
        ax.plot(segabracoe[:,0], segabracoe[:,1])
        ax.plot(segcoxad[:,0], segcoxad[:,1])
        ax.plot(segcoxae[:,0], segcoxae[:,1])
        ax.plot(segpernad[:,0], segpernad[:,1])
        ax.plot(segpernae[:,0], segpernae[:,1])
        ax.plot(segped[:,0], segped[:,1])
        ax.plot(segpee[:,0], segpee[:,1])
        ax.plot(cg_cab[frame,0], cg_cab[frame,1], 'k.', markersize=18)
        ax.plot(cg_braco_d[frame,0], cg_braco_d[frame,1], 'k.', markersize=18)
        ax.plot(cg_braco_e[frame,0], cg_braco_e[frame,1], 'k.', markersize=18)
        ax.plot(cg_antebraco_d[frame,0], cg_antebraco_d[frame,1], 'k.', markersize=18)
        ax.plot(cg_antebraco_e[frame,0], cg_antebraco_e[frame,1], 'k.', markersize=18)
        ax.plot(cg_tronco[frame,0], cg_tronco[frame,1], 'k.', markersize=18)
        ax.plot(cg_coxa_d[frame,0], cg_coxa_d[frame,1], 'k.', markersize=18)
        ax.plot(cg_coxa_e[frame,0], cg_coxa_e[frame,1], 'k.', markersize=18)
        ax.plot(cg_perna_d[frame,0], cg_perna_d[frame,1], 'k.', markersize=18)
        ax.plot(cg_perna_e[frame,0], cg_perna_e[frame,1], 'k.', markersize=18)
        ax.plot(cg_pe_d[frame,0], cg_pe_d[frame,1], 'k.', markersize=18)
        ax.plot(cg_pe_e[frame,0], cg_pe_e[frame,1], 'k.', markersize=18)
        ax.plot(midhip[frame,0], midhip[frame,1], 'k.', markersize=18)
        # ax.plot(neck[frame,0], neck[frame,1], 'k.', markersize=18)
        # ax.plot(cg_cab[frame,0],cg_cab[frame,1], 'k.', markersize=18)
        ax.plot(olho_d[frame,0], olho_d[frame,1], 'g.', markersize=6)
        ax.plot(olho_e[frame,0], olho_e[frame,1], 'g.', markersize=6)
        # ax.plot(orelha_d[frame,0], orelha_d[frame,1], 'y.', markersize=6)
        # ax.plot(orelha_e[frame,0], orelha_e[frame,1], 'y.', markersize=6)
        ax.plot(cg_total[frame,0], cg_total[frame,1], 'k*', markersize=14)
        ax.set_box_aspect(2)
        plt.title(f'Frame number = {frame}; Modelo Antropométrico: {modelo}')
        plt.show()
    
    return cg_total

if __name__ == '__main__':
    main()

dir_atual = os.getcwd()
dir_working = sorted(os.listdir(dir_atual + '/reffor3d/' + '/working/'))
saltos = 0
while(saltos<len(dir_working)):
    saltoanalisado = dir_working[saltos]
    dat = np.loadtxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0f.dat')
    
    CM = main()
    saida = np.hstack((dat,CM))
    fmt = '%d', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f', '%6f'
    np.savetxt(dir_atual + '/reffor3d/' + 'working/' + saltoanalisado + '/' + 'dvideow_people_0cm.dat', saida, fmt=fmt)
    print( 'Centro de massa do' f'{saltoanalisado} calculado com sucesso')
    saltos = saltos+1
    




