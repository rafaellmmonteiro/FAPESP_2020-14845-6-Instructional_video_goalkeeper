# Automatizar a reconstrucao 3D
# Maria Vitoria Ribeiro Mendes - 29/08/2021 - v1

"""
Terminal na pasta 'reconstrucao'

Nessa pasta deve ter: calibvid e snap_calib
infos_calib com arquivo refcal.ref
for3d com pasta c1,c2, c3

1) Lê de 3 em 3 linhas
Cada linha, um video

2) Buscar video na pasta 'videos_cortados'
Copiar video para a pasta calibvid

3) Chamar exframe2calib

4) Chamar makecalib_dat

5) Chamar make_dlt

6) Procurar dvideow_people_0.dat na pasta de cada video
working/nome do video/*.dat

7) Copiar para for3d c1,c2,c3 respectivamente

8) Chamar make_rec3d

9) Criar pasta com nome do video 1 

10) Copiar para a pasta:

- Em info_calib: pasta dlt_to_calib 
cp2d_ref_to_checkError.dat

-Em snap_calib: c1,c2,c3

- Pasta working3d

11) Apagar

- Em info_calib: pasta dlt_to_calib 
cp2d_ref_to_checkError.dat

-Em snap_calib: c1,c2,c3

- Pasta working3d

12) Recomeçar o processo para os próximos vídeos

"""
import glob 
import shutil
import os
import subprocess # chamar shell script e passar parametros
import sys # stdout e stderr

# open txt

listaDeVideos = open('paraReconstruir.txt','r')

lista = listaDeVideos.readlines() # cada linha do arquivo se torna um elemento da lista

subLista = [lista[n:n+3] for n in range(0, len(lista), 3)]

diretorioInicial = os.getcwd()

# iterar pela lista de videos 3 a 3 (3 cameras)
# cada iteracao, 1 salto totalmente processado
# cabe ao usuario printar os frames e marcar os pontos

