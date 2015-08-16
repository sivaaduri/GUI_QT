import sys
from PyQt4 import QtGui, QtCore
from PyQt4 import QtCore, QtGui
import sys
import simple_rc

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1000,700)
        #self.center()
        self.setWindowTitle('OIKOS DEMO BOARD')
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.statusBar().showMessage('Disconnected')
        #self.createActions()
        #self.setwin()
        self.initUI()
        
    def initUI(self):      
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        hbox = QtGui.QHBoxLayout(self)
        hbox1 = QtGui.QHBoxLayout(self)
        tor = QtGui.QPushButton("Torque Sensor")
        topleft = QtGui.QWidget(self)
        #topleft.setFrameShape(QtGui.QFrame.StyledPanel)
        self.widget.setLayout(hbox1)
        hbox.addWidget(tor)
        
        topright = QtGui.QFrame(self)
        topright.setFrameShape(QtGui.QFrame.StyledPanel)

        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_()) 