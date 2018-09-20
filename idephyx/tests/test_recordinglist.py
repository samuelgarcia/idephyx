import os

import pyqtgraph as pg
import idephyx


from idephyx.recordinglist import RecordingList



def test_RecordingList():
    
    recording_path = os.path.expanduser('~/idephyx_files')
    
    app = pg.mkQApp()
    win = RecordingList(recording_path)
    win.show()
    app.exec_()


if __name__ == '__main__':
    test_RecordingList()
    
