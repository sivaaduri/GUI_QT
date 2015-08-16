"""@Package This is the main script which calls other scripts and also invoke Application 
QtGui.QApplication()

"""
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
import sys, serial,traceback,os,time
import simple_rc
from gauge4 import Gauge
from Angle_Sensor import Angle_Sensor
from Torque1 import Torque_Sensor
from OIKOS import OIKOS
from aurix_dmsty import Brigde_Driver
from hypersonic import Hypersonic
import pyqtgraph as pg
import numpy as np
import pyqtgraph.console
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1000,700)
        self.center()
        self.setWindowTitle('OIKOS DEMO BOARD')
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.statusBar().showMessage('Disconnected')
        self.createActions()
        self.a=0b0000
        self.t=0
        self._vt1=1
        self._vt2=1
        self._vref=1
        self.uc=QtCore.Qt.Unchecked
        self.ch=QtCore.Qt.Checked
        self.setwin()
        self.CONNECTED=0
        self.anglee=30
        self.torque=0
        self.continue_samecomm=0
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1)
        
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
        self.layout.addWidget(self.Motorcontrol(), 1, 0)
        self.layout.addWidget(self.Ics(), 1, 1)
        self.layout.addWidget(self.Sensors(), 2,1)
        self.layout.addWidget(self.Commandline(), 2,0)
        #self.widget.setStyleSheet("background-image:url(:/images/Back.png)")
        self.Menu(self)
        self.statusbr(0)
        self.widget.setLayout(self.layout)
    def vt1(self,state):
        if(state==QtCore.Qt.Checked):
           self._vt1=1
        else:
           self._vt1=0
    def vt2(self,state):
        if(state==QtCore.Qt.Checked):
           self._vt2=1
        else:
           self._vt2=0
    def vref(self,state):
        if(state==QtCore.Qt.Checked):
           self._vref=1
        else:
           self._vref=0
    def Motorcontrol(self):
        groupBox = QtGui.QGroupBox("Status Panel")
        groupBox.setFixedWidth(500)
        groupBox.setFixedHeight(300)
        self.aurixv=[]
        self.aurixvt=[]
        self.hyperstat=QtGui.QLabel("Status of Hypersonic")
        self.hyperstat1=QtGui.QLineEdit()
        self.bridgestat=QtGui.QLabel("Status of Bridge Driver")
        self.bridgestat1=QtGui.QLineEdit()
        self.aurixstat=QtGui.QLabel("Status of Aurix")
        self.aurixstat1=QtGui.QLineEdit()
        self.aurixstat1.setText("Normal")
        self.hypv=[]
        self.hypvt=[]
        for i in xrange(3):
           self.hypv.append(QtGui.QCheckBox())
           self.hypvt.append(QtGui.QLineEdit())
           self.hypv[i].setCheckState(self.ch)
        self.hypv[2].stateChanged.connect(lambda: self.vref)
        self.hypv[0].stateChanged.connect(lambda: self.vt1)
        self.hypv[1].stateChanged.connect(lambda: self.vt2)
        self.hypvt[0].setText("V Tracker 1")
        self.hypvt[1].setText("V Tracker 2")
        self.hypvt[2].setText("V Reference")
        hbox=QtGui.QGridLayout()
        self.aurixvt.append(QtGui.QLabel("Aurix Core Voltage"))
        self.aurixvt.append(QtGui.QLabel("Aurix Supply Voltage"))
        self.aurixvt.append(QtGui.QLabel("Aurix ADC Ref. Voltage"))
        for i in xrange(3):
           self.aurixv.append(QtGui.QLCDNumber())
           self.aurixv[i].setDecMode()
           self.aurixv[i].setDigitCount(4)
           hbox.addWidget(self.aurixv[i],0,i)
           hbox.addWidget(self.aurixvt[i],1,i)
           hbox.addWidget(self.hypv[i],4,i)
           hbox.addWidget(self.hypvt[i],5,i)
           hbox.setSpacing(10)
        hbox.addWidget(self.hyperstat,2,0)
        hbox.addWidget(self.hyperstat1,3,0)
        hbox.addWidget(self.bridgestat,2,1)
        hbox.addWidget(self.bridgestat1,3,1)
        hbox.addWidget(self.aurixstat,2,2)
        hbox.addWidget(self.aurixstat1,3,2)
        
        vbox=QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
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
        IC2.clicked.connect(self.bridge)
        IC1.clicked.connect(self.hypersonic)
        return groupBox
    def Sensors(self):
        groupBox = QtGui.QGroupBox("Sensors")

        self.sensor1 = QtGui.QPushButton("  ")
        self.sensor2 = QtGui.QPushButton("  ")
        title1 = QtGui.QLabel("Angle sensor")
        title2 = QtGui.QLabel("Torque sensor")
        title3 = QtGui.QLabel("         ")
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.sensor1.setToolTip('Click to go view Angle sensor data')
        self.sensor1.setStyleSheet("background-image:url(:/images/Ang.png)")
        self.sensor1.setFlat(True)
        self.sensor1.setAutoFillBackground(True)
        self.sensor1.setFixedWidth(62)
        self.sensor1.setFixedHeight(62)
        self.sensor2.setToolTip('Click to go view Torque sensor data')
        self.sensor2.setStyleSheet("background-image:url(:/images/torque.png)")
        self.sensor2.setFlat(True)
        self.sensor2.setAutoFillBackground(True)
        self.sensor2.setFixedWidth(62)
        self.sensor2.setFixedHeight(62)
        group=QtGui.QGridLayout()
        group.addWidget(title1,1,0)
        group.addWidget(title2,2,0)
        group.addWidget(title3,1,2)
        group.addWidget(self.sensor1,1,1)
        group.addWidget(self.sensor2,2,1)
        groupBox.setLayout(group)
        self.sensor1.clicked.connect(self.ang1)
        self.sensor2.clicked.connect(self.tor1)
        return groupBox
    def hypersonic(self):
        self.hyp=Hypersonic()
        self.hyp.show()
    def ang1(self):
        self.ann=Angle_Sensor()
        self.a=1
        self.ann.show()
        self.ang2(self.anglee)
    def ang2(self,angle):
        self.ann.angle(self.anglee)
    def tor1(self):
        self.tor=Torque_Sensor()
        self.t=1
        self.tor.show()
    def tor2(self,angle):
        self.torque=angle
        self.tor.angle(angle)
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
    def bridge(self):
        self.driver=Brigde_Driver()
        self.driver.show()
    def statusbr(self,d):
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
        if(self.CONNECTED==1):
            reply = QtGui.QMessageBox.question(self, 'Message',
            "Do you want to Disconnect and quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        else:
            event.accept()
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
        self.connect_oikos()
        if self.c==1:
            self.statusbr(1)
            self.CONNECTED=1
    def Disconnect(self,event):
        self.ser.close()
        self.CONNECTED=0
        self.statusbr(0)
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def update(self):
        if self.CONNECTED==1:
           self.update_oikos()
           self.anglee=self.angle
           #print self.anglee
    def connect_oikos(self):
        print "Connecting"
        self.ser=serial.Serial(17,baudrate=115200,timeout=.05)
        try:
           self.c=1
           self.angle=0
           if(self.continue_samecomm==0):
               c1=self.aurix_communication(1,0,0)
           self.ser.close()
           
        except:
            self.c=0
            traceback.print_exc(file=sys.stdout)
            self.ser.close()
        print "Connected"
    def update_oikos(self):
        try:
           self.c=1
           self.angle=0
           
           n=11
           """if((self._vt1==1)&(self._vt2==1)&(self._vref==1)):
                 self.ser.write("5")
           elif((self._vt1==0)&(self._vt2==1)&(self._vref==1)):
                 self.ser.write("2")
           elif((self._vt1==1)&(self._vt2==0)&(self._vref==1)):
                 self.ser.write("3")
           elif((self._vt1==1)&(self._vt2==0)&(self._vref==1)):
                 self.ser.write("4")"""
           if(self.continue_samecomm==0):
                self.c1=self.aurix_communication(1,0,0)
                self.sensor_update()
           a=self.driver.aurix_xomm(1)
           d=self.driver.aurix_xomm(2)
           a1=self.hyp.aurix_xomm(1)
           d1=self.hyp.aurix_xomm(2)
           f=self.aurix_communication(3,a1,d1)
           f=self.aurix_communication(4,a,d)
           
        except:
            self.c=0
            traceback.print_exc(file=sys.stdout)
            self.ser.close()
    def hypst(self,x):
        return {
                 1:"Init",
                 2:"Normal",
                 3:"Sleep",
                 4:"STBY",
                 5:"WAKE",
                   }.get(x,"Reserved")
    def bridst(self,x):
        return {
                 0x80:"Normal Driving Mode on",
                 0: "Normal Driving Mode off",
                }.get(x,"Reserved")
    def aurix_communication(self,c,a,d):
        
        if(c==1):
           n=11
           self.ser.close()
           self.ser.open()
           s="%up"
           c="0EEA$"
           s=s+c
           print s
           for i in range(0,len(s)):
	          self.ser.write(s[i])
	          time.sleep(.01)
           f=self.ser.readline()
        if(c==2):
           self.ser.close()
           self.ser.open()
           s="%bw"
           a1=str(a).replace("H","")
           c=a1+str(d)+"$"
           s=s+c
           for i in range(0,len(s)):
	          self.ser.write(s[i])
	          time.sleep(.01)
           f=self.ser.readline()
        if(c==3):
           self.ser.close()
           self.ser.open()
           s="%hw"
           e="0"
           if(len(str(a))<2):
              a=e+str(a)
              print a
           a1=str(a).replace("H","")
           c=a1+str(d)+"$"
           s=s+c
           print s,"_____________________"
           for i in range(0,len(s)):
	          self.ser.write(s[i])
	          time.sleep(.01)
           f=self.ser.readline()
        if(c==4):
           self.ser.close()
           self.ser.open()
           s="%bw"
           a1=str(a).replace("H","")
           c=a1+str(d)+"$"
           s=s+c
           print s,"_____________________"
           for i in range(0,len(s)):
	          self.ser.write(s[i])
	          time.sleep(.01)
           f=self.ser.readline()
        return f
    def sensor_update(self):
       print self.c1
	   #print len(c1)
       if(self.c1==0):
          print "unsuccessful Read",c1
          return
       x=0b0000;
       x=ord(self.c1[1]);
       x=x<<8|ord(self.c1[0]) 
       self.angle=x
       self.ser.close()
       if(self.a):
		   self.ang2(self.angle)
       if(self.t):
           self.tor2((ord(self.c1[2])+ord(self.c1[3])/2))
       self.aurixv[0].display(5.7692*(ord(self.c1[4])-1)*.001)
       self.aurixv[1].display((23.077*(ord(self.c1[5])-1)*.001)) 
       self.aurixv[2].display((23.077*(ord(self.c1[6])-1)*.001))
       self.hypersonic_status=ord(self.c1[7])
       z=0x07&self.hypersonic_status
       self.hyperstat1.setText(self.hypst(z))
       #self.bridge_status=ord(self.c1[8])
       #self.bridgestat1.setText(self.bridst(self.bridge_status&0x80))
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())        