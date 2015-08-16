# -*- coding:utf-8 -*-
"""
Created on 20110704

@author: heinzale
"""
import cPickle  
import serial
from PyQt4 import QtGui, QtCore
from serial_connection import serial_connection
import re, sys
import platform


class ConfigDialog(QtGui.QDialog):
    
    def __init__(self,baud_rate=19200,auto_connect=False):
        
        QtGui.QWidget.__init__(self)
        self.baud_rate=baud_rate
        
        self.connection = None
        self.config = ConnectionConfig().load()
            
#        self.setFixedSize(245, 150)
        self.setModal(True)
        
        self.setWindowTitle('configure connection')
        layout = QtGui.QGridLayout();
        layout.setColumnStretch(0,0)
        layout.setColumnStretch(1,0)
        layout.setColumnMinimumWidth(1,90)
        layout.setColumnStretch(2,1)
        
        label = QtGui.QLabel();
        label.setText("serial port:")
        self.addr_label = label
        layout.addWidget(label,0,0,1,1)
        
        addr = QtGui.QComboBox()
        addr.setEditable(False)
#        addr.setMinimumWidth(140)
        self.addr = addr
        layout.addWidget(addr,0,1,1,1)
        
        self.timer=QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)
        
        self.ifx_ucs=self.get_ifx_com_ports()

        if platform.system()=='Windows':
            wrn_label = QtGui.QLabel();
            wrn_label.setText("a warning with a fairly long text")
            self.wrn_label = wrn_label
            self.wrn_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(self.wrn_label,1,0,1,2)
            
            self.connect(self.addr,QtCore.SIGNAL('currentIndexChanged(QString)'), self.port_changed)

        self.connect_button = QtGui.QPushButton("connect")
        self.connect(self.connect_button,QtCore.SIGNAL('clicked(bool)'), self.connectPressed)
        layout.addWidget(self.connect_button,2,1,1,1)
        
        self.work_offline_button = QtGui.QPushButton("work offline")
        self.connect(self.work_offline_button,QtCore.SIGNAL('clicked(bool)'), self.exitPressed)
        layout.addWidget(self.work_offline_button,2,0,1,1)
        
        self.setLayout(layout)
        
        import time
        self.portSelect(self.config.port)
        
        flags=self.windowFlags()
        flags&= (~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(flags)
        
        if auto_connect and not self.timer.isActive():
            self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.connectPressed)
            self.timer.start()
        
    def port_changed(self,port_name):
        if port_name in self.ifx_ucs:
            self.wrn_label.setText("(%s should be ok)"%port_name)
        else:
            txt="(%s might be incorrect)"%port_name
            self.wrn_label.setText(txt)
            
    def __get_driver_installed(self):
        if platform.system()!='Windows':
            return False
        try:
            import _winreg as winreg
            
            path = 'SYSTEM\\CurrentControlSet\\services\\FTSER2K'
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            no_device_nodes=winreg.QueryInfoKey(key)[0]
            if no_device_nodes>0:
                return True
        except:
            return False
        return False
        
    def get_ifx_com_ports(self):
        result=[]
        
        if platform.system()!='Windows':
            return result
        try:
            import _winreg as winreg
            path = 'SYSTEM\\CurrentControlSet\\Enum\\FTDIBUS'
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

            no_device_nodes=winreg.QueryInfoKey(key)[0]
            
            for i in range(no_device_nodes):
                ftdi_sub_node_str = winreg.EnumKey(key, i)
                ftdi_path=path+'\\'+ftdi_sub_node_str
                ftdi_node=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ftdi_path)
                ftdi_node_info=winreg.QueryInfoKey(ftdi_node)
                
                no_of_sub_nodes=ftdi_node_info[0]
                
                if no_of_sub_nodes!=1:
                    continue
                
                sub_node_0000_str=winreg.EnumKey(ftdi_node, 0)
                sub_node_0000_path=ftdi_path+'\\'+sub_node_0000_str
                sub_node_0000=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_node_0000_path)
                
                friendly_name_tuple=winreg.QueryValueEx(sub_node_0000,'FriendlyName')
                friendly_name=friendly_name_tuple[0]
                
                m=re.match(r"^Infineon.+USB COM Port \((COM\d+)\)$",friendly_name)
                
                if m:
                    port_no=str(m.group(1))
                    result.append(port_no)
            return result
        except:
            return result
        
        
    def portSelect(self,port):
        self.addr.clear()
        for i in range(256):
            try:
                s = serial.Serial(i)
                self.addr.addItem(s.portstr)
#                        available.append( (i, s.portstr))
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        no_of_items=self.addr.count()
        #set default according to config
        default_set=False
        if len(port) != 0:
            saved=self.config.port
            idx=self.addr.findText(saved) #is it included in the list
            if idx>=0:
                self.addr.setCurrentIndex(idx)
                default_set=True
        if not default_set:
#            ifx_ucs=self.get_ifx_com_ports()
            for idx in range(no_of_items):
                if self.addr.itemText(idx) in self.ifx_ucs:
                    self.addr.setCurrentIndex(idx)
                    default_set=True
                    break
        self.addr.setFocus()
        
        if no_of_items==0:
            msg="COM port unavailable or busy.\nFalling back to 'work offline' mode"
#            QtGui.QMessageBox.critical(None,"COM port error",msg)
            self.connect_button.setDisabled(True)
            
            QtGui.QMessageBox.information(None,"COM port error",msg)
            
            QtCore.QObject.connect(self.timer,QtCore.SIGNAL('timeout()'), self.exitPressed)
            self.timer.start()
#            sys.exit(0)
            
    def connectPressed(self):  
        self.setWindowTitle("connecting...") 
        try:
            port=str(self.addr.currentText())
            self.connection = serial_connection(port,self.baud_rate)
            self.config.save(port)
            self.done(1)
            return
            QtGui.QMessageBox.critical(self,"invalid input",\
                        "given serial port is invalid!<br>Port: com-port")
        except Exception, e:
            print e
            QtGui.QMessageBox.critical(self,"connection error!",str(e))
            self.setWindowTitle('configure connection')
        
    def exitPressed(self):
        self.connection = None
        self.done(1)
#        sys.exit(0)
        
    def closeEvent(self, evt):
        sys.exit(0)
      
class ConnectionConfig:

    def __init__(self):
        
        self.config_file = "config.pkl"
        self.port=str()
    
    def load(self):
        try:
            fd = open(self.config_file,"rb")
            return cPickle.load(fd)   
        except:
            return self
        
    def save(self, port):
        self.port = port
        
        fd = open(self.config_file,"wb")
        cPickle.dump(self,fd,cPickle.HIGHEST_PROTOCOL)
        fd.close()