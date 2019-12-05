from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QPalette, QFont
from PyQt5.QtCore import Qt
from enigma import EnigmaMachine
from enigma_config_window import EnigmaConfigWindow
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
        self.setGeometry(x,y,52,53)
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
        if not kwargs:
            kwargs = {
                "pb_map": {},
                "reflector": 'B',
                "rotors": [1,2,3],
                "ringstellung": [1,1,1]
            }
        self.enigma = EnigmaMachine(**kwargs)
        self.title = 'Enigma'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.result = None
        self.keyboard = {}
        self.lamps = {}
        self.visible_settings = {}
        self.initUI()
        self.update_shown_rotor_positions()

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create background
        label = QLabel(self)
        pixmap = QPixmap('images/enigma.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        # Create settings knob
        knob = QPushButton(self)
        knob.setGeometry(551,63,64,64)
        knob.setFixedSize(64,64)
        knob.setFlat(True)
        knob.setStyleSheet("border: 0px; border-radius:32;")
        knob.clicked.connect(self.open_settings)

        # Create visible rotor settings
        for idx, pos in enumerate(("left","middle","right")):
            label = QLabel(self)
            label.setGeometry(140+86*idx, 236, 30, 59)
            label.setStyleSheet('color: white;font: 40px arial')
            label.setAlignment(Qt.AlignCenter)
            self.visible_settings[pos] = label
            # Create rotor to increment values with
            button = QPushButton(self)
            button.setGeometry(188+87*idx, 174, 20, 153)
            button.setFlat(True)
            button.setStyleSheet("border: 0px")
            button.clicked.connect(partial(self.increment_rotor, pos))


        # Create lamps and keyboard
        button_spacing = 22 + 52
        top_row = ['Q','W','E','R','T','Z','U','I','O']
        middle_row = ['A','S','D','F','G','H','J','K']
        bottom_row = ['P','Y','X','C','V','B','N','M','L']            

        for offset, letter in enumerate(top_row):
            lamp = Lamp(80+offset*button_spacing, 410, letter, self)
            button = KeyboardPushButton(80+offset*button_spacing,659,self)
            self.lamps[letter] = lamp
            self.keyboard[letter] = button
            button.pressed.connect(partial(self.key_pressed, letter))
            button.released.connect(partial(self.key_released, letter))

        for offset, letter in enumerate(middle_row):
            lamp = Lamp(117+offset*button_spacing,481,letter,self)
            button = KeyboardPushButton(117+offset*button_spacing,730,self)
            self.lamps[letter] = lamp
            self.keyboard[letter] = button
            button.pressed.connect(partial(self.key_pressed, letter))
            button.released.connect(partial(self.key_released, letter))

        for offset, letter in enumerate(bottom_row):
            lamp = Lamp(80+offset*button_spacing,552,letter,self)
            button = KeyboardPushButton(80+offset*button_spacing,799,self)
            self.lamps[letter] = lamp
            self.keyboard[letter] = button
            button.pressed.connect(partial(self.key_pressed, letter))
            button.released.connect(partial(self.key_released, letter))

        self.show()

    def increment_rotor(self, rotor: str):
        self.enigma.increment_rotor(rotor)
        self.update_shown_rotor_positions()

    def update_shown_rotor_positions(self):
        settings = self.enigma.rotor_positions()
        self.visible_settings['left'].setText(settings[0])
        self.visible_settings['middle'].setText(settings[1])
        self.visible_settings['right'].setText(settings[2])


    def open_settings(self):
        settings_dialog = EnigmaConfigWindow()
        if settings_dialog.exec():
            # Replace our enigma machine with a new one
            self.enigma = EnigmaMachine(**settings_dialog.enigma_settings())
            self.update_shown_rotor_positions()

    def key_pressed(self, letter: str):
        self.keyboard[letter].darken()
        self.result = self.enigma.encrypt(letter)
        self.update_shown_rotor_positions()
        self.lamps[self.result].enable()

    def key_released(self, letter: str):
        self.keyboard[letter].brighten()
        self.lamps[self.result].disable()
        self.result = None

