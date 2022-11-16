import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
from client import array, gui_play
import time

class Test():
    def __init__(self):
        self.selected = "/media/huss/CE6698AB66989635/Users/tendl/Desktop/M2/Son/TP/TP/mu32/megamicro_20190702_Tfdn_mfcc.h5"


#antenne=array('server')   # When performing real-time acquisition (acquisition system is required)
antenne=array('play')     # When playing recorded files (can work without acquisition system)

gui = gui_play(antenne.play_fct, antenne.stopplay_fct, antenne.loadFile_fct)
s = gui.file
# gui.file.selected="/media/huss/CE6698AB66989635/Users/tendl/Desktop/M2/Son/TP/TP/mu32/megamicro_20190702_Tfdn_mfcc.h5"

A = Test()
antenne.loadFile_fct(A)

from client import loadFile_fct
