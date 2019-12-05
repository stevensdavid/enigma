from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QPalette
from enigma import EnigmaMachine
from copy import copy
from functools import partial

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
    def __init__(self, **kwargs):
        super().__init__()
        self.enigma = EnigmaMachine(**kwargs)
        self.title = 'Enigma'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.result = None
        self.keyboard = {}
        self.lamps = {}
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('images/enigma.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        button_spacing = 23+52
        top_row = ['Q','W','E','R','T','Z','U','I','O']
        middle_row = ['A','S','D','F','G','H','J','K']
        bottom_row = ['P','Y','X','C','V','B','N','M','L']
        for offset, letter in enumerate(top_row):
            lamp = Lamp(80+offset*button_spacing,406,letter,self)
            button = KeyboardPushButton(79+offset*button_spacing,659,self)
            self.lamps[letter] = lamp
            self.keyboard[letter] = button
            button.pressed.connect(partial(self.key_pressed, letter))
            button.released.connect(partial(self.key_released, letter))
            # button.pressed.connect(lambda: self.key_pressed(copy(letter)))
            # button.released.connect(lambda: self.key_released(copy(letter)))
        middle_row_spacing = 22+52
        for offset, letter in enumerate(middle_row):
            lamp = Lamp(115+offset*middle_row_spacing,477,letter,self)
            button = KeyboardPushButton(114+offset*middle_row_spacing,730,self)
            self.lamps[letter] = lamp
            self.keyboard[letter] = button
            button.pressed.connect(partial(self.key_pressed, letter))
            button.released.connect(partial(self.key_released, letter))
            # button.pressed.connect(lambda: self.key_pressed(copy(letter)))
            # button.released.connect(lambda: self.key_released(copy(letter)))

        for offset, letter in enumerate(bottom_row):
            lamp = Lamp(80+offset*button_spacing,551,letter,self)
            button = KeyboardPushButton(79+offset*button_spacing,804,self)
            self.lamps[letter] = lamp
            self.keyboard[letter] = button
            button.pressed.connect(partial(self.key_pressed, letter))
            button.released.connect(partial(self.key_released, letter))
            # button.pressed.connect(lambda: self.key_pressed(copy(letter)))
            # button.released.connect(lambda: self.key_released(copy(letter)))

        self.show()

    def key_pressed(self, letter: str):
        self.keyboard[letter].darken()
        self.result = self.enigma.encrypt(letter)
        self.lamps[self.result].enable()

    def key_released(self, letter: str):
        self.keyboard[letter].brighten()
        self.lamps[self.result].disable()
        self.result = None

