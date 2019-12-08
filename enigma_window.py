from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QPalette, QFont
from PyQt5.QtCore import Qt
from enigma import EnigmaMachine
from enigma_config_window import EnigmaConfigWindow
from copy import copy
from functools import partial

class KeyboardPushButton(QPushButton):
    def __init__(self, x:int, y:int, scale: float, parent=None):
        super().__init__(parent=parent)
        dim = 52 * scale
        self.setGeometry(x,y,dim,dim)
        self.setFixedSize(dim,dim)
        self.setFlat(True)
        self.bright_style = f"border: 0px; border-radius:{dim/2};"
        self.dark_style = f"border: 0px; border-radius:{dim/2}" + \
            ";background-color: rgba(0,0,0,0.3)"
        self.setStyleSheet(self.bright_style)
        self.pressed.connect(self.darken)
        self.released.connect(self.brighten)
    
    def darken(self):
        self.setStyleSheet(self.dark_style)

    def brighten(self):
        self.setStyleSheet(self.bright_style)

class Lamp(QLabel):
    def __init__(self, x:int, y:int, letter:str, 
                 scale:float, parent=None):
        super().__init__(parent=parent)
        icon = QPixmap(f'images/letters/{letter}.png')
        icon = icon.scaled(icon.width() * scale, icon.height() * scale)
        self.setGeometry(x,y,icon.width(),icon.height())
        self.setPixmap(icon)
        self.disable()

    def enable(self):
        self.setVisible(True)

    def disable(self):
        self.setVisible(False)


class EnigmaWindow(QWidget):
    def __init__(self, scale, **kwargs):
        super().__init__()
        if not kwargs:
            kwargs = {
                "pb_map": {},
                "reflector": 'B',
                "rotors": [1,2,3],
                "ringstellung": [1,1,1]
            }
        self.scale = scale
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
        scale = self.scale
        pixmap = pixmap.scaled(pixmap.width()*scale, pixmap.height()*scale)

        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())

        # Create settings knob
        knob = QPushButton(self)
        knob.setGeometry(551*scale,63*scale,64*scale,64*scale)
        knob.setFixedSize(64*scale,64*scale)
        knob.setFlat(True)
        knob.setStyleSheet(f"border: 0px; border-radius:{32*scale};")
        knob.clicked.connect(self.open_settings)

        # Create visible rotor settings
        for idx, pos in enumerate(("left","middle","right")):
            label = QLabel(self)
            label.setGeometry((140+86*idx)*scale, 236*scale, 30*scale, 59*scale)
            label.setStyleSheet(f'color: white;font: {int(40*scale)}px arial')
            label.setAlignment(Qt.AlignCenter)
            self.visible_settings[pos] = label
            # Create rotor to increment values with
            button = QPushButton(self)
            button.setGeometry((188+87*idx)*scale, 174*scale, 20*scale, 153*scale)
            button.setFlat(True)
            button.setStyleSheet("border: 0px")
            button.clicked.connect(partial(self.increment_rotor, pos))


        # Create lamps and keyboard
        button_spacing = 22 + 52
        top_row = ['Q','W','E','R','T','Z','U','I','O']
        middle_row = ['A','S','D','F','G','H','J','K']
        bottom_row = ['P','Y','X','C','V','B','N','M','L']      

        row_settings = (
            (top_row, {"x_start":80,"lamp_y":410, "button_y": 659}),
            (middle_row, {"x_start":117,"lamp_y":481, "button_y": 730}),
            (bottom_row, {"x_start":80,"lamp_y":552, "button_y": 799}),
        )

        for row, settings in row_settings:
            for offset, letter in enumerate(row):
                lamp = Lamp(
                    (settings["x_start"]+offset*button_spacing)*scale, 
                    settings["lamp_y"]*scale, letter, scale, self
                )
                button = KeyboardPushButton(
                    (settings["x_start"]+offset*button_spacing)*scale,
                    settings["button_y"]*scale,scale, self
                )
                self.lamps[letter] = lamp
                self.keyboard[letter] = button
                button.pressed.connect(partial(self.key_pressed, letter))
                button.released.connect(partial(self.key_released, letter))

        # for offset, letter in enumerate(top_row):
            

        # for offset, letter in enumerate(middle_row):
        #     lamp = Lamp(
        #         (117+offset*button_spacing)*scale,
        #         481*scale,letter,self.is_scale,self
        #     )
        #     button = KeyboardPushButton(
        #         (117+offset*button_spacing)*scale,
        #         730,self.is_scale, self
        #     )
        #     self.lamps[letter] = lamp
        #     self.keyboard[letter] = button
        #     button.pressed.connect(partial(self.key_pressed, letter))
        #     button.released.connect(partial(self.key_released, letter))

        # for offset, letter in enumerate(bottom_row):
        #     lamp = Lamp(80+offset*button_spacing,552,letter,self)
        #     button = KeyboardPushButton(80+offset*button_spacing,799,self)
        #     self.lamps[letter] = lamp
        #     self.keyboard[letter] = button
        #     button.pressed.connect(partial(self.key_pressed, letter))
        #     button.released.connect(partial(self.key_released, letter))

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

