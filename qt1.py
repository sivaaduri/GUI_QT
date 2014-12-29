#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

This is a simple drag and drop example. 

author: Jan Bodnar
website: zetcode.com
last edited: October 2013
"""

import sys
from PyQt4 import QtGui


class Button(QtGui.QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)
        
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
      
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
            
        else:
            e.ignore() 

    def dropEvent(self, e):
        
        self.setText(e.mimeData().text()) 


class Example(QtGui.QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        edit = QtGui.QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)
        
        self.setWindowTitle('Simple Drag & Drop')
        self.setGeometry(300, 300, 300, 150)
        self.show()


def main():
  
    app = QtGui.QApplication([])
    ex = Example()
    app.exec_()  
  

if __name__ == '__main__':
    main() 