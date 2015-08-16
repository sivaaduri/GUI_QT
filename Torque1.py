
import sys
from PyQt4 import QtGui, QtCore,Qt
import simple_rc
from numpy import matrix
from math import cos,sin,radians
from gauge5 import Gauge
from plot import PLot
import pyqtgraph as pg
import numpy as np
import pyqtgraph.metaarray as metaarray
from pyqtgraph.flowchart import Flowchart
import pyqtgraph as pg
import numpy as np
import pyqtgraph.console
class Torque_Sensor(QtGui.QMainWindow):
    def __init__(self):
        super(Torque_Sensor, self).__init__()
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
        groupBox = QtGui.QGroupBox("Torque Value")
        self.clock=Gauge()
        #self.clock.setMinimum(-100)
        #self.clock.setMaximum(100)
        #self.clock.setValue(0)
        #self.clock.setTextVisible(True)
        #self.clock1=QtGui.QProgressBar()
        #self.clock1.setInvertedAppearance(True)
        """x=QtGui.QStyleOptionSlider()
        x.orientation=QtCore.Qt.Vertical
        self.clock.initStyleOption()"""
        vbox=QtGui.QHBoxLayout()
        vbox.addWidget(self.clock)
        #vbox.addWidget(self.clock1)
        groupBox.setLayout(vbox)
        return groupBox
    
    def angle(self,angle):
        self.anglee=angle
        #self.clock.chanGe(self.anglee)
        self.plot.datalog(self.anglee)
        self.command(str(self.anglee))
 
    def Plot(self):
        groupBox = QtGui.QGroupBox("Plot")
        self.plot=PLot()
        vbox=QtGui.QVBoxLayout()
        vbox.addWidget(self.plot)
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

        namespace = {'pg': pg, 'np': np}

        ## initial text to display in the console
        text = """
        This is a console. The numpy and pyqtgraph modules have already been imported 
        as 'np' and 'pg'.Please refer to angle_sensor value as Ang, torque_sensor as Tor """
        c = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=text)
        title = QtGui.QLabel("Please Enter Commands")
        grid = QtGui.QVBoxLayout()
        grid.addWidget(c)
        groupBox.setLayout(grid)
        return groupBox         
    
    def command(self,text):
        self.text.setText(text)

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
    ex = Torque_Sensor()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()