import pyqtgraph as pg
import idephyx




def test_mainwindow_with_last_config():
    configuration_file = 'test_idephyx_config.py'
    
    app = pg.mkQApp()
    win = idephyx.MainWindow()

    if not win.configured or win.configuration_file != configuration_file:
        win.open_configuration(configuration_file=configuration_file)
    win.show()
    app.exec_()


def test_mainwindow_from_example():
    #~ configuration_file = '../../examples/configuration_examples/empty_template.py'
    configuration_file = '../../examples/configuration_examples/video_config.py'
    
    app = pg.mkQApp()
    win = idephyx.MainWindow(configuration_file=configuration_file)
    win.show()
    app.exec_()


if __name__ == '__main__':
    test_mainwindow_with_last_config()
    
    test_mainwindow_from_example()
