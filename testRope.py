from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor
import sys
import random
import math

class Rope():

    def __init__(self, window):
        self.window = window
        self.number_nodes = 10
        self.anchor1 = None
        self.anchor2 = None
        self.nodes = []

        for i in range(0, self.number_nodes):
            self.nodes.append(QPoint(i*10, i*10))
    
    def update(self):
        #cursor = self.window.mousePos()
        pass

    def setAnchor(self, point, anchor=1):
        if (anchor == 1):
            self.anchor1 = point
        else:
            self.anchor2 = point

    def isClose(self, point):
        if (self.anchor1 != None):
            distToAnchor1 = math.sqrt(math.pow(self.anchor1.x() - point.x(), 2) + math.pow(self.anchor1.y() - point.y(), 2))
            if (distToAnchor1 <= 10):
                return self.anchor1, 1

        if (self.anchor2 != None):
            distToAnchor2 = math.sqrt(math.pow(self.anchor2.x() - point.x(), 2) + math.pow(self.anchor2.y() - point.y(), 2))
            if (distToAnchor2 <= 10):
                return self.anchor2, 2
        return None, None

    def removeAnchor(self, anchor):
        if (anchor == 1):
            self.anchor1 = None
        else:
            self.anchor2 = None
    
    def __repr__(self):
        string = "["
        if (self.anchor1 != None):
            string += "a1: ({0},{1})".format(self.anchor1.x(), self.anchor1.y())
        if (self.anchor2 != None):
            string += "\ta2: ({0},{1})".format(self.anchor2.x(), self.anchor2.y())
        return string + "]"

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
        self.ropes = [] 
        self.cursor = QCursor()
        self.carryingAnchor = False
        self.placingAnchor = False

    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(0, len(self.ropes)):
            rope = self.ropes[i]
            rope.update()
            if (rope.anchor1 != None):
                painter.drawEllipse(rope.anchor1.x(), rope.anchor1.y(), 5, 5)
            if (rope.anchor2 != None):
                painter.drawEllipse(rope.anchor2.x(), rope.anchor2.y(), 5, 5)
            if (rope.anchor1 != None and rope.anchor2 != None):
                painter.drawLine(rope.anchor1, rope.anchor2)
            if (self.carryingAnchor):
                pos = self.mousePos()
                if (pos != None):
                    painter.drawEllipse(pos.x(), pos.y(), 5, 5)
                    if (self.carryingAnchorId == 2):
                        painter.drawLine(pos, self.ropes[self.carryingRopeId].anchor1)
                    elif (self.carryingAnchorId == 1):
                        painter.drawLine(pos, self.ropes[self.carryingRopeId].anchor2)

    def mousePressEvent(self, QMouseEvent):
        pos = self.mousePos()
        ropeAnchor, id = None, None
        i = None
        for i in range(0, len(self.ropes)):
            ropeAnchor, id = self.ropes[i].isClose(pos)
            if (ropeAnchor != None):
                break
        # re-place anchor point
        if (self.carryingAnchor):
            self.ropes[self.carryingRopeId].setAnchor(pos, anchor=self.carryingAnchorId)
            self.carryingAnchor = False
            self.carryingAnchorId = -1
        else:
            # place second anchor
            if(self.placingAnchor == True):
                self.placingAnchor = False
                self.ropes[self.placingAnchorId].setAnchor(pos, 2)
            # new rope
            elif (ropeAnchor == None):
                self.placingAnchor = True
                self.placingAnchorId = len(self.ropes)
                rope = Rope(self)
                rope.setAnchor(pos, 1)
                self.ropes.append(rope)
            # start moving anchor point
            else:
                self.carryingRopeId = i
                self.carryingAnchor = True
                self.carryingAnchorId = id
                self.ropes[i].removeAnchor(id)

    def mousePos(self):
        this = self
        pos = this.mapFromGlobal(self.cursor.pos())
        if (pos.x() <= 500 and
            pos.x() >= 0 and
            pos.y() <= 500 and
            pos.y() >= 0):
            return pos
        return None

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window() 
    timer = QTimer(window)
    timer.timeout.connect(window.update)
    timer.start(33)
    sys.exit(App.exec())    