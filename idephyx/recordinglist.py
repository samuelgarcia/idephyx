# -*- coding: utf-8 -*-
import os, sys
import json
import datetime
import dateutil.parser


from .myqt import QT, DebugDecorator
import pyqtgraph as pg



only_today = 'only today'

class RecordingList(QT.QWidget):
    def __init__(self, recording_path, parent=None):
        QT.QWidget.__init__(self, parent=parent)
        
        self.recording_path = recording_path
        
        
        self.setMinimumSize(10,10)
        
        layout = QT.QVBoxLayout()
        self.setLayout(layout)
        
        self.combo = QT.QComboBox()
        layout.addWidget(self.combo)
        self.combo.addItems([only_today, 'all'])
        self.combo.currentIndexChanged.connect(self.refresh_list)
        
        self.rec_list = QT.QTreeWidget(columnCount=1)
        layout.addWidget(self.rec_list)
        self.rec_list.itemDoubleClicked.connect( self.open_fileexplorer)
        
        self.refresh_list()
        
        #~ self.time_flash = QT.QTimer(interval=500)
        #~ self.time_flash.timeout.connect(self.refresh_color)
        #~ self.flash_state = True
        #~ self.time_flash.start()
        
        #~ self.list = [ ]
        
    
    #~ def refresh_color(self):
        #~ self.flash_state = not(self.flash_state)
        #~ for rec in self.list:
            #~ if rec['state'] == 'finished':
                #~ color = 'green'
            #~ elif rec['state'] == 'recording' and self.flash_state:
                #~ color = 'orange'
            #~ else:
                #~ color = 'white'
            #~ brush = QT.QBrush(QT.QColor(color), QT.SolidPattern)
            #~ brush.setColor(QT.QColor(color))
            #~ rec['item'].setBackground(0, brush)
    
    def refresh_list(self, v=None):
        self.rec_list.clear()
        for name in sorted(os.listdir(self.recording_path)):
            fullpath = os.path.join(self.recording_path, name)
            if not os.path.isdir(fullpath):
                continue
            
            if not (os.path.exists(os.path.join(fullpath, 'stream_properties.json')) or 
                    os.path.exists(os.path.join(fullpath, 'avi_stream_properties.json')) or 
                    os.path.exists(os.path.join(fullpath, 'annotations.json')) ):
                continue
            
            if self.combo.currentText() == only_today:
                # check data
                today_date = datetime.datetime.now().date()
                
                with open(os.path.join(fullpath, 'annotations.json'), 'r', encoding='utf8') as f:
                    ann = json.load(f)                
                    rec_datetime = dateutil.parser.parse(ann['rec_datetime'])
                    if today_date != rec_datetime.date():
                        continue
                
            item = QT.QTreeWidgetItem([name])
            self.rec_list.addTopLevelItem(item)
    
    #~ def add_rec(self, name, dirname, rec_datetime, state = 'recording'):
        #~ item = QT.QTreeWidgetItem([ name  ,'' , '' ] )
        #~ item.setToolTip(0,name)
        
        #~ self.list.append( {'name' : name, 'dirname': dirname, 'rec_datetime' : rec_datetime, 'item' : item , 'state' : state})
        #~ self.rec_list.addTopLevelItem(item)
    
    def open_fileexplorer(self, item, column):
        #~ print item.index.row()
        #~ i = self.rec_list.	indexOfTopLevelItem(item)
        #~ name = self.rec_list.
        name = item.text(0)
        
        fullpath = os.path.join(self.recording_path, name)
        
        #~ dirname = self.list[i]['dirname']


        if sys.platform.startswith('win'):
            os.startfile(fullpath)
        elif sys.platform.startswith('linux'):
            os.system('xdg-open "{}"'.format(fullpath))
        elif sys.platform== 'darwin' :
            os.system('open "{}"'.format(fullpath))

