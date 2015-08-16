# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Dec 13 21:24:32 2014
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(793, 539)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 340, 761, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 581, 321))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setGeometry(QtCore.QRect(610, 10, 151, 311))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButton = QtGui.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 793, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "GroupBox", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))

