from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EnigmaSettings(object):
    def setupUi(self, EnigmaSettings):
        EnigmaSettings.setObjectName("EnigmaSettings")
        EnigmaSettings.resize(249, 190)
        self.gridLayout = QtWidgets.QGridLayout(EnigmaSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.main_vlayout = QtWidgets.QVBoxLayout()
        self.main_vlayout.setObjectName("main_vlayout")
        self.rotors_vlayout = QtWidgets.QVBoxLayout()
        self.rotors_vlayout.setObjectName("rotors_vlayout")
        self.rotor_choice_hlayout = QtWidgets.QHBoxLayout()
        self.rotor_choice_hlayout.setObjectName("rotor_choice_hlayout")
        self.left_rotor_choice_vlayout = QtWidgets.QVBoxLayout()
        self.left_rotor_choice_vlayout.setObjectName("left_rotor_choice_vlayout")
        self.left_rotor_label = QtWidgets.QLabel(EnigmaSettings)
        self.left_rotor_label.setObjectName("left_rotor_label")
        self.left_rotor_choice_vlayout.addWidget(self.left_rotor_label)
        self.left_rotor_combo = QtWidgets.QComboBox(EnigmaSettings)
        self.left_rotor_combo.setObjectName("left_rotor_combo")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_combo.addItem("")
        self.left_rotor_choice_vlayout.addWidget(self.left_rotor_combo)
        self.rotor_choice_hlayout.addLayout(self.left_rotor_choice_vlayout)
        self.middle_rotor_choice_vlayout = QtWidgets.QVBoxLayout()
        self.middle_rotor_choice_vlayout.setObjectName("middle_rotor_choice_vlayout")
        self.middle_rotor_label = QtWidgets.QLabel(EnigmaSettings)
        self.middle_rotor_label.setObjectName("middle_rotor_label")
        self.middle_rotor_choice_vlayout.addWidget(self.middle_rotor_label)
        self.middle_rotor_combo = QtWidgets.QComboBox(EnigmaSettings)
        self.middle_rotor_combo.setObjectName("middle_rotor_combo")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_combo.addItem("")
        self.middle_rotor_choice_vlayout.addWidget(self.middle_rotor_combo)
        self.rotor_choice_hlayout.addLayout(self.middle_rotor_choice_vlayout)
        self.right_rotor_choice_vlayout = QtWidgets.QVBoxLayout()
        self.right_rotor_choice_vlayout.setObjectName("right_rotor_choice_vlayout")
        self.right_rotor_label = QtWidgets.QLabel(EnigmaSettings)
        self.right_rotor_label.setObjectName("right_rotor_label")
        self.right_rotor_choice_vlayout.addWidget(self.right_rotor_label)
        self.right_rotor_combo = QtWidgets.QComboBox(EnigmaSettings)
        self.right_rotor_combo.setObjectName("right_rotor_combo")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_combo.addItem("")
        self.right_rotor_choice_vlayout.addWidget(self.right_rotor_combo)
        self.rotor_choice_hlayout.addLayout(self.right_rotor_choice_vlayout)
        self.rotors_vlayout.addLayout(self.rotor_choice_hlayout)
        self.ring_position_label = QtWidgets.QLabel(EnigmaSettings)
        self.ring_position_label.setObjectName("ring_position_label")
        self.rotors_vlayout.addWidget(self.ring_position_label)
        self.ring_position_hlayout = QtWidgets.QHBoxLayout()
        self.ring_position_hlayout.setObjectName("ring_position_hlayout")
        self.left_position_spinbox = QtWidgets.QSpinBox(EnigmaSettings)
        self.left_position_spinbox.setMinimum(1)
        self.left_position_spinbox.setMaximum(26)
        self.left_position_spinbox.setObjectName("left_position_spinbox")
        self.ring_position_hlayout.addWidget(self.left_position_spinbox)
        self.middle_position_spinbox = QtWidgets.QSpinBox(EnigmaSettings)
        self.middle_position_spinbox.setMinimum(1)
        self.middle_position_spinbox.setMaximum(26)
        self.middle_position_spinbox.setObjectName("middle_position_spinbox")
        self.ring_position_hlayout.addWidget(self.middle_position_spinbox)
        self.right_position_spinbox = QtWidgets.QSpinBox(EnigmaSettings)
        self.right_position_spinbox.setMinimum(1)
        self.right_position_spinbox.setMaximum(26)
        self.right_position_spinbox.setObjectName("right_position_spinbox")
        self.ring_position_hlayout.addWidget(self.right_position_spinbox)
        self.rotors_vlayout.addLayout(self.ring_position_hlayout)
        self.main_vlayout.addLayout(self.rotors_vlayout)
        self.refl_pb_hlayout = QtWidgets.QHBoxLayout()
        self.refl_pb_hlayout.setObjectName("refl_pb_hlayout")
        self.refl_vlayout = QtWidgets.QVBoxLayout()
        self.refl_vlayout.setObjectName("refl_vlayout")
        self.refl_label = QtWidgets.QLabel(EnigmaSettings)
        self.refl_label.setObjectName("refl_label")
        self.refl_vlayout.addWidget(self.refl_label)
        self.refl_combo = QtWidgets.QComboBox(EnigmaSettings)
        self.refl_combo.setObjectName("refl_combo")
        self.refl_combo.addItem("")
        self.refl_combo.addItem("")
        self.refl_vlayout.addWidget(self.refl_combo)
        self.refl_pb_hlayout.addLayout(self.refl_vlayout)
        self.pb_vlayout = QtWidgets.QVBoxLayout()
        self.pb_vlayout.setObjectName("pb_vlayout")
        self.pb_label = QtWidgets.QLabel(EnigmaSettings)
        self.pb_label.setObjectName("pb_label")
        self.pb_vlayout.addWidget(self.pb_label)
        self.pb_input = QtWidgets.QLineEdit(EnigmaSettings)
        self.pb_input.setObjectName("pb_input")
        self.pb_vlayout.addWidget(self.pb_input)
        self.refl_pb_hlayout.addLayout(self.pb_vlayout)
        self.main_vlayout.addLayout(self.refl_pb_hlayout)
        self.gridLayout.addLayout(self.main_vlayout, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(EnigmaSettings)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 1, 0, 1, 1)

        self.retranslateUi(EnigmaSettings)
        self.button_box.accepted.connect(EnigmaSettings.accept)
        self.button_box.rejected.connect(EnigmaSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(EnigmaSettings)

    def retranslateUi(self, EnigmaSettings):
        _translate = QtCore.QCoreApplication.translate
        EnigmaSettings.setWindowTitle(_translate("EnigmaSettings", "Enigma Settings"))
        self.left_rotor_label.setText(_translate("EnigmaSettings", "Left rotor"))
        self.left_rotor_combo.setItemText(0, _translate("EnigmaSettings", "1"))
        self.left_rotor_combo.setItemText(1, _translate("EnigmaSettings", "2"))
        self.left_rotor_combo.setItemText(2, _translate("EnigmaSettings", "3"))
        self.left_rotor_combo.setItemText(3, _translate("EnigmaSettings", "4"))
        self.left_rotor_combo.setItemText(4, _translate("EnigmaSettings", "5"))
        self.left_rotor_combo.setItemText(5, _translate("EnigmaSettings", "6"))
        self.left_rotor_combo.setItemText(6, _translate("EnigmaSettings", "7"))
        self.left_rotor_combo.setItemText(7, _translate("EnigmaSettings", "8"))
        self.middle_rotor_label.setText(_translate("EnigmaSettings", "Middle rotor"))
        self.middle_rotor_combo.setItemText(0, _translate("EnigmaSettings", "1"))
        self.middle_rotor_combo.setItemText(1, _translate("EnigmaSettings", "2"))
        self.middle_rotor_combo.setItemText(2, _translate("EnigmaSettings", "3"))
        self.middle_rotor_combo.setItemText(3, _translate("EnigmaSettings", "4"))
        self.middle_rotor_combo.setItemText(4, _translate("EnigmaSettings", "5"))
        self.middle_rotor_combo.setItemText(5, _translate("EnigmaSettings", "6"))
        self.middle_rotor_combo.setItemText(6, _translate("EnigmaSettings", "7"))
        self.middle_rotor_combo.setItemText(7, _translate("EnigmaSettings", "8"))
        self.right_rotor_label.setText(_translate("EnigmaSettings", "Right rotor"))
        self.right_rotor_combo.setItemText(0, _translate("EnigmaSettings", "1"))
        self.right_rotor_combo.setItemText(1, _translate("EnigmaSettings", "2"))
        self.right_rotor_combo.setItemText(2, _translate("EnigmaSettings", "3"))
        self.right_rotor_combo.setItemText(3, _translate("EnigmaSettings", "4"))
        self.right_rotor_combo.setItemText(4, _translate("EnigmaSettings", "5"))
        self.right_rotor_combo.setItemText(5, _translate("EnigmaSettings", "6"))
        self.right_rotor_combo.setItemText(6, _translate("EnigmaSettings", "7"))
        self.right_rotor_combo.setItemText(7, _translate("EnigmaSettings", "8"))
        self.ring_position_label.setText(_translate("EnigmaSettings", "Ring positions"))
        self.refl_label.setText(_translate("EnigmaSettings", "Reflector"))
        self.refl_combo.setItemText(0, _translate("EnigmaSettings", "B"))
        self.refl_combo.setItemText(1, _translate("EnigmaSettings", "C"))
        self.pb_label.setText(_translate("EnigmaSettings", "Plugboard"))


class EnigmaConfigWindow(Ui_EnigmaSettings, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EnigmaConfigWindow, self).__init__(parent)
        self.setupUi(self)

    def enigma_settings(self):
        kwargs = {}
        kwargs["rotors"] = [int(x) for x in 
            (self.left_rotor_combo.currentText(), 
            self.middle_rotor_combo.currentText(), 
            self.right_rotor_combo.currentText())
        ]
        kwargs["ringstellung"] = [
            self.left_position_spinbox.value(),
            self.middle_position_spinbox.value(),
            self.right_position_spinbox.value()
        ]
        kwargs['pb_map'] = {
            x[0]:x[1] 
            for x in self.pb_input.text().split(' ') 
            if self.pb_input.text()
        }
        kwargs["reflector"] = self.refl_combo.currentText()
        return kwargs
