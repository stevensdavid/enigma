from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QPalette

class KeyboardPushButton(QPushButton):
    def __init__(self, x:int, y:int, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(x,y,52,52)
        self.setFixedSize(52,52)
        self.setFlat(True)
        self.setStyleSheet("border: 0px; border-radius:26;")
        self.pressed.connect(self.darken)
        self.released.connect(self.brighten)
    
    def darken(self):
        self.setStyleSheet("border: 0px; border-radius:26;background-color: rgba(0,0,0,0.3)")

    def brighten(self):
        self.setStyleSheet("border: 0px; border-radius:26;")

class Lamp(QLabel):
    def __init__(self, x:int, y:int, letter:str, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(x,y,52,52)
        icon = QPixmap(f'images/letters/{letter}.png')
        self.setPixmap(icon)
        self.disable()

    def enable(self):
        self.setVisible(True)

    def disable(self):
        self.setVisible(False)


class EnigmaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Enigma'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.keyboard = {}
        self.lights = {}
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('images/enigma.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        button_spacing = 23
        
        button = KeyboardPushButton(79,659, self)
        lamp = Lamp(80,406,'Q',self)

        self.show()