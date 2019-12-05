from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor
import sys
import random

class Rope():

    def __init__(self, window):
        self.window = window
        self.number_nodes = 10
        self.cursor = QCursor()
        self.anchor1 = None
        self.anchor2 = None
        self.nodes = []

        for i in range(0, self.number_nodes):
            self.nodes.append(QPoint(i*10, i*10))
    
    def update(self):
        cursor = self.mousePos()

    def mousePos(self):
        pos = self.window.mapFromGlobal(self.cursor.pos())
        if (pos.x() <= 500 and
            pos.x() >= 0 and
            pos.y() <= 500 and
            pos.y() >= 0):
            return pos
        return None

    def setAnchor(self, anchor=1):
        if (anchor == 1):
            self.anchor1 = self.mousePos()
        else:
            self.anchor2 = self.mousePos()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500
        self.initWindow()
        self.initRope()
 
    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def initRope(self):
        self.rope = Rope(self)

    def paintEvent(self, event):
        self.rope.update()
        painter = QPainter(self)
        nodes = self.rope.nodes
        #for i in range(0, len(nodes)):
        #    node = nodes[i]
        #    painter.drawEllipse(node.x(), node.y(), 5, 5)
        if (self.rope.anchor1 != None):
            painter.drawEllipse(self.rope.anchor1.x(), self.rope.anchor1.y(), 5, 5)
        if (self.rope.anchor2 != None):
            painter.drawEllipse(self.rope.anchor2.x(), self.rope.anchor2.y(), 5, 5)
        if (self.rope.anchor1 != None and self.rope.anchor2 != None):
            painter.drawLine(self.rope.anchor1, self.rope.anchor2)

    def mousePressEvent(self, QMouseEvent):
        if (self.rope.anchor1 == None):
            self.rope.setAnchor(1)
        else:
            self.rope.setAnchor(2)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    print(App.screens()[0])
    window = Window() 
    timer = QTimer(window)
    timer.timeout.connect(window.update)
    timer.start(33)
    sys.exit(App.exec())    