from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPalette
from enigma import EnigmaMachine
from enigma_window import EnigmaWindow
from enigma_config_window import EnigmaConfigWindow
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Set to barbarossa settings
    plugboard_map = { 
        'A': 'V', 'B': 'S', 'C': 'G', 'D': 'L', 'F': 'U', 'H': 'Z', 
        'I': 'N', 'K': 'M', 'O': 'W', 'R': 'X' 
    }
    rotors = [2,4,5]
    ringstellung = [2,21,12]
    
    ex = EnigmaWindow(pb_map=plugboard_map, reflector='B', 
        rotors=rotors, ringstellung=ringstellung)
    while ex.enigma.rotor_position('right') != 'A':
        ex.enigma.increment_rotor('right')

    while ex.enigma.rotor_position('middle') != 'L':
        ex.enigma.increment_rotor('middle')

    while ex.enigma.rotor_position('left') != 'B':
        ex.enigma.increment_rotor('left')
    sys.exit(app.exec_())
