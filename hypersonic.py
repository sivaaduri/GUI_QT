
import sys
from PyQt4 import QtGui, QtCore, Qt
import simple_rc
from numpy import *
from math import cos,sin,radians
from gauge5 import Gauge
from plot import PLot
from xlrd import open_workbook,cellname
import pyqtgraph as pg
import numpy as np
import pyqtgraph.metaarray as metaarray
from pyqtgraph.flowchart import Flowchart
class Hypersonic(QtGui.QMainWindow):
    def __init__(self):
        super(Hypersonic, self).__init__()
        self.resize(1000,700)
        self.center()
        self.wb = open_workbook('Book1.xlsx')
        self.s = self.wb.sheet_by_index(4)
        self.s1 = self.wb.sheet_by_index(5)
        self.s2 = self.wb.sheet_by_index(7)
        self.s3= self.wb.sheet_by_index(6)
        self.aurix_add="ffH"
        self.aurix_data="ff"
        #print self.s.name,self.s.nrows,self.s.ncols,self.s1.name,self.s1.nrows,self.s1.ncols,self.s2.name,self.s2.nrows,self.s2.ncols
        self.field=zeros([84,8,2],dtype="S20")
        self.combo=[]
        for i in xrange(84):
            self.combo.append([]) 
        self.combo.append([])
        self.setWindowTitle('OIKOS DEMO BOARD')
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.Registers_init()
        self.r_addrs_init()
        self.defaults_init()
        self.fields_init()
        self.setwin()
        
        
        
    def setwin(self):
        self.widget = QtGui.QWidget()
        self.setCentralWidget(self.widget)
        self.mainlayout=QtGui.QVBoxLayout()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.Commandline())
        self.layout1 = QtGui.QVBoxLayout()
        self.layout1.addWidget(self.Plot())
        self.layout2 = QtGui.QVBoxLayout()
        self.layout2.addWidget(self.panel())
        self.tabs=QtGui.QTabWidget()
        #self.tab_bar = QtGui.QTabBar(self.tabs)
        tab1 = QtGui.QWidget()
        tab1.setLayout(self.layout)
        self.tabs.addTab(tab1,'Main_Page')
        tab2 = QtGui.QWidget()
        tab2.setLayout(self.layout1)
        self.tabs.addTab(tab2,'Magic')
        self.mainlayout.addWidget(self.tabs)
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
                  x=str(self.Registers(i))
                  y=str(self.r_addrs(i))
                  title=QtGui.QPushButton(x)
                  title.setFixedWidth(500)
                  title.setFixedHeight(45)
                  title.setFont(QtGui.QFont('TimesRoman', 9.5))
                  title2=QtGui.QLabel(y)
                  title2.setFixedWidth(50)
                  title2.setFont(QtGui.QFont('TimesRoman', 9))
                  hbox=QtGui.QHBoxLayout()
                  vbox=QtGui.QHBoxLayout()
                  hbox.addWidget(title)
                  hbox.addWidget(title2)
                  z=self.how_many_bits(i)
                  for k in xrange(z):
                    self.combo[i].append(QtGui.QComboBox())
                  for k in xrange(len(self.combo[i])):
                    self.combo[i][k].setWindowTitle(x)
                    self.combo[i][k].setMaxCount(2**8-1)
                    
                    if(2**(int(self.field[i][k][1]))<=0):
                        print 2**(int(self.field[i][k][1])),"yes problem",int(self.field[i][k][1])
                        raise SystemExit()
                    for l in xrange((2**(int(self.field[i][k][1])))):
                        self.combo[i][k].addItem(str((self.field[i][k][0]))+" "+str(int(l)))
                        #print (int(self.field[i][k][1])),"so close", str(self.field[i][k][0])
                    self.combo[i][k].setFixedHeight(35)
                    self.combo[i][k].setFixedWidth(100)
                    vbox.addWidget(self.combo[i][k])
                  self.text.append(QtGui.QLineEdit())
                  self.text[i].AutoNone=0
                  self.text[i].setFixedHeight(30)
                  self.text[i].setFixedWidth(70)
                  self.text[i].setWindowTitle(x)
                  #self.text[i].setValidator(validator)
                  self.text[i].setText(self.default(i))
                  #self.connect(self.text[i],Qt.SIGNAL("editingFinished()"),self.reg_change)
                  self.connect(self.text[i],Qt.SIGNAL("textChanged()"),self.reg_change)
                  self.text[i].editingFinished.connect(self.reg_change)
                  self.text[i].textChanged.connect(lambda: self.reg_change)
                  #self.text[i].returnPressed.connect(lambda: self.reg_change)
                  for k in xrange(len(self.combo[i])):
                    self.combo[i][k].currentIndexChanged.connect(self.combs)
                  hbox.addWidget(self.text[i])
                  grid.addLayout(hbox)
                  grid.addSpacing(10)
                  grid.addLayout(vbox)
        widget.setLayout(grid)
        scroll.setWidget(widget)
        vLayout = QtGui.QVBoxLayout(self)
        vLayout.addWidget(scroll)
        groupBox.setLayout(vLayout)
        return groupBox         
    def Plot(self):
        groupBox = QtGui.QGroupBox("Plot")
        fc = Flowchart(terminals={'For PWM Outputs': {'io': 'in'},'Angle_Value': {'io': 'out'},'Torque_value':{'io':'out'}})
        w = fc.widget()
        #self.plot=PLot()
        ## Add two plot widgets
        pw1 = pg.PlotWidget()
        pw2 = pg.PlotWidget()
        vbox=QtGui.QVBoxLayout()
        ctrl = fc.ctrlWidget()
        
        #vbox.addWidget(self.plot)
        vbox.addWidget((fc.widget()))
        vbox.addWidget(ctrl)
        vbox.addWidget(pw1)
        vbox.addWidget(pw2)
        groupBox.setLayout(vbox)
        return groupBox

    def panel(self):
        pass


    def reg_change(self):
        sender = self.sender()
        self.aurix_add=self.reg_addrs[self.reg.index(str(sender.windowTitle()))]
        self.aurix_data=str(sender.text())
        print self.aurix_data
    def combs(self):
        sender=self.sender()
        s=str(sender.windowTitle())
        for i in xrange(len(self.text)):
            if(self.text[i].windowTitle()==s):
              #print s,i,type(i)
              break
        z=self.how_many_bits(i)
        d=int(self.combo2test(i),2)
        print hex(d)
        self.text[i].setText(QtCore.QString(hex(d)[2:4]))
    
    def combo2test(self,i):
        z=self.how_many_bits(i)
        s=0
        s1=0
        for j in xrange(z):
            d=(bin(2**int(self.field[i][j][1])-1))
            e=d[2::]
            f=bin(((self.combo[i][j].currentIndex())<<(8-(len(e))-s1)))
            
            s=(s)+int(f,2)
            #print f,bin(s),len(f),len(bin(s)[2::])
            #print d,e,s1,j,bin(2**int(self.field[i][j][1])-1),int(self.combo[i][j].currentIndex()),(8-(len(e))-s1)
            s1=len(e)+s1
        #print bin(s),len(bin(s)[2::])
        return bin(s)
    def command(self,text):
        self.text.setText(text)
        QtGui.QApplication.instance().processEvents()
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
       
    def Registers_init(self):
        self.reg=list()
        for row_index in xrange(self.s1.nrows):
            col_index=0
            self.reg.append(self.s1.cell(rowx=row_index,colx=col_index).value)
        return 1
    def Registers(self,i):
        return self.reg[i]
    def r_addrs_init(self):
        self.reg_addrs=list()
        for row_index in xrange(self.s.nrows):
            col_index=0
            self.reg_addrs.append(self.s.cell(rowx=row_index,colx=col_index).value)
        return 1
    def r_addrs(self,i):
        return self.reg_addrs[i]
    def fields_init(self):
        reg=0
        for row_index in xrange(self.s2.nrows):
            col_index=0
            if((self.s2.cell(rowx=row_index,colx=col_index).value=="Field")):
                j=0
                row_index=row_index+1
                self.field[reg][j]=str(self.s2.cell(rowx=row_index,colx=col_index).value)
                self.field[reg][j][1]=self.num_bits((self.s2.cell(rowx=row_index,colx=col_index+1).value))
                #print self.s2.cell(rowx=row_index,colx=col_index).value
                while(self.s2.cell(rowx=row_index,colx=col_index).value!="Field"):
                    row_index=row_index+1
                    j=j+1
                    if(  row_index==(self.s2.nrows)):
                         break
                    if( (self.s2.cell(rowx=row_index,colx=col_index).value=="Field")):
                         row_index=row_index-1
                         break
                    #print self.s2.cell(rowx=row_index,colx=col_index).value,"I am here",j
                    self.field[reg][j]=str(self.s2.cell(rowx=row_index,colx=col_index).value)
                    self.field[reg][j][1]=self.num_bits((self.s2.cell(rowx=row_index,colx=col_index+1).value))
                j=0
                reg=reg+1
                #print reg
        #print (self.field)
    def defaults_init(self):
        self._default=list()
        for row_index in xrange(self.s1.nrows):
            col_index=0
            self._default.append(self.s3.cell(rowx=row_index,colx=col_index).value)
        return 1
    def default(self,i):
        return self._default[i]
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
    def aurix_xomm(self,n):
        a=self.aurix_add
        d=self.aurix_data
        
        if(n==1):
          #self.aurix_add="ffH"
          return a
        else:
          #self.aurix_data="ff"
          return d
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Hypersonic()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()