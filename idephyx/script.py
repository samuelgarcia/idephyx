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


def open_mainwindow():
        app = pg.mkQApp()
        win = idephyx.MainWindow()
        win.show()
        app.exec_()            

def main():
    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='idephyx')
    #~ parser.add_argument('command', help='command in [{}]'.format(txt_command_list), default='mainwin', nargs='?')
    
    #~ parser.add_argument('-d', '--dirname', help='working directory', default=None)
    #~ parser.add_argument('-c', '--chan_grp', type=int, help='channel group index', default=0)
    #~ parser.add_argument('-p', '--parameters', help='JSON parameter file', default=None)
    
    
    args = parser.parse_args(argv)
    #~ print(sys.argv)
    #~ print(args)
    #~ print(args.command)
    
    #~ command = args.command
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

