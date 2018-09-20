# -*- coding: utf-8 -*-

import sys
import os
import datetime
from collections import OrderedDict

import numpy as np

import pyqtgraph as pg
from pyqtgraph.util.mutex import Mutex


#local imports
from .myqt import QT, DebugDecorator
from . import icons
from .tools import check_annotations, get_dict_from_group_param
from .recordinglist import RecordingList
from .controlpanel import ControlPanel
from .cpuview import CpuView

pyver = '.'.join(str(e) for e in sys.version_info[0:3])
appname = 'idephyx'+'_py'+pyver


"""
TODO:
  * open ephyviewer
  * close manager in close_configuration
  * size main controlelr
  * expand path pour last_configuration_file sinon ça bug.
  
"""


class MainWindow(QT.QMainWindow):
    def __init__(self, configuration_file=None):
        QT.QMainWindow.__init__(self)
        
        self.configured = False
        self.docks = {}
        self.conf = {}
        
        
        self.create_toolbar()
        #~ self.create_layout()
        
        self.timer_auto_scale = QT.QTimer(singleShot=True, interval=500)
        self.timer_auto_scale.timeout.connect(self.auto_scale_all)
        
        
        self.is_recording = False
        self.is_running = False
        self.mutex = Mutex()
        
        self.configuration_file = configuration_file
        self.open_settings()
        
        
        

    def warn(self, text, title='Error in idephyx'):
        mb = QT.QMessageBox.warning(self, title,text, 
                QT.QMessageBox.Ok ,
                QT.QMessageBox.NoButton)
    
    def errorToMessageBox(self, e):
        self.warn(error_box_msg.format(e))
    
    def open_settings(self):
        self.app_settings = QT.QSettings(appname, 'app_settings')
        
        if self.configuration_file is None:
            self.configuration_file = self.app_settings.value('last_configuration_file')
        
        if self.configuration_file is not None:
            self.open_configuration(self.configuration_file)
        
    
    def create_toolbar(self):
        self.toolbar = QT.QToolBar('Tools')
        self.toolbar.setObjectName('Tools')
        
        self.toolbar.setToolButtonStyle(QT.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(QT.Qt.RightToolBarArea, self.toolbar)
        self.toolbar.setIconSize(QT.QSize(60, 40))
        
        self.act_start = QT.QAction('Start', self,checkable=False , icon=QT.QIcon(":/media-playback-start.svg"))
        self.act_start.triggered.connect(self.start_nodes)
        self.toolbar.addAction(self.act_start)

        self.act_stop = QT.QAction('Stop', self,checkable=False, icon=QT.QIcon(":/media-playback-stop.svg"))
        self.act_stop.triggered.connect(self.stop_nodes)
        self.toolbar.addAction(self.act_stop)

        self.act_start_rec = QT.QAction('Start rec', self,checkable = False , icon=QT.QIcon(":/media-record.svg"))
        self.act_start_rec.triggered.connect(self.start_rec)
        self.toolbar.addAction(self.act_start_rec)

        self.act_stop_rec = QT.QAction('Stop rec', self,checkable = False, icon=QT.QIcon(":/media-record-stop.svg"))
        self.act_stop_rec.triggered.connect(self.stop_rec)
        self.toolbar.addAction(self.act_stop_rec)
        
        self.toolbar.addSeparator()
 
        self.act_open_conf = QT.QAction('Open conf', self,checkable=False , icon=QT.QIcon(":/document-open.svg"))
        self.act_open_conf.triggered.connect(self.open_conf_dialog)
        self.toolbar.addAction(self.act_open_conf)
 
        #~ self.act_save_state = QT.QAction('Save state', self,checkable=False , icon=QT.QIcon(":/view-group.svg"))
        #~ self.act_save_state.triggered.connect(self.save_window_state)
        #~ self.toolbar.addAction(self.act_save_state)
 
#~         
        

        self.toolbar.addSeparator()

    @DebugDecorator
    def open_configuration(self, configuration_file):
        if len(self.conf)>0:
            self.close_configuration()
        print('idephyx open_configuration', configuration_file)
        #~ try:
        if 1:
            
            self._apply_configuration(configuration_file)
            self.app_settings.setValue('last_configuration_file', os.path.abspath(configuration_file))
            self.file_settings = QT.QSettings(appname, os.path.basename(configuration_file).replace('.py', ''))
            self.load_window_state()
            self.configured = True
            print('LOADED : ', configuration_file)
        #~ except:
            #~ self.app_settings.setValue('last_configuration_file', None)
            #~ err_msg ='LOAD ERROR : {}'.format(configuration_file)
            #~ print(err_msg)
            #~ self.warn(err_msg)


    def _apply_configuration(self, configuration_file):
        
        self.conf = {}
        with open(configuration_file) as f:
            exec(f.read(), None, self.conf)
        #~ for k, v in conf.items():
            #~ print(k, ':', v, type(v))
        
        # show/hide open setting
        self.act_open_conf.setVisible(self.conf.get('show_open_settings_menu', True))
        

        # control panel
        self.controlpannel = self.conf.get('controlpannel', None)
        if self.controlpannel is None:
            self.controlpannel = ControlPanel(self.conf)
        self.docks['controlpannel'] = QT.QDockWidget('controlpannel',self)
        self.docks['controlpannel'].setWidget(self.controlpannel)
        self.addDockWidget(QT.Qt.RightDockWidgetArea, self.docks['controlpannel'])
        
        # cpu if have manager
        manager = self.conf.get('manager', None)
        if manager is not None:
            self.cpuview = CpuView(self.conf)
            self.docks['cpuview'] = QT.QDockWidget('cpuview',self)
            self.docks['cpuview'].setWidget(self.cpuview)
            self.tabifyDockWidget(self.docks['controlpannel'], self.docks['cpuview'])
        
        # node launcher if present in config
        nodelauncher = self.conf.get('nodelauncher', None)
        if nodelauncher is not None:
            self.docks['nodelauncher'] = QT.QDockWidget('nodelauncher',self)
            self.docks['nodelauncher'].setWidget(nodelauncher)
            self.tabifyDockWidget(self.docks['controlpannel'], self.docks['nodelauncher'])
        
        
        # annotations and recording list
        annotations = self.conf.get('annotations', None)
        annotations_for_naming = self.conf.get('annotations_for_naming', None)
        recording_path = self.conf.get('recording_path', None)
        if recording_path is not None and not os.path.exists(recording_path):
            os.makedirs(recording_path)
        
        if annotations is not None and annotations_for_naming is not None and recording_path is not None:
            check_annotations(annotations, annotations_for_naming)
            
            self._annotations = pg.parametertree.Parameter.create(name='annotations', type='group', children=annotations)
            self.tree_annotations = pg.parametertree.ParameterTree()
            self.tree_annotations.header().hide()
            self.tree_annotations.setParameters(self._annotations, showTop=True)
            #~ self.tree_annotations.setWindowTitle('Annotations')
            self.docks['annotations'] = QT.QDockWidget('annotations',self)
            self.docks['annotations'].setWidget(self.tree_annotations)
            self.addDockWidget(QT.Qt.RightDockWidgetArea, self.docks['annotations'])
            
            self.recording_list = RecordingList(recording_path)
            self.docks['recording_list'] = QT.QDockWidget('recording_list',self)
            self.docks['recording_list'].setWidget(self.recording_list)
            self.addDockWidget(QT.Qt.RightDockWidgetArea, self.docks['recording_list'])
            
            if not os.path.exists(recording_path):
                os.makedirs(recording_path)
        else:
            self._annotations = None
            self.recording_list = None


        
        # nodes
        assert 'nodes' in self.conf, 'Configuration file must contains "nodes" dict'
        
        # widgets
        assert 'widgets' in self.conf, 'Configuration file must contains "widgets" dict'
        
        for name, widget in self.conf['widgets'].items():
            self.docks[name] = QT.QDockWidget(name,self)
            self.docks[name].setWidget(widget)
            self.addDockWidget(QT.LeftDockWidgetArea, self.docks[name])
            
            if hasattr(widget, 'annotation_changed'):
                widget.annotation_changed.connect(self.new_annotation_from_widget)
        
        # for save/restore state need object name
        for name, dock in self.docks.items():
            dock.setObjectName(name)

    def close_configuration(self):
        self.stop_nodes()
        self.close_nodes()
        
        for dock in self.docks.values():
            self.removeDockWidget(dock)
        
        manager = self.conf.get('manger', None)
        if manager is not None:
            manager.close()
        
        self.conf = {}
        self.docks = {}
    
    @DebugDecorator
    def open_conf_dialog(self, v=None):
        with self.mutex:
            if self.is_recording:
                return
        
        #~ print('open_conf_dialog')
        fd = QT.QFileDialog(fileMode=QT.QFileDialog.ExistingFile, acceptMode=QT.QFileDialog.AcceptOpen)
        #~ fd.setNameFilters(['Hearingloss setup (*.json)', 'All (*)'])
        fd.setViewMode(QT.QFileDialog.Detail)
        if fd.exec_():
            configuration_file = fd.selectedFiles()[0]
            self.close_configuration() 
            self.open_configuration(configuration_file)
            #~ print(dirname)

    @DebugDecorator
    def start_nodes(self, v=None):
        for node in self.conf['nodes'].values():
            if node.running():
                continue
            node.start()
        
        with self.mutex:
            self.is_running = True
            
        if self.conf.get('auto_scale_on_start', True):
            self.timer_auto_scale.start()

    @DebugDecorator
    def stop_nodes(self, v=None):
        print('stop_nodes')
        for node in self.conf['nodes'].values():
            if not node.running():
                continue
            node.stop()

        with self.mutex:
            self.is_running = False

    @DebugDecorator
    def close_nodes(self, v=None):
        print('close_nodes')
        for node in self.conf['nodes'].values():
            node.close()


    @DebugDecorator
    def start_rec(self, v=None):
        if 'recorders' not in self.conf:
            return
        with self.mutex:
            if self.is_recording:
                return
            if not self.is_running:
                return
        
        
        _annotations = get_dict_from_group_param(self._annotations)
        #~ #chec annotations with no_ and no =
        annotations = {}
        for k, v in _annotations.items():
            if isinstance(v, str):
                if ('_' in v) or ('=' in v):
                    v = v.replace('_', ' ').replace('=', ' ')
            annotations[k] = v

        rec_datetime = datetime.datetime.now()
        annotations['rec_datetime'] = rec_datetime.isoformat()
        
        name = '{:%Y-%m-%dT%Hh%Mm%S}'.format(rec_datetime, )
        for k in self.conf['annotations_for_naming']:
            name += '_{}={}'.format(k, annotations[k])
        dirname =  os.path.join(self.conf['recording_path'] , name)
        #~ print(dirname)
        
        for rec, streams in self.conf['recorders'].items():
            rec.configure(streams=streams, autoconnect=True, dirname=dirname)
            rec.initialize()
            #~ print(annotations)
            rec.add_annotations(**annotations)
            rec.start()

        if self.recording_list is not None:
            self.recording_list.refresh_list()

        with self.mutex:
            self.is_recording = True
        
            but = self.toolbar.widgetForAction(self.act_start_rec)
            but.setStyleSheet("QToolButton:!hover { background-color: red }")
        
    
    
    @DebugDecorator
    def stop_rec(self, v=None):
        with self.mutex:
            if not self.is_recording:
                return
        
        
        
        for rec, streams in self.conf['recorders'].items():
            rec.stop()
            rec.close()

        with self.mutex:
            self.is_recording = False
            
            but = self.toolbar.widgetForAction(self.act_start_rec)
            but.setStyleSheet("")

    def closeEvent(self, event):
        #~ print('closeEvent')
        with self.mutex:
            if self.is_recording:
                event.ignore()
                return
        
        if self.conf.get('state_window_state_at_exit', False):
            self.save_window_state()
        self.close_configuration()
        event.accept()

    @DebugDecorator
    def new_annotation_from_widget(self, annotations):
        if self._annotations is not None:
            for k, v in annotations.items():
                self._annotations[k] = v
    
    def auto_scale_all(self):
        for name, widget in self.conf['widgets'].items():
            if hasattr(widget, 'auto_scale'):
                try:
                    widget.auto_scale()
                except:
                    pass
    
    def save_window_state(self):
        print('save_window_state')
        geometry = self.saveGeometry()
        self.file_settings.setValue("windowGeometry", geometry)
        state = self.saveState()
        self.file_settings.setValue("windowSate", state)
    
    def load_window_state(self):
        return # this is too buggy

        #~ geometry = self.file_settings.value("windowGeometry")
        #~ if geometry is not None:
            #~ self.restoreGeometry(geometry)
        
        #~ state = self.file_settings.value("windowSate")
        #~ if state is not None:
            #~ self.restoreState(state)

