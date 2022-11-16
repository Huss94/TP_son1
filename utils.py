import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
from client import array, gui_play
import time
import glob
import os 
import time
class File():
    
    def __init__(self, selected):
        self.selected = selected


def save_folder_of_h5files_as_dict(folder_path, save_destination = "matrices"):
    """
    Prend cahque fichier h5 du chemin indiqué et les sauvegarde le premier buffer dans un dictionnaire
    """

    if not os.path.isdir(save_destination):
        os.mkdir(save_destination)
    
    paths= glob.glob(folder_path + '/*.h5')
    for path in paths:
        dict_to_save, _ = transform_h5_to_dict(path)

        index = path[::-1].index('/')
        name = path[len(path) - index : -3]

        np.save(save_destination + '/' + name, dict_to_save)
        print(f"Saved {name} to {save_destination} folder")

    print("Finished")

def transform_h5_to_dict(path):
    """
    retourne l'antenne du fichier h5 ainsi qu'un dicitonnaire reprenant ses info importante
    """
    try:
        #Nous avons volontairement modifié le fichier client.py pour éviter des erreurs sur notre machine
        antenne=array('play', displaying=False)     
    except TypeError:
        antenne = array('play')
    
    A = File(path)
    antenne.loadFile_fct(A)
    antenne.play_fct(button = None)
    time.sleep(0.1)
    antenne.stopplay_fct(button = None)
    m = antenne.read()

    dic = {}

    dic['mat'] = m
    dic['fs'] = antenne.fs
    dic['blocksize'] = antenne.blocksize
    dic['N'] = antenne.mems_nb
    dic['interspace'] = antenne.interspace
    return dic, antenne


def fourier(x, Fs,i, mode = "modulus", K = None, newFig = 0,limaxis= (0,1000) ):
    if newFig: 
        plt.figure()
    if K == None:
        K = len(x)
    freq = np.fft.fftfreq(K, 1/Fs)
    sp = np.fft.fft(x, K)
    if mode == "phase" or mode == "angle":
        plt.title("Phase du signal")
        plt.plot(np.fft.fftshift(freq), np.fft.fftshift(np.angle(sp)), label = i)
        plt.ylabel=("Phase")
    if mode == "modulus":
        plt.title("Spectre du signal")

        plt.plot(np.fft.fftshift(freq), np.fft.fftshift(np.abs(sp)), label = i)
        plt.ylabel=("Module")

    plt.xlabel=("frequence")
    plt.xlim(limaxis)

    return freq, sp












# gui = gui_play(antenne.play_fct, antenne.stopplay_fct, antenne.loadFile_fct)
# s = gui.file
# gui.file.selected="/media/huss/CE6698AB66989635/Users/tendl/Desktop/M2/Son/TP/TP/mu32/megamicro_20190702_Tfdn_mfcc.h5"