from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QColor
import sys
import random
import math
import numpy as np

class Node():
    def __init__(self, x, y):
        self.position = np.array([x,y])
        self.speed = np.array([0,0])
        self.velocity = np.array([0,0])
        self.acceleration = np.array([0,0])

    def update(self):
        # x & y velocity
        self.velocity[0] += self.acceleration[0] * (1/30)
        self.velocity[1] += self.acceleration[1] * (1/30)
        # negative because canvas coordinates inverted
        self.position[0] += self.velocity[0] * (1/30)
        self.position[1] += self.velocity[1] * (1/30)

        # gravity
        self.applyForce([0,9.82])
    
    def applyForce(self, vector):
        self.acceleration[0] += vector[0]
        self.acceleration[1] += vector[1]

class Rope():
    def __init__(self, window):
        self.window = window
        self.number_nodes = 10
        self.anchors = [None, None]
        self.nodes = []
    
    def update(self):
        #cursor = self.window.mousePos()
        """
        force = -k * (x - d)
        k: a constant to represent the stiffness of the spring
        x: distance of the mass from the point it is bound to
        d: a constant positive distance value that a spring stays steady
        """
        self.springConstant = 1
        self.springLength = 5
        self.frictionConstant = 1

        for i in range(0, len(self.nodes)):
            node = self.nodes[i]
            if (i == 0):
                npAnchor = np.array([self.anchors[0].x(), self.anchors[0].y()])
                springVector = npAnchor - node.position 
                length = np.linalg.norm(springVector)
                if (length > 0):
                    f = (springVector / length) * (length - self.springLength) * self.springConstant
                    # force += -(mass1->vel - mass2->vel) * frictionConstant;
                    f += -(node.velocity) * self.frictionConstant
                    node.applyForce(f)
            elif (i == len(self.nodes)-1):
                npAnchor = np.array([self.anchors[1].x(), self.anchors[1].y()])
                springVector = npAnchor - node.position 
                length = np.linalg.norm(springVector)
                if (length > 0):
                    f = (springVector / length) * (length - self.springLength) * self.springConstant
                    f += -(node.velocity) * self.frictionConstant
                    node.applyForce(f)
            else:
                prevNode = self.nodes[i-1]
                nextNode = self.nodes[i+1] 
                f = self.springForce(node, prevNode)
                node.applyForce(f)
                prevNode.applyForce(-f)

                f = self.springForce(node, nextNode)
                node.applyForce(f)
                nextNode.applyForce(-f)

            node.update()

    def springForce(self, node1, node2):
        springVector = node2.position - node1.position 
        length = np.linalg.norm(springVector)
        if (length > 0):
            f = (springVector / length) * (length - self.springLength) * self.springConstant
            f += -(node1.velocity - node2.velocity) * self.frictionConstant
            return f
        return [0,0]

    def setAnchor(self, point, anchor=0):
        if (anchor == 0):
            self.anchors[0] = point
        else:
            self.anchors[1] = point

            # place rope nodes
            x_distance = abs(self.anchors[0].x() - self.anchors[1].x())
            # slope between anchors
            dx = (self.anchors[1].x() - self.anchors[0].x())
            if (dx == 0):
                dx = 1
            m = (self.anchors[1].y() - self.anchors[0].y()) / dx
            step = x_distance / (self.number_nodes + 2)
            #self.number_nodes = int(distance / 10)
            for i in range(0, self.number_nodes):
                if (self.anchors[1].x() >= self.anchors[0].x()):
                    # x += t
                    x = self.anchors[0].x() + step * (i+1)
                    # y += mx
                    y = self.anchors[0].y() + m * ((i+1) * step)
                else:
                    x = self.anchors[0].x() - step * (i+1)
                    y = self.anchors[0].y() - m * ((i+1) * step)
                self.nodes.append(Node(x, y))

    def isClose(self, point):
        id = 0
        for anchor in self.anchors:
            if (anchor != None):
                distToAnchor = self.dist(anchor, point)
                if (distToAnchor <= 10):
                    return anchor, id
            id += 1
        return None, None

    def dist(self, point1, point2):
        return math.sqrt(math.pow(point2.x() - point1.x(), 2) + math.pow(point2.y() - point1.y(), 2))
    
    def __repr__(self):
        string = "["
        for anchor in self.anchors:
            if (anchor != None):
                string += "a: ({0},{1})".format(anchor.x(), anchor.y())
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
            # debug 
            painter.setPen(QPen(Qt.black, 1))
            for node in rope.nodes:
                painter.drawEllipse(node.position[0], node.position[1], 5, 5)

            #painter.setPen(QPen(QColor(76, 18, 0), 10))
            hasBothAnchors = True
            for anchor in rope.anchors:
                if (anchor != None):
                    painter.drawEllipse(anchor.x(), anchor.y(), 5, 5)
                else:
                    hasBothAnchors = False
            if (hasBothAnchors):
                q = QPoint(rope.nodes[0].position[0], rope.nodes[0].position[1])
                painter.drawLine(rope.anchors[0], q)
                q = QPoint(rope.nodes[len(rope.nodes)-1].position[0], rope.nodes[len(rope.nodes)-1].position[1])
                painter.drawLine(rope.anchors[1], q)
                for i in range(1,len(rope.nodes)):
                    q1 = QPoint(rope.nodes[i].position[0], rope.nodes[i].position[1])
                    q2 = QPoint(rope.nodes[i-1].position[0], rope.nodes[i-1].position[1])
                    painter.drawLine(q1, q2)
        if (self.carryingAnchor):
            pos = self.mousePos()
            if (pos != None):
                    rope = self.ropes[self.carryingRopeId]
                    rope.anchors[self.carryingAnchorId] = pos
                #painter.drawEllipse(pos.x(), pos.y(), 5, 5)
                #if (self.carryingAnchorId == 2):
                #    painter.drawLine(pos, self.ropes[self.carryingRopeId].anchors[0])
                #elif (self.carryingAnchorId == 1):
                #    painter.drawLine(pos, self.ropes[self.carryingRopeId].anchors[1])

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
            #self.ropes[self.carryingRopeId].setAnchor(pos, anchor=self.carryingAnchorId)
            self.carryingAnchor = False
            self.carryingAnchorId = -1
        else:
            # place second anchor
            if(self.placingAnchor == True):
                self.placingAnchor = False
                self.ropes[self.placingAnchorId].setAnchor(pos, 1)
            # new rope
            elif (ropeAnchor == None):
                self.placingAnchor = True
                self.placingAnchorId = len(self.ropes)
                rope = Rope(self)
                rope.setAnchor(pos, 0)
                self.ropes.append(rope)
            # start moving anchor point
            else:
                self.carryingRopeId = i
                self.carryingAnchor = True
                self.carryingAnchorId = id
                #self.ropes[i].removeAnchor(id)

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