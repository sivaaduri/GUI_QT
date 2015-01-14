
import sys
from PyQt4 import QtGui, QtCore
import simple_rc
from numpy import matrix
from math import cos,sin,radians
from gauge4 import Gauge
from plot import PLot
class Angle_Sensor(QtGui.QMainWindow):
    def __init__(self):
        super(Angle_Sensor, self).__init__()
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
        self.mainlayout=QtGui.QVBoxLayout()
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.Angle_Value(), 1, 1)
        self.layout.addWidget(self.Plot(), 1, 0)
        self.layout.addWidget(self.Sensors(), 2,0)
        self.layout.addWidget(self.Commandline(), 2,1)
        self.Menu(self)
        self.statusbr(self,d=0)
        self.layout.setColumnMinimumWidth(1,500)
        self.mainlayout.addLayout(self.layout)
        self.widget.setLayout(self.mainlayout)

    def Angle_Value(self):
        groupBox = QtGui.QGroupBox("Angle Value")
        clock=Gauge()
        vbox=QtGui.QVBoxLayout()
        vbox.addWidget(clock)
        groupBox.setLayout(vbox)


        
        return groupBox
    def Plot(self):
        groupBox = QtGui.QGroupBox("Plot")
        plot=PLot()
        vbox=QtGui.QVBoxLayout()
        vbox.addWidget(plot)
        groupBox.setLayout(vbox)
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
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Angle_Sensor()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()