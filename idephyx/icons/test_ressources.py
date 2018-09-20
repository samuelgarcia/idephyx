 
import sys
from idephyx.myqt import QT, mkQApp, QT_MODE
print('QT_MODE', QT_MODE)

import  idephyx.icons


if __name__ == '__main__' :
	app = mkQApp()
	
	w = QT.QWidget()
	w.show()
	w.setWindowIcon(QT.QIcon(':/media-record.png'))
	
	app.exec_()
	
	
