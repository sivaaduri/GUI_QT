import sip
sip.setapi('QVariant', 2)
import sys
from PyQt4 import QtGui, QtCore
import simple_rc

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.resize(200, 200)
        self.initUI()
        
    def initUI(self):      

        self.image = QtGui.QImage()
        self.setWindowTitle('Draw Image')
        self.show()

    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        
        qp.begin(self)
        self.drawImage(event, qp)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.end()
        

    def drawImage(self, event, qp):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()
        newSize=self.size()
        target=QtCore.QRectF(10.0, 10.0, newSize.width()-20, newSize.height()-20);
        source=QtCore.QRectF(0.0, 0.0,self.image.width(),self.image.height()) ;
        qp.setPen(QtGui.QColor(168, 34, 3))
        if  not self.image.load("c:/Users/aduri/Desktop/GUI/Wxpython_gui/qt/GUI_QT/images/gauge.png"):
            s="error loading image"
            print s
        print self.size()
        qp.drawImage(target, self.image,source)   
    
         
                
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()