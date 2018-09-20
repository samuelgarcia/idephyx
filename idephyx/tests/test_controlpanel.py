import os

import pyqtgraph as pg
import idephyx

import pyacq

from idephyx.controlpanel import ControlPanel



def test_ControlPanel():
    
    conf = {}
    configuration_file = 'test_idephyx_config.py'
    exec(open(configuration_file).read(), None, conf)
    print(conf)
    
    app = pg.mkQApp()
    win = ControlPanel(conf)
    win.show()
    app.exec_()


if __name__ == '__main__':
    test_ControlPanel()
    
