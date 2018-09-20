"""
Config with:
  * one fake device 4 channel 100Hz
  * one oscilloscope
  * annotation for rec
"""

import os




import numpy as np

import pyacq
from pyacq.core.host import Host
from pyacq.devices import NumpyDeviceBuffer
from pyacq.viewers import QOscilloscope
from pyacq.rec import RawRecorder
from idephyx import NodeLauncher

if __name__ == '__main__':
    import pyqtgraph as pg
    app = pg.mkQApp()


nb_channel = 4
chunksize = 20
sample_rate = 1000
#~ sample_rate = 10000.
#~ chunksize = 20
length = chunksize*1000
sigs = np.zeros((length, nb_channel), dtype='float32')
times = np.arange(length)/sample_rate
sigs[:, :] = np.sin(2*np.pi*2.678*times)[:, None]


manager = pyacq.create_manager()

ng0 = manager.create_nodegroup('device0')




#~ print(manager.list_nodegroups())


#~ dev0 = NumpyDeviceBuffer()
dev0 = ng0.create_node('NumpyDeviceBuffer')
dev0.configure(nb_channel=nb_channel, sample_interval=1./sample_rate, chunksize=chunksize, buffer=sigs)
dev0.output.configure(protocol='tcp', interface='127.0.0.1', transfermode='plaindata')
dev0.outputs['signals'].configure(protocol='tcp', interface='127.0.0.1', transfertmode='plaindata')
dev0.initialize()


oscope0 = QOscilloscope()
oscope0.configure(with_user_dialog=True, max_xsize=60.)
oscope0.input.connect(dev0.output)
oscope0.initialize()
oscope0.params['scale_mode'] = 'by_channel'


rec = RawRecorder()




# global UI settings
show_open_settings_menu = True
#~ auto_scale_on_start = False

# optional control pannel
# controlpanel = CustumControlPanel(...)


# node list
nodes = {
    'signals' : dev0,
    'oscilloscope' : oscope0,
}

#widget
widgets = {
    'oscilloscope' : oscope0,
}

# recorders
recorders = {
    rec : [dev0.output],
}

# annotation
annotations = [
    {'name': 'annotation1', 'type': 'str', 'value' : 'yeah'},
    {'name': 'annotation2', 'type': 'str', 'value' : 'boom'},
]

annotations_for_naming = ['annotation1',]

recording_path = os.path.expanduser('~/idephyx_files')



# other nodes
ng1 = manager.create_nodegroup('Oscope Bis')

# create fake host
#~ host_proc, host = Host.spawn('test-host')
#~ host_addr = host_proc.client.address
#~ host = manager.get_host(host_addr)
#~ ng1 = manager.create_nodegroup('fake-distant', host=host)



#~ oscope1 = QOscilloscope(close_node_on_widget_closed=False)
oscope1 = ng1.create_node('QOscilloscope', close_node_on_widget_closed=False)
oscope1.configure(with_user_dialog=True, max_xsize=60.)
oscope1.input.connect(dev0.output)
oscope1.initialize()
oscope1.params['scale_mode'] = 'by_channel'

other_nodes = {
    'oscilloscope_bis' : oscope1,
}
nodelauncher = NodeLauncher(other_nodes)


print('test_idephyx_config.py end file')

