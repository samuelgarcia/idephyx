# -*- coding: utf-8 -*-
from .myqt import QT, DebugDecorator
import pyqtgraph as pg


class ControlPanel(QT.QWidget):
    def __init__(self, conf,  parent=None):
        QT.QWidget.__init__(self, parent=parent)
        
        self.conf = conf
        
        layout = QT.QVBoxLayout()
        self.setLayout(layout)
        
        but = QT.QPushButton('Auto scale viewers')
        layout.addWidget(but)
        but.clicked.connect(self.auto_scale_viewers)

    
    def auto_scale_viewers(self):
        for name, widget in self.conf['widgets'].items():
            if hasattr(widget, 'auto_scale'):
                try:
                    widget.auto_scale()
                except:
                    pass



