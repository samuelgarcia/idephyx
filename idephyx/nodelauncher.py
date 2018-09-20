# -*- coding: utf-8 -*-

from .myqt import QT, DebugDecorator
import pyqtgraph as pg
import os


from pyacq.core import ObjectProxy


class NodeLauncher(QT.QWidget):
    def __init__(self, other_nodes,  parent=None):
        QT.QWidget.__init__(self, parent=parent)
        
        self.other_nodes = other_nodes
        
        layout = QT.QVBoxLayout()
        self.setLayout(layout)

        #~ layout.addWidget(QT.QLabel('Launch nodes:'))
        
        grid = QT.QGridLayout()
        layout.addLayout(grid)
        
        self.state_labels = {}
        
        for i, name in enumerate(self.other_nodes):
            grid.addWidget(QT.QLabel(name), i, 0)
            
            #~ but = QT.QPushButton('start')
            but = QT.QPushButton(QT.QIcon(':media-playback-start.svg'), '')
            but.name = name
            but.clicked.connect(self.on_start_clicked)
            grid.addWidget(but, i, 1)
            
            #~ but = QT.QPushButton('stop')
            but = QT.QPushButton(QT.QIcon(':media-playback-stop.svg'), '')
            but.name = name
            but.clicked.connect(self.on_stop_clicked)
            grid.addWidget(but, i, 2)
            
            #~ but = QT.QPushButton('show')
            but = QT.QPushButton(QT.QIcon(':dialog-messages.svg'), '')
            but.name = name
            but.clicked.connect(self.on_show_clicked)
            grid.addWidget(but, i, 3)

            
            label = QT.QLabel('Off')
            self.state_labels[name] = label
            grid.addWidget(label, i, 4)
        
        layout.addStretch()
        
        self.timer_running = QT.QTimer(singleShot=False, interval=500)
        self.timer_running.timeout.connect(self.check_nodes_running)
        self.timer_running.start()
    
    def check_nodes_running(self):
        for name, node in self.other_nodes.items():
            if node.running():
                self.state_labels[name].setText('Running')
            else:
                self.state_labels[name].setText('Off')
    
    def on_start_clicked(self):
        name = self.sender().name
        node = self.other_nodes[name]
        if not node.running():
            node.start()
            if hasattr(node, 'auto_scale'):
                try:
                    node.auto_scale()
                except:
                    pass
        node.show()

    def on_stop_clicked(self):
        name = self.sender().name
        node = self.other_nodes[name]
        if node.running():
            node.stop()
        #~ node.show()
    
    def on_show_clicked(self):
        name = self.sender().name
        node = self.other_nodes[name]
        node.show()

    def stop_all(self):
        for name, node in self.other_nodes.items():
            if node.running():
                node.stop()
        
    def close_all(self):
        self.timer_running.stop()
        for name, node in self.other_nodes.items():
            node.close()

