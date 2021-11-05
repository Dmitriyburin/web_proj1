from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit
from PyQt5.QtCore import Qt
from classes import *


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../ui_files/login.ui', self)
        self.registrationButton.clicked.connect(self.show_registration_w)

    def show_registration_w(self):
        self.registration_w = Registration()
        self.registration_w.setWindowModality(Qt.ApplicationModal)
        self.registration_w.show()
        self.close()


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('../ui_files/registration.ui', self)
        self.classEdit.setMinimum(1)
        self.classEdit.setMaximum(11)