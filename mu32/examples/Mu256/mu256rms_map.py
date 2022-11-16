# mu256rms_map.py python program example for MegaMicro Mu32 transceiver 
#
# Copyright (c) 2022 DistalSense
# Author: françois.ollivier@distalsense, bruno.gas@distalsense.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Run the Mu32 system and plot signals comming from activated microphones. Use pyqtgraph.

Documentation is available on https://distalsense.io

Please, note that the following packages should be installed before using this program:
	> pip install libusb1
	> pip install pyqt6 pyqtgraph
"""

welcome_msg = '-'*20 + '\n' + 'Mu32 run program\n \
Copyright (C) 2022  distalsense\n \
This program comes with ABSOLUTELY NO WARRANTY; for details see the source code\'.\n \
This is free software, and you are welcome to redistribute it\n \
under certain conditions; see the source code for details.\n' + '-'*20

import argparse
import numpy as np
import queue
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from mu32.core import Mu256, logging, mu32log


PO = 20e-6

MEMS = range( 240 )             # MEMS = range(256)
DURATION = 0                    # 0 = infinite duration
BLOCKSIZE = 2048				# Number of samples per block.
BUFFER_NUMBER = 4				# USB transfer buffer number. should be at least equal to two
SAMPLING_FREQUENCY = 50000		# this is the max frequency
QUEUE_SIZE = 0                  # queue max size (if > 0: no latency = buffers comming when size is exceeded are lost. If 0: no size. Latency can occure)


mu32log.setLevel( logging.INFO )

def main():

    parser = argparse.ArgumentParser()
    parser.parse_args()
    print( welcome_msg )

    """
    Init graph
    """
    win = pg.GraphicsLayoutWidget( show=True, title="Mu32 example: Mapping" )
    win.resize( 1000, 1000 )
    win.setWindowTitle( 'Mu32 example: Mapping' )
    pg.setConfigOptions( antialias=True )

    ## create four areas to add plots
    w = win.addPlot()
    graph = pg.ScatterPlotItem(
        pxMode=False,  # Set pxMode=False to allow spots to transform with the view
        hoverable=True,
        hoverPen=pg.mkPen('g'),
        hoverSize=1,
    )
    bar = pg.ColorBarItem( values= (0, 90) ) # prepare interactive color bar
    spots = []
    size = 0.9-0.6*( len(MEMS)/256 )
    for i in range( len( MEMS )//8 ):
        for j in range( 8 ):
            spots.append( {'pos': ( j, i ), 'size': size, 
                          'pen': {'color': 'w', 'width': 2}, 
                          'brush':pg.intColor( i*4+j )} )
    graph.addPoints( spots )
    w.addItem( graph )
    w.setAspectLocked( 1 )
    w.showAxis(axis='left',show=False)
    w.showAxis(axis='bottom',show=False)
    w.showGrid( x=True, y=True )
    w.setXRange( -0.5, 7.5 )
    w.setYRange( -0.5, 3.5 )
    w.setLabel( 'bottom', '# Micro' )
    w.setLabel( 'left', '# Faisceau' )

    timer = QtCore.QTimer()
    timer.timeout.connect( lambda: update_map( mu256, graph ) )	

    """
    start Mu32 acquisition
    """
    try:
        mu256 = Mu256()
        mu256.run( 
            mems=MEMS,
            duration=DURATION,
            sampling_frequency=SAMPLING_FREQUENCY,
            buffer_length=BLOCKSIZE,
            buffers_number=BUFFER_NUMBER,
            callback_fn=None,
            post_callback_fn=None,
            queue_size = QUEUE_SIZE,
            block =False
        )

        timer.start( 10 )

        input( 'Press [Return] key to stop...' )
        mu256.stop()

    except Exception as e:
        print( 'aborting: ', e )


def update_map( mu256, graph ):
    """
    get last queued signal, compute std, log scale and plot
    """
    try:
        data = ( mu256.signal_q.get_nowait() * mu256.sensibility ).std( axis=1 )
    except queue.Empty:
        return
    
    Lvl = 20*np.log10( ( data+PO )/PO )
    Lvl = [pg.intColor(Lvl[i], 120) for i in range( mu256.mems_number )]
    
    graph.setBrush( Lvl )



if __name__ == "__main__":
	main()

