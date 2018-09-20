"""


"""

import os
import pyacq

from pyacq.devices import WebCamAV
from pyacq.viewers import ImageViewer
from pyacq.rec import AviRecorder

if __name__ == '__main__':
    import pyqtgraph as pg
    app = pg.mkQApp()



# this allow user to load another configuraton file from the UI or not
show_open_settings_menu = False


cam = WebCamAV()
cam.configure(camera_num=0)
cam.output.configure(protocol='tcp', interface='127.0.0.1', transfermode='plaindata')
cam.initialize()

camviewer = ImageViewer()
camviewer.configure()
camviewer.input.connect(cam.output)
camviewer.initialize()

rec = AviRecorder()







# node list
nodes = {
    'camera': cam,
    'camviewer' : camviewer,
}

#widget
widgets = {
    'camviewer' : camviewer,
}

# recorders
recorders = {
    rec : {'webcam' : cam.output},
}

# annotation
annotations = [
]

annotations_for_naming = []

recording_path = os.path.expanduser('~/idephyx_files')

