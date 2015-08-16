import PyQt4.QtGui as gui

app = gui.QApplication([])

w = gui.QWidget()

la = gui.QFormLayout()
w.setLayout(la)

tw = gui.QTreeWidget()
sp = tw.sizePolicy()
sp.setVerticalStretch(1)
tw.setSizePolicy(sp)

la.addWidget(tw)

w.show()

app.exec_()