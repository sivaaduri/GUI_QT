from PyQt4 import QtCore, QtGui
import sys
import simple_rc

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

        IC1 = QtGui.QPushButton("&Hypersonic")
        IC2 = QtGui.QPushButton("Bridge Driver")
        IC3 = QtGui.QPushButton("Aurix")


        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(IC1)
        vbox.addWidget(IC2)
        #vbox.addWidget(IC3)
        vbox.addStretch(2)
        groupBox.setLayout(vbox)
        return groupBox
    def Ics(self):
        groupBox = QtGui.QGroupBox("IC's")

        IC1 = QtGui.QPushButton("&Hypersonic")
        IC2 = QtGui.QPushButton("Bridge Driver")
        IC3 = QtGui.QPushButton("Aurix")
        

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(IC1)
        vbox.addWidget(IC2)
        vbox.addWidget(IC3)
        vbox.addStretch(2)
        groupBox.setLayout(vbox)

        return groupBox
    def Sensors(self):
        groupBox = QtGui.QGroupBox("Sensors")

        sensor1 = QtGui.QPushButton("Ang")
        sensor2 = QtGui.QPushButton("Torque Sensor")
        title = QtGui.QLabel("Angle sensor")
        sensor1.resize(10,10)
        sensor2.resize(10,10)
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        sensor1.setToolTip('Click to go view Angle sensor data')
        sensor1.setStyleSheet("background-image:url(:/images/Ang.png)")
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel("Angle Sensor"), sensor1)
        layout.addRow(QtGui.QLabel("Torque Sensor"), sensor2)
        layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        groupBox.setLayout(layout)

        return groupBox
    def Commandline(self):
        groupBox = QtGui.QGroupBox("Commandline")

        sensor1 = QtGui.QPushButton("&Angle Sensor")
        sensor2 = QtGui.QPushButton("Torque Sensor")
        sensor1.resize(70,70)
        sensor2.resize(70,70)
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        sensor1.setToolTip('Click to go view Angle sensor data')
        sensor1.setStyleSheet("background-image:url(:/images/Ang.png)")


        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(sensor1)
        vbox.addWidget(sensor2)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
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