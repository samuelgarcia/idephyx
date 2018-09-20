import os

import pyqtgraph as pg
import idephyx

import pyacq

from idephyx.nodelauncher import NodeLauncher



def test_CpuView():

    conf = {}
    configuration_file = 'test_idephyx_config.py'
    exec(open(configuration_file).read(), None, conf)
    print(conf)
    
    app = pg.mkQApp()
    win = NodeLauncher(conf['other_nodes'])
    win.show()
    app.exec_()


if __name__ == '__main__':
    test_CpuView()
    
