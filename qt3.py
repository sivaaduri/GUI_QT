from PyQt4 import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem
from demoscene import DemoScene
from demotextitem import DemoTextItem
from imageitem import ImageItem
from menumanager import MenuManager


class MainWindow(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.updateTimer = QtCore.QTimer(self)
        self.demoStartTime = QtCore.QTime()
        self.fpsTime = QtCore.QTime()
        self.background = QtGui.QPixmap()

        self.scene = None
        self.mainSceneRoot = None
        self.frameTimeList = []
        self.fpsHistory = []

        self.currentFps = Colors.fps
        self.fpsMedian = -1
        self.fpsLabel = None
        self.pausedLabel = None
        self.doneAdapt = False
        self.useTimer = False
        self.updateTimer.setSingleShot(True)
        self.companyLogo = None
        self.qtLogo = None

        self.setupWidget()
        """self.setupScene()
        self.setupSceneItems()
        self.drawBackgroundToPixmap()"""

    def setupWidget(self):
        desktop = QtGui.QApplication.desktop()
        screenRect = desktop.screenGeometry(desktop.primaryScreen())
        windowRect = QtCore.QRect(0, 0, 800, 600)

        if screenRect.width() < 800:
            windowRect.setWidth(screenRect.width())

        if screenRect.height() < 600:
            windowRect.setHeight(screenRect.height())

        windowRect.moveCenter(screenRect.center())
        self.setGeometry(windowRect)
        self.setMinimumSize(80, 60)

        self.setWindowTitle("PyQt Examples and Demos")
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        #self.setRenderingSystem()
        self.updateTimer.timeout.connect(self.tick)
        quit = QtGui.QPushButton('Close',self)
        quit.setGeometry(10,10,70,40)
        self.connect(quit,QtCore.SIGNAL( "clicked() " ), QtGui.qApp,QtCore.SLOT( "quit() " ))

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())