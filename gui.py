from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPalette
from enigma import EnigmaMachine
from enigma_window import EnigmaWindow
from enigma_config_window import EnigmaConfigWindow
import sys

def letter_pressed(letter: str):
    pass


def letter_released(letter: str):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EnigmaWindow()
    sys.exit(app.exec_())
