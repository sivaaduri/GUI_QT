import sip
sip.setapi('QVariant', 2)
import sys
from PyQt4 import QtGui, QtCore
import simple_rc
from numpy import matrix
from math import cos,sin,radians

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.resize(200, 200)
        self.qp = QtGui.QPainter()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)
        self.initUI()
        
    def initUI(self):      
        
        self.image = QtGui.QImage()
        self.setWindowTitle('Gauge')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.qp.setRenderHint(QtGui.QPainter.Antialiasing)
        self.drawImage(event)
        self.qp.end()
        

    def drawImage(self, event):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()
        color = QtGui.QColor(255, 0, 0)
        self.qp.setPen(color)
        self.qp.drawPoint(self.size().width()/2, self.size().height()/2)
        color = QtGui.QColor(0, 0, 0)
        self.qp.setPen(color)
        target=QtCore.QRectF(self.size().width()/2, self.size().height()/2, self.size().width()/2.0-20.0, self.size().height()/2.0-20.0)
        centre=QtCore.QPointF(self.size().width()/2, self.size().height()/2)
        print self.size()
        self.qp.setBrush(QtGui.QColor(235, 235, 245,160))
        self.qp.drawEllipse(centre, self.size().width()/2.0-5, self.size().height()/2.-5)
        color = QtGui.QColor(207,207,209)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(207,207,209,160))
        self.qp.drawEllipse(centre, self.size().width()/2.0-10.0, self.size().height()/2.0-10.0)
        color = QtGui.QColor(235, 235, 245)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(235, 235, 245,160))
        self.qp.drawEllipse(centre, self.size().width()/2.0-15.0, self.size().height()/2.0-15.0)
        self.qp.translate(centre)
        color = QtGui.QColor(0,0,0)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(color))
        print cos(radians(90))
        x1=-self.size().width()/100.0
        y1=-self.size().height()/2.0+17
        x2=x1+self.size().width()/40
        y2=y1
        x3=x2
        y3=y1-self.size().height()/20
        x4=x1
        y4=y3
        self.qp.drawRect(-self.size().width()/100.0,-self.size().height()/2.0+17,self.size().width()/40,self.size().height()/20)
        #npx=firstx*cos(radians(30))+firsty*sin(radians(30))
        #npy=-firstx*sin(radians(30))+firsty*cos(radians(30))
        point1=QtCore.QPointF(-10,-10)
        point2=QtCore.QPointF(10,-10)
        point3=QtCore.QPointF(10,10)
        point4=QtCore.QPointF(-10,10)
        self.qp.drawPolygon(point1,point2,point3,point4)
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()