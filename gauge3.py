import sip
sip.setapi('QVariant', 2)
import sys
from PyQt4 import QtGui, QtCore
import simple_rc

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
        self.setWindowTitle('Draw Image')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.drawImage(event)
        self.qp.setRenderHint(QtGui.QPainter.Antialiasing)
        self.qp.end()
        

    def drawImage(self, event):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()
        newSize=self.size()
        target=QtCore.QRectF(10.0, 10.0, newSize.width()-20, newSize.height()-20);
        source=QtCore.QRectF(0.0, 0.0,self.image.width(),self.image.height()) ;
        transform = QtGui.QTransform()
        transform.rotate(2*time.second())
        print transform.determinant()
        self.qp.setPen(QtGui.QColor(168, 34, 3))
        if  not self.image.load("c:/Users/aduri/Desktop/GUI/Wxpython_gui/qt/GUI_QT/images/gauge.png"):
            s="error loading image"
            print sd
        print self.size()
        self.image= self.image.transformed(transform)
        self.qp.drawImage(target, self.image,source)
        print self.image.trueMatrix

         
                
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()