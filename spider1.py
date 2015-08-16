# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 10:50:57 2015

@author: aduri
"""


import sys
from PyQt4 import QtGui, QtCore, Qt
import simple_rc
from numpy import *
from math import cos,sin,radians
from gauge5 import Gauge
from plot import PLot
from xlrd import open_workbook,cellname
class Brigde_Driver(QtGui.QMainWindow):
    def __init__(self):
        super(Brigde_Driver, self).__init__()
        self.resize(1000,700)
        self.center()
        self.wb = open_workbook('Book1.xlsx')
        self.s = self.wb.sheet_by_index(0)
        self.s1 = self.wb.sheet_by_index(1)
        self.s2 = self.wb.sheet_by_index(2)
        print self.s.name,self.s.nrows,self.s.ncols,self.s1.name,self.s1.nrows,self.s1.ncols,self.s2.name,self.s2.nrows,self.s2.ncols
        self.field=zeros([84,8,2],dtype="S20")
        self.combo=[]
        for i in xrange(84):
            self.combo.append([]) 
        self.combo.append([])
        self.setWindowTitle('OIKOS DEMO BOARD')
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.fields()
        self.setwin()
        
        
        
    def setwin(self):
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.mainlayout=QtGui.QVBoxLayout()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.Commandline())
        #self.layout.setColumnMinimumWidth(1,500)
        self.mainlayout.addLayout(self.layout)
        self.widget.setLayout(self.mainlayout)
 
    def Commandline(self):
        groupBox = QtGui.QGroupBox("Registers")
        scroll = QtGui.QScrollArea()
        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        title = QtGui.QLabel("Please Enter Commands")
        self.text = list()
        widget = QtGui.QWidget()
        grid = QtGui.QVBoxLayout()
        #grid.minimumHeightForWidth(10)
        self.hbox=list()
        rx=QtCore.QRegExp("(?:[0-9 a-f A-F]\\d{1},)*[0-9 a-f A-F]\\d{1}")
        validator =  QtGui.QRegExpValidator(rx)
        for i in xrange(self.s.nrows):
                  x=self.Registers(i)
                  y=self.r_addrs(i)
                  title=QtGui.QLabel(x)
                  title.setFixedWidth(300)
                  title2=QtGui.QLabel(y)
                  hbox=QtGui.QHBoxLayout()
                  vbox=QtGui.QHBoxLayout()
                  hbox.addWidget(title)
                  hbox.addWidget(title2)
                  z=self.how_many_bits(i)
                  for k in xrange(z):
                    self.combo[i].append(QtGui.QComboBox())
                  for k in xrange(len(self.combo[i])):
                    self.combo[i][k].setWindowTitle(x)
                    self.combo[i][k].setMaxCount(2^5-1)
                    self.combo[i][k].currentIndexChanged.connect(self.combs)
                    for l in xrange((2^(int(self.field[i][k][1])-1))):
                        self.combo[i][k].addItem(str(self.field[i][k][0])+" "+str(bin(l)))
                        print (int(self.field[i][k][1])),"so close", str(self.field[i][k][0])
                    vbox.addWidget(self.combo[i][k])
                  self.text.append(QtGui.QLineEdit())
                  self.text[i].AutoNone=0
                  self.text[i].setFixedHeight(30)
                  self.text[i].setFixedWidth(70)
                  self.text[i].setWindowTitle(x)
                  self.text[i].setValidator(validator)
                  self.connect(self.text[i],Qt.SIGNAL("editingFinished()"),self.reg_change)
                  hbox.addWidget(self.text[i])
                  grid.addLayout(hbox)
                  grid.addLayout(vbox)
        widget.setLayout(grid)
        scroll.setWidget(widget)
        vLayout = QtGui.QVBoxLayout(self)
        vLayout.addWidget(scroll)
        groupBox.setLayout(vLayout)
        return groupBox         
    
    def reg_change(self):
        sender = self.sender()
        print str(sender.windowTitle())
    def combs(self):
        sender=self.sender()
        s=str(sender.windowTitle())
        for i in xrange(self.s.nrows):
            if(self.text[i].windowTitle()==s):
              L=i
              break
        z=self.how_many_bits(L)
        self.combo2test(L)
        
    
    def combo2test(self,i):
        z=self.how_many_bits(i)
        s=str("")
        for j in xrange(z): 
            s=s+str(bin(self.combo[i][j].currentIndex()))
        print s
    def command(self,text):
        self.text.setText(text)
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
       
    def Registers(self,i):
        reg=list()
        for row_index in xrange(self.s1.nrows):
            col_index=0
            reg.append(self.s1.cell(rowx=row_index,colx=col_index).value)
        return reg[i]
    def r_addrs(self,i):
        reg_addrs=list()
        for row_index in xrange(self.s.nrows):
            col_index=0
            reg_addrs.append(self.s.cell(rowx=row_index,colx=col_index).value)
        return reg_addrs[i]
    def fields(self):
        reg=0
        for row_index in xrange(self.s2.nrows):
            col_index=0
            if((self.s2.cell(rowx=row_index,colx=col_index).value=="Field")):
                j=0
                row_index=row_index+1
                self.field[reg][j]=str(self.s2.cell(rowx=row_index,colx=col_index).value)
                self.field[reg][j][1]=self.num_bits((self.s2.cell(rowx=row_index,colx=col_index+1).value))
                print self.s2.cell(rowx=row_index,colx=col_index).value
                while(self.s2.cell(rowx=row_index,colx=col_index).value!="Field"):
                    row_index=row_index+1
                    j=j+1
                    if(  row_index==(self.s2.nrows)):
                         break
                    if( (self.s2.cell(rowx=row_index,colx=col_index).value=="Field")):
                         row_index=row_index-1
                         break
                    print self.s2.cell(rowx=row_index,colx=col_index).value,"I am here",j
                    self.field[reg][j]=str(self.s2.cell(rowx=row_index,colx=col_index).value)
                    self.field[reg][j][1]=self.num_bits((self.s2.cell(rowx=row_index,colx=col_index+1).value))
                j=0
                reg=reg+1
                print reg
        print (self.field)
    def num_bits(self,bits):
        c=':'
        try:
				if(bits.find(c)):
					i=bits.find(c)
					k=int(str(bits)[i-1])-int(str(bits)[i+1])+1
					return k
        except:
            return 1
    def how_many_bits(self,i):
        k=0
        for j in xrange(8):
            if(self.field[i][j][0]):
                k=k+1
        return k
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Brigde_Driver()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()