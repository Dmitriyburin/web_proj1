from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from classes import *



class Login(QMainWindow):
    def __init__(self, usersAll, main_w):
        super().__init__()
        self.usersAll = usersAll
        self.main_w = main_w
        uic.loadUi('../ui_files/login.ui', self)
        self.setFixedSize(self.size())

        self.registrationButton.clicked.connect(self.show_registration_w)
        self.loginButton.clicked.connect(self.login)
        self.passwordEdit.setEchoMode(QLineEdit.Password)

    def login(self):
        user_name = self.loginEdit.text()
        password = self.passwordEdit.text()
        if user_name in self.usersAll.user_all:
            if password == self.usersAll.user_all[user_name][0].password:
                self.main_w.settings_login(self.usersAll.user_all[user_name][0],
                                           self.usersAll)
                self.close()
            else:
                QMessageBox.critical(self, 'Error', 'Пароль неверный.',
                                     buttons=QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Error', f'Такого пользователя не существует.',
                                 buttons=QMessageBox.Ok)
        for field in [self.loginEdit, self.passwordEdit]:
            if len(field.text()) == 0:
                flag = False
                empty_field_style(field, False)
            else:
                empty_field_style(field, True)

    def show_registration_w(self):
        self.registration_w = Registration(self.usersAll, self.main_w)
        self.registration_w.setWindowModality(Qt.ApplicationModal)
        self.registration_w.show()
        self.close()


class Registration(QMainWindow):
    def __init__(self, usersAll, main_w):
        super().__init__()
        self.usersAll = usersAll
        self.main_w = main_w
        uic.loadUi('../ui_files/registration.ui', self)
        self.classEdit.setMinimum(1)
        self.classEdit.setMaximum(11)
        self.registrationButton.clicked.connect(self.registration)
        self.passwordEdit.setEchoMode(QLineEdit.Password)

    def registration(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()
        class_count = self.classEdit.text()
        flag = True
        for field in [self.loginEdit, self.passwordEdit]:
            if len(field.text()) == 0:
                flag = False
                empty_field_style(field, False)
            else:
                empty_field_style(field, True)
        if login in self.usersAll.user_all:
            flag = False
            QMessageBox.question(self, 'Error', 'Такой login уже существует',
                                 buttons=QMessageBox.Ok)
        if flag:
            self.usersAll.add_user(UserRegistered(0, login, password, class_count))
            self.main_w.settings_login(self.usersAll.user_all[login][0], self.usersAll)
            self.close()


def empty_field_style(textEdit: QTextEdit, is_empty: bool):
    if not is_empty:
        textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid red; '
                               f'border-radius: 10px;')
        return
    textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid rgb(0, 132, 255); '
                           f'border-radius: 10px;')
