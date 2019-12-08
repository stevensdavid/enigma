import argparse
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPalette
from enigma import EnigmaMachine
from enigma_window import EnigmaWindow
from enigma_config_window import EnigmaConfigWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', type=float, default=1, 
                        help="GUI scaling factor as a float")
    args = parser.parse_args()
    ex = EnigmaWindow(args.scale)
    sys.exit(app.exec_())
