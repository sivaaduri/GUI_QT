
import sys
from PyQt4 import QtGui, QtCore
import simple_rc
from numpy import matrix
from math import cos,sin,radians

class Gauge(QtGui.QWidget):
    
    def __init__(self):
        super(Gauge, self).__init__()
        self.qp = QtGui.QPainter()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)
        self.initUI()
        
    def initUI(self):      
        
        self.image = QtGui.QImage()
        self.setWindowTitle('Gauge')
        self.angle=0
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.qp.setRenderHint(QtGui.QPainter.Antialiasing)
        self.drawImage(event)
        self.qp.end()
        

    def drawImage(self, event):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()
        self.drawouter()
        Hand = QtGui.QPolygon([
        QtCore.QPoint(3, 5),
        QtCore.QPoint(-3, 5),
        QtCore.QPoint(0, -self.size().height()/2+17)])
        self.qp.rotate(self.angle)
        
    

    def drawouter(self):
        color = QtGui.QColor(255, 0, 0)
        self.qp.setPen(color)
        self.qp.drawPoint(self.size().width()/2, self.size().height()/2)
        color = QtGui.QColor(104,109,105,88)
        self.qp.setPen(color)
        radius = min(self.size().width()/2.0, self.size().height()/2.0)
        target=QtCore.QRectF(15.0-radius,15.0-radius, 2*(radius-15.0), 2*(radius-15.0))
        centre=QtCore.QPointF(self.size().width()/2, self.size().height()/2)
        new_centre=QtCore.QPointF(0.0, 0.0)
        print self.size()
        self.qp.setBrush(color)
        self.qp.drawEllipse(centre, radius-5, radius-5)
        color = QtGui.QColor(0,0, 0,160)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(color))
        self.qp.drawEllipse(centre, radius-15.0, radius-15.0)
        self.qp.translate(centre)
        color = QtGui.QColor(37,149,255)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(color))
        self.qp.drawPie(target,0,90*16)
        color = QtGui.QColor(0, 0, 0,160)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(color))
        self.qp.drawEllipse(new_centre, radius-45.0, radius-45.0)
        color = QtGui.QColor(0,0,0)
        self.qp.setPen(color)
        self.qp.setBrush(QtGui.QColor(color))
        w=[5,10,15,0,-15,-10,-5,0]
        
        for i in w:
            self.qp.rotate(45)
            self.qp.setFont(QtGui.QFont('Decorative', min(self.size().width(),self.size().height())/30))
            s=str((i))
            sp=QtCore.QPointF(-self.size().width()/100.0, -self.size().height()/2.0+17+self.size().height()/20+34)
            color = QtGui.QColor(255,255,255)
            self.qp.setPen(color)
            self.qp.drawText(sp,s)  
        
    def chanGe(self,angle):
        self.angle=angle

        """npx=[]
        npy=[]
        point1=[]
        for i in range (0,4):
            npx.append(x1[i]*cos(radians(30))+y1[i]*sin(radians(30)))
            npy.append(-x1[i]*sin(radians(30))+y1[i]*cos(radians(30)))
            point1.append(QtCore.QPointF(x1[i],y1[i]))
        print point1
        self.qp.drawPolygon(point1[0],point1[1],point1[2],point1[3])"""
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Gauge()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()