import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QCoreApplication, QProcess
from PyQt5.QtGui import QPixmap

from classes import *


class MyWidget(QMainWindow):
    def __init__(self, olympsAll, program, userAll: UsersAll):
        super().__init__()
        uic.loadUi('../ui_files/main.ui', self)
        logo = QPixmap('../images/graduation-cap.png')
        self.setFixedSize(self.size())

        self.logo.setPixmap(logo)  # логотип
        self.logo.setScaledContents(True)
        self.current_user = False
        self.is_admin = False
        self.olympiadsAll = olympsAll
        self.userAll = userAll
        self.program = program
        self.current_olymps = self.olympiadsAll.all_olymp_dict.copy()
        self.searchButton.clicked.connect(self.search)
        self.comboBox.setEnabled(False)
        self.addButton.hide()
        self.classEdit.setMaximum(11)

        self.widget = QWidget(self)  # для корректного отображения олимп. на scrollArea
        self.layout = QVBoxLayout(self)  # для корректного отображения олимп. на scrollArea
        self.update_olymp(self.current_olymps)

    def update_olymp(self, olymp_dict: dict):  # обновление экрана с олимпиадами

        for i in reversed(range(self.layout.count())):  # удаление всех элементов layout
            self.layout.itemAt(i).widget().deleteLater()

        for subject, value in olymp_dict.items():  # проходка по всем олимпиадам из словаря
            max_height_frame = len(value) * 30 + 30
            frame = QFrame(self)
            frame.setStyleSheet(f'background-color: #0084ff; border-radius: 25px; '
                                f'max-height: {max_height_frame}; max-width: 500px')
            layout_frame = QVBoxLayout(self)
            subject = QLabel(subject)
            subject = self.styleSheet_olymp(subject, 'subject')

            layout_frame.addWidget(subject)
            for olymp in value:
                layout_frame.addWidget(self.styleSheet_olymp(QLabel(olymp.title), 'olymp'))

            frame.setLayout(layout_frame)
            self.layout.addWidget(frame)
        if not len(olymp_dict):
            self.layout.addWidget(QLabel('Ни одной олимпиады не нашлось('))
        self.layout.setContentsMargins(10, 10, 0, 400 - ((len(olymp_dict.values())
                                                          + len(olymp_dict.keys())) * 30))
        print(400 - ((len(olymp_dict.values()) + len(olymp_dict.keys())) * 30))
        print('смениласб')
        self.widget.setLayout(self.layout)
        self.scrollArea.setWidget(self.widget)

    def styleSheet_olymp(self, title_label: QLabel, flag):  # смена стиля для QLabel
        if flag == 'olymp':
            title_label.setStyleSheet("""
                    QLabel {
                        color: #fff;
                    }
                    QLabel:hover {
                        color: #ababab;
                    }
                    QToolTip { 
                        color: #ffffff; 
                        background-color: #2a82da; 
                        border: 1px solid white; 
                        border-radius: 0;
                    }
                    """)
            return title_label
        if flag == 'subject':
            title_label.setStyleSheet("""
                    QLabel {
                        font-size: 17px; 
                        color: #fff; 
                        font-weight: bold;
                    }
                    QLabel:hover {
                        color: #c1c1c1;
                    }
                    """)
            return title_label

    def search(self):  # фильтрация олимпиад
        title = self.titleEdit.text() if len(self.titleEdit.text()) != 0 else False
        sub = self.subjectEdit.text() if len(self.subjectEdit.text()) != 0 else False
        clas = self.classEdit.text() if int(self.classEdit.text()) != 0 else False
        self.current_olymps = {}
        flag = True
        if title and flag:
            for subject, olimpiads in self.olympiadsAll.all_olymp_dict.items():
                for olimpiad in olimpiads:
                    if olimpiad.title == title:
                        if subject in self.current_olymps:
                            self.current_olymps[subject].append(olimpiad)
                        else:
                            self.current_olymps[subject] = [olimpiad]
            if len(self.current_olymps) == 0:
                flag = False
        if sub and flag:
            if len(self.current_olymps) == 0:
                self.current_olymps = self.olympiadsAll.all_olymp_dict.copy()
            if sub in self.current_olymps:
                self.current_olymps = {sub: self.current_olymps[sub]}
            else:
                self.current_olymps = {}
            if len(self.current_olymps) == 0:
                flag = False
        if clas and flag:
            if len(self.current_olymps) == 0:
                olymps = self.olympiadsAll.all_olymp_dict.copy()
            else:
                olymps = self.current_olymps.copy()
            self.current_olymps = {}
            for subject, olimpiads in olymps.items():
                for olimpiad in olimpiads:
                    if str(olimpiad.sch_class) == clas:
                        if subject in self.current_olymps:
                            self.current_olymps[subject].append(olimpiad)
                        else:
                            self.current_olymps[subject] = [olimpiad]

        print(self.current_olymps, self.olympiadsAll.all_olymp_dict, 'в серче')
        if not title and not sub and not clas:
            self.current_olymps = self.olympiadsAll.all_olymp_dict.copy()
            self.update_olymp(self.olympiadsAll.all_olymp_dict.copy())
        else:
            self.update_olymp(self.current_olymps)
        self.program.clicked_for_olymp()
        # if s

    def settings_login(self, user_name: UserRegistered,
                       usersAll: UsersAll):  # настройка интерфейса после входа в аккаунт
        self.current_user = usersAll.user_all[user_name.name][0]
        self.is_login = True
        if self.current_user.name == 'admin':
            self.addButton.show()
            self.is_admin = True
        else:
            self.addButton.hide()
        self.comboBox.setEnabled(True)
        self.confirmSettingsButton.clicked.connect(self.menu_login)
        self.loginButton.disconnect()
        self.loginButton.setText(user_name.name)
        # self.loginButton.clicked.connect(self.menu_login)

    def menu_login(self):  # настройка основного меню comboBox
        command = self.comboBox.currentText()
        if command == 'Выйти из аккаунта':
            self.restart()
        elif command == 'Удалить аккаунт':
            message = QMessageBox.warning(self, 'Осторожно', 'Вы уверены, '
                                                             'что хотите удалить аккаунт?',
                                          QMessageBox.Yes | QMessageBox.No)
            if message == QMessageBox.Yes:
                self.delete_user()
                self.close()
        elif command == 'Избранные олимпиады':
            self.program.show_favorites_olymps_window()

    def restart(self):  # перезагрузка(на данный момент: выход из программы)
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)
        print(status)

    def delete_user(self):  # удаление пользователя
        self.userAll.delete_user(self.current_user)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

