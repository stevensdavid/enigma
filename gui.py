from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from enigma import EnigmaMachine

Form, Window = uic.loadUiType('enigma.ui')

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()
