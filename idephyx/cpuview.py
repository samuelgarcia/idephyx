# -*- coding: utf-8 -*-

from .myqt import QT, DebugDecorator
import pyqtgraph as pg
import os

import psutil

from pyacq.core import ObjectProxy

class CpuView(QT.QWidget):
    def __init__(self, conf,  parent=None):
        QT.QWidget.__init__(self, parent=parent)
        
        self.conf = conf
        
        layout = QT.QVBoxLayout()
        self.setLayout(layout)
        
        #~ but = QT.QPushButton('refresh')
        #~ layout.addWidget(but)
        #~ but.clicked.connect(self.refresh_cpu)
        
        self.label = QT.QLabel('')
        layout.addWidget(self.label)
        
        #~ manager = self.conf.get('manager', None)
        
        self.table_hosts = QT.QTableWidget()
        layout.addWidget(self.table_hosts)
        
        #~ if manager is not None:
        self.table_nodegroups = QT.QTableWidget()
        layout.addWidget(self.table_nodegroups)
        
        self.full_refresh()
        
        self.timer = QT.QTimer(interval=2000)
        self.timer.timeout.connect(self.refresh_cpu)
        self.timer.start()
        
        
    
    def full_refresh(self):
        manager = self.conf.get('manager', None)
        if manager is not None:
            self.hosts = manager.hosts._get_value()
            #~ self.nodegroups = manager.list_nodegroups()
            self.nodegroups = manager.nodegroups._get_value()
        else:
            self.hosts = {}
            self.nodegroups = {}
        
        # hosts
        qtable = self.table_hosts
        qtable.clear()
        qtable.setColumnCount(2)
        qtable.setHorizontalHeaderLabels(['addr', 'cpu',])
        qtable.setRowCount(len(self.hosts)+1)

        qtable.setItem(0, 0,  QT.QTableWidgetItem('localhost'))
        
        self.psutil_remote = []
        for r, (name, host) in enumerate(self.hosts.items()):
            #~ qtable.setItem(r+1, 0,  QT.QTableWidgetItem(host.name._get_value()))
            print('host name', name, type(name))
            qtable.setItem(r+1, 0,  QT.QTableWidgetItem(str(name)))
            rpsutil = host._client()._import('psutil')
            self.psutil_remote.append(rpsutil)

        # nodegroups = process
        qtable = self.table_nodegroups
        qtable.clear()
        qtable.setColumnCount(3)
        qtable.setHorizontalHeaderLabels(['name', 'cpu', 'host'])
        qtable.setRowCount(len(self.nodegroups)+1)
        
        self.local_process = psutil.Process(os.getpid())
        qtable.setItem(0, 0,  QT.QTableWidgetItem('main local'))
        
        self.psutil_remote_processes = []
        for r, (name, ng) in enumerate(self.nodegroups.items()):
            print('host ng', name, type(name))
            if isinstance(ng, ObjectProxy):
                rpsutil = ng._client()._import('psutil')
                pid = ng._client()._import('os').getpid()
                self.psutil_remote_processes.append(rpsutil.Process(pid))
            
            qtable.setItem(r+1, 0,  QT.QTableWidgetItem(str(name)))
        
        self.refresh_cpu()
    
    def refresh_cpu(self):
        manager = self.conf.get('manager', None)
        if manager is None:
            txt = 'No subprocess\n'
        else:
            txt = 'Have manager\n'
        self.label.setText(txt)
        
        # host local and distant
        cpu = psutil.cpu_percent()
        self.table_hosts.setItem(0, 1,  QT.QTableWidgetItem(str(cpu)))
        
        for r, (name, host) in enumerate(self.hosts.items()):
            cpu = self.psutil_remote[r].cpu_percent()
            self.table_hosts.setItem(r+1, 1,  QT.QTableWidgetItem(str(cpu)))
        
        cpu = self.local_process.cpu_percent()
        self.table_nodegroups.setItem(0, 1,  QT.QTableWidgetItem(str(cpu)))
        
        # nodegroups local and other
        for r, (name, ng) in enumerate(self.nodegroups.items()):
            cpu = self.psutil_remote_processes[r].cpu_percent()
            self.table_nodegroups.setItem(r+1, 1,  QT.QTableWidgetItem(str(cpu)))
