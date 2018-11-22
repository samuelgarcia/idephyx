"""

"""
import sys
import os
import argparse


import pyqtgraph as pg
import idephyx

#~ comand_list =[
#~ ]
#~ txt_command_list = ', '.join(comand_list)


def open_mainwindow(configuration_file=None):
        app = pg.mkQApp()
        win = idephyx.MainWindow()
        if configuration_file is not None:
            win.open_configuration(configuration_file=configuration_file)
        win.show()
        app.exec_()            

def main():
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='idephyx')
    parser.add_argument('configuration_file', help='configuration file (.py)', default=None, nargs='?')
    
    #~ parser.add_argument('-d', '--dirname', help='working directory', default=None)
    #~ parser.add_argument('-c', '--chan_grp', type=int, help='channel group index', default=0)
    #~ parser.add_argument('-p', '--parameters', help='JSON parameter file', default=None)
    
    
    args = parser.parse_args(argv)
    #~ print(sys.argv)
    #~ print(args)
    #~ print(args.command)
    
    configuration_file = args.configuration_file
    #~ if not command in comand_list:
        #~ print('command should be in [{}]'.format(txt_command_list))
        #~ exit()
    
    #~ dirname = args.dirname
    #~ if dirname is None:
        #~ dirname = os.getcwd()
    
    #~ print(command)
    
    #~ if command=='mainwin':
    open_mainwindow()
    

    
    

if __name__ =='__main__':
    open_mainwindow()

