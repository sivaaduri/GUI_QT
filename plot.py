import sys
from PyQt4 import QtGui,QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

import random

class PLot(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PLot, self).__init__(parent)
        self.resize(50,50)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Clear')
        self.button.clicked.connect(self.clean)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.data=[0]
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        #self.data = [random.random() for i in range(10)]

        # create an axis
        self.ax = self.figure.add_subplot(111)

        # discards the old graph
        self.ax.hold(False)

        # plot data
        #ax.plot(self.data, '-')
        self.ax.plot(self.data)

        # refresh canvas
        self.canvas.draw()
	
    def label(self,xlabel,ylabel,title):
        self.ax.ylabel('Torque_Value')
        self.ax.xlabel('Samples')
        self.ax.title('Torque_Sensor')
    def datalog(self,data):
        self.data.append(data)
    def clean(self):
        self.data=[0]
    def update(self):
        self.plot()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = PLot()
    main.show()

    sys.exit(app.exec_())