for grupo in subLista:
    for video in grupo:
        video = video.replace('\n',"")
        #videos.append(video)
        #print(video)
    #print('**end group**') ok, funciona. pega de 3 em 3 videos
        
        # copiar de videos_cortados para calibvid
        try:
            #print('Procurando: '+'/videos-cortados/'+video+'.mp4')
            localVideo = glob.glob(diretorioInicial+'/videos-cortados/'+video+'.mp4')
            origem = diretorioInicial+'/videos-cortados/'+video+'.mp4'
            destino = diretorioInicial+'/calibvid'
            try: 
                shutil.copy2(origem,destino)
                print(origem +' foi copiado com sucesso para '+destino)
            except shutil.SameFileError:
                print('Mesmo arquivo na origem e no destino')
            except PermissionError:
                print('Permissao negada')
            except:
                print('Algum erro aconteceu. Origem: ' + origem)
        except:
            print('Video nao encontrado! Video: '+video)
           
    # chamar exframe2calib e fazer print no frame
    print('Print dos frames para o grupo: '+ str(grupo))
    
    print('Chama exframe2calib')
    
    for video in grupo:
        os.system('./exframe2calib.sh')
        print('__ exframe2calib para o video '+video+'__')
    # chamar makecalib_py
    print('Prints feitos, diretorio atual: '+diretorioInicial+'\nChamar makecalib_py\n')
    os.system('python3 makecalib_dat.py')

    # chamar make_dlt
    os.system('python3 make_dlt.py')


    # copiar arquivos do openpose de working pra for3d
    dircam = 1 
    for video in grupo:
        video = video.replace('\n',"")
        os.chdir(diretorioInicial+'/working/'+video)
        openpose = glob.glob('*_0.dat')
        print('Arquivo do openpose sendo copiado: '+openpose[0])
        origem = diretorioInicial+'/working/'+video+'/'+openpose[0]
        shutil.copy(origem,diretorioInicial+'/for3d/c'+ str(dircam))
        dircam += 1

    os.chdir(diretorioInicial)
    #chamar makerec3d
    os.system('python3 make_rec3d.py')

    print('\n ______ Fim de processamento para o grupo: '+ str(grupo)+' ______\n')
    
    # guardar as infos em uma pasta para cada salto

    videoPasta = grupo[0]
    # criarPasta = 'mkdir '+ videoPasta
    os.system('mkdir '+ videoPasta) # criar pasta

    """for cam in range (1,4):
        origem = diretorioInicial+'/snap_calib/c'+str(cam)+'/c'+str(cam)+'.dat'
        destino = diretorioInicial+'/'+videoPasta 
        try:
            fileDestination = shutil.copy(origem,destino)
            print('Copiando .dat de '+ origem +' para '+ destino)
            print('fileDestination = '+ fileDestination)
        except:
            print('Algum erro ocorreu na copia de ' + origem +' para '+ destino)
     """
    # copiar c1,c2,c3 de snap_calib
    origem = diretorioInicial+'/snap_calib'
    destino = diretorioInicial+'/'+ videoPasta 
    try: 
        fileDestination = shutil.copytree(origem,destino)
        print('Copiando .dat de '+ origem +' para '+ destino)
        print('fileDestination = '+ fileDestination)
    except:
        print('Algum erro ocorreu na copia de ' + origem +' para '+ destino)
    
    # copiar arquivos do dlt
    
    
    origem = diretorioInicial+ '/infos_calib/dlt_to_calib/dlt_all_cams.cal'
    destino = diretorioInicial+ '/'+ videoPasta
    try:
        shutil.copy(origem,destino)
        print('Copiando .dat de '+ origem +' para '+ destino)
    except:
        print('Algum erro ocorreu na copia de ' + origem +' para '+ destino)

    origem = diretorioInicial+ '/infos_calib/cp2d_ref_to_checkError.dat'
    destino = diretorioInicial+ '/'+ videoPasta
    try:
        shutil.copy(origem,destino)
        print('Copiando .dat de '+ origem +' para '+ destino)
    except:
        print('Algum erro ocorreu na copia de ' + origem +' para '+ destino)
    
    # copiar arquivo resultante da reconstrucao 3D
    origem = diretorioInicial+ '/working3d/arq3d_0.3d'
    destino = diretorioInicial+ '/'+videoPasta
    try:
        shutil.copy(origem,destino)
        print('Copiando .dat de '+ origem +' para '+ destino)
    except:
        print('Algum erro ocorreu na copia de ' + origem +' para '+ destino)

    try:
        origem = diretorioInicial + '/arqchek_error.3d'
        destino = diretorioInicial+ '/'+videoPasta
        print('Copiando .dat de '+ origem +' para '+ destino)

    except:
        print('Algum erro ocorreu na copia de ' + origem +' para '+ destino)

    print('\n ______ Fim copia de arquivos do grupo grupo: '+ str(grupo)+' ______\nPasta criada: '+ grupo[0]+'\n')
    
    # apagar algumas pastas e arquivos para que os proximos saltos sejam processados sem erro e warnings
    
    os.system('rm -r snap_calib')
    os.system('rm -r infos_calib/dlt_to_calib')
    os.system('rm infos_calib/cp2d_ref_to_checkError.dat')
    os.chdir(diretorioInicial+'/calibvid')
    os.system('rm *.mp4')

    os.chdir(diretorioInicial)
    
    # working3d
    os.system('rm -r working3d')
    # for3d: c1,c2,c3 -> arquivo dentro da pasta
    os.system('rm for3d/c1/dvideow_people_0.dat')
    os.system('rm for3d/c2/dvideow_people_0.dat')
    os.system('rm for3d/c3/dvideow_people_0.dat')
    os.system('rm arqchek_error.3d')
    
    print('\n ______ Fim remocao de arquivos do grupo grupo: '+ str(grupo)+'\n')

