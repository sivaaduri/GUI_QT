from PyQt4 import QtCore, QtGui
import sys
import simple_rc
from gauge import AnalogClock
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1000,700)
        self.center()
        self.setWindowTitle('OIKOS DEMO BOARD')
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.statusBar().showMessage('Disconnected')
        self.createActions()
        self.setwin()
        
    def setwin(self):
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QtGui.QGridLayout()
        
        """quit = QtGui.QPushButton('Close')
        tor = QtGui.QPushButton("Torque Sensor")
        quit.setGeometry(QtCore.QRect(10,10,70,40))
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        quit.setToolTip('Close')
        quit.setStyleSheet("background-image:url(:/images/save.png)")
        self.connect(quit,QtCore.SIGNAL( 'clicked()' ), QtGui.qApp,QtCore.SLOT( 'quit()'))
        self.layout.addWidget(quit,0,0)
        self.layout.addWidget(tor,0,1)"""
        self.layout.addWidget(self.Motorcontrol(), 2, 0)
        self.layout.addWidget(self.Ics(), 1, 1)
        self.layout.addWidget(self.Sensors(), 1,0)
        self.layout.addWidget(self.Commandline(), 2,1)
        #self.widget.setStyleSheet("background-image:url(:/images/Back.png)")
        self.Menu(self)
        self.statusbr(self,d=0)
        self.widget.setLayout(self.layout)

    def Motorcontrol(self):
        groupBox = QtGui.QGroupBox("Motorcontrol")
        clock=AnalogClock()
        vbox=QtGui.QVBoxLayout()
        vbox.addWidget(clock)
        groupBox.setLayout(vbox)


        
        return groupBox
    def Ics(self):
        groupBox = QtGui.QGroupBox("IC's")

        IC1 = QtGui.QPushButton("   ")
        IC2 = QtGui.QPushButton("   ")
        IC3 = QtGui.QPushButton("   ")
        title1 = QtGui.QLabel("Hypersonic")
        title2 = QtGui.QLabel("Bridge Driver")
        title3 = QtGui.QLabel("Aurix")
        title4 = QtGui.QLabel("      ")

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        IC1.setToolTip('Click to go view Hypersonic')
        IC1.setStyleSheet("background-image:url(:/images/powersupply.png)")
        IC1.setFlat(True)
        IC1.setAutoFillBackground(True)
        IC1.setFixedWidth(62)
        IC1.setFixedHeight(62)
        IC2.setToolTip('Click to go view Bridge Driver')
        IC2.setStyleSheet("background-image:url(:/images/bridge.png)")
        IC2.setFlat(True)
        IC2.setAutoFillBackground(True)
        IC2.setFixedWidth(62)
        IC2.setFixedHeight(62)
        IC3.setToolTip('Click to go view Bridge Driver')
        IC3.setStyleSheet("background-image:url(:/images/aurix.tif)")
        IC3.setFlat(True)
        IC3.setAutoFillBackground(True)
        IC3.setFixedWidth(62)
        IC3.setFixedHeight(62)


        group=QtGui.QGridLayout()
        group.addWidget(title1,1,0)
        group.addWidget(title2,2,0)
        group.addWidget(title3,3,0)
        group.addWidget(IC1,1,1)
        group.addWidget(IC2,2,1)
        group.addWidget(IC3,3,1)
        group.addWidget(title4,1,2)
        groupBox.setLayout(group)

        return groupBox
    def Sensors(self):
        groupBox = QtGui.QGroupBox("Sensors")

        sensor1 = QtGui.QPushButton("  ")
        sensor2 = QtGui.QPushButton("  ")
        title1 = QtGui.QLabel("Angle sensor")
        title2 = QtGui.QLabel("Torque sensor")
        title3 = QtGui.QLabel("         ")
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        sensor1.setToolTip('Click to go view Angle sensor data')
        sensor1.setStyleSheet("background-image:url(:/images/Ang.png)")
        sensor1.setFlat(True)
        sensor1.setAutoFillBackground(True)
        sensor1.setFixedWidth(62)
        sensor1.setFixedHeight(62)
        sensor2.setToolTip('Click to go view Torque sensor data')
        sensor2.setStyleSheet("background-image:url(:/images/torque.png)")
        sensor2.setFlat(True)
        sensor2.setAutoFillBackground(True)
        sensor2.setFixedWidth(62)
        sensor2.setFixedHeight(62)
        group=QtGui.QGridLayout()
        group.addWidget(title1,1,0)
        group.addWidget(title2,2,0)
        group.addWidget(title3,1,2)
        group.addWidget(sensor1,1,1)
        group.addWidget(sensor2,2,1)
        groupBox.setLayout(group)

        return groupBox
    def Commandline(self):
        groupBox = QtGui.QGroupBox("Commandline")

        title = QtGui.QLabel("Please Enter Commands")
        text = QtGui.QTextEdit()


        grid = QtGui.QGridLayout()
        grid.addWidget(title,1,0)
        grid.addWidget(text,2,0,2,2)
        groupBox.setLayout(grid)
        return groupBox         

    def statusbr(self,event,d):
        if(d==0):
            self.statusBar().showMessage('Disconnected')
        else:
            self.statusBar().showMessage('Connected')
    def Menu(self,event):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Debug')
        fileMenu.addAction(self.conn)
        fileMenu.addAction(self.disconn)
        self.toolbar = self.addToolBar('Connect')
        self.toolbar.addAction(self.conn)
 
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Do you want to Disconnect and quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def createActions(self):
        self.conn = QtGui.QAction(QtGui.QIcon(':/images/download.jpg'),"&Connect", self,
                statusTip="Connect to a COM PORT", triggered=self.Connect)
        self.disconn = QtGui.QAction("&Disconnect", self,
                statusTip="Disconnect to a COM PORT", triggered=self.Disconnect)
    def Connect(self,event):
        pass
    def Disconnect(self,event):
        pass
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())        