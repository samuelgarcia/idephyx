import os

import pyqtgraph as pg
import idephyx

import pyacq

from idephyx.cpuview import CpuView



def test_CpuView():

    conf = {}
    configuration_file = 'test_idephyx_config.py'
    exec(open(configuration_file).read(), None, conf)
    print(conf)
    
    app = pg.mkQApp()
    win = CpuView(conf)
    win.show()
    app.exec_()


if __name__ == '__main__':
    test_CpuView()
    
