import sys
import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon

from Main_window import MyWidget
from ViewOlympWindow import MyOlymp
from CreateOlympWindow import CreateOlymp, CreateOlympWithSubject
from FavoritesOlymps import FavoritesOlymps
from LoginWindow import Login

from classes import OlympiadsAll, Olympiad, UsersAll


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('MainWindow')
        self.olympiadsAll = OlympiadsAll()
        self.usersAll = UsersAll(self.olympiadsAll)
        self.is_admin = False
        self.program = self
        self.show_main_window()

    def show_main_window(self):  # открытие и настройка основного окна
        self.main_w = MyWidget(self.olympiadsAll, self, self.usersAll)
        self.main_w.setWindowTitle('   Все олимпиады')
        self.main_w.show()
        self.main_w.addButton.clicked.connect(self.show_create_olymp_window_with_subj)
        self.main_w.loginButton.clicked.connect(self.show_login_window)
        self.clicked_for_olymp()

    def clicked_for_olymp(self):  # обработка олимпиад на основном меню
        self.olymp_label_class = {}  # словарь ключ: QLabel олимпиады, значение: объект Olympiads
        self.current_olymps = None
        self.current_olymp = None
        self.flag_subject = False
        for frame in self.main_w.scrollArea.findChildren(QFrame):  # привязка события на все олимпиады (QLabel)
            if type(frame) == QFrame:
                for count, olymp in enumerate(frame.findChildren(QLabel)):
                    if count == 0:
                        self.flag_subject = True
                        self.current_olymps = self.main_w.current_olymps[olymp.text()]

                    else:
                        self.current_olymp = self.current_olymps[count - 1]
                        self.olymp_label_class[olymp] = self.current_olymp
                        olymp.setToolTip(f'Класс: {self.current_olymp.sch_class}\n'
                                         f'Название: {self.current_olymp.title}\n'
                                         f'Предмет: {self.current_olymp.subject}\n'
                                         f'Продолжительность: {self.current_olymp.dur} минут')
                    olymp.installEventFilter(self)

    def eventFilter(self, obj, e):  # для подлкючения события clicked на QLabel
        if e.type() == 2:
            if obj in self.olymp_label_class:
                self.show_olymp_window(self.olymp_label_class[obj])
            else:
                if self.main_w.is_admin:
                    self.show_create_olymp_window(obj.text())
        return super(QMainWindow, self).eventFilter(obj, e)

    def show_olymp_window(self, olympiad: Olympiad):  # открытие и настройка окна олимпиады
        subject = olympiad.subject
        self.olymp_view_w = MyOlymp(olympiad, self.olympiadsAll,
                                    self.main_w, self, subject, self.main_w.is_admin,
                                    self.usersAll)
        self.olymp_view_w.setWindowModality(Qt.ApplicationModal)
        self.olymp_view_w.setWindowTitle('Олимпиада')
        self.olymp_view_w.show()
        self.passed_olymp(olympiad, self.olymp_view_w)
        self.olympiadsAll.update_all_olymp_dict()

    def show_create_olymp_window(self, subject):  # открытие и настройка окна создания олимпиады
        self.create_olymp_w = CreateOlymp(subject, self.olympiadsAll,
                                          self.main_w, self)
        self.create_olymp_w.setWindowModality(Qt.ApplicationModal)
        self.create_olymp_w.setWindowTitle('Создание олимпиады')
        self.create_olymp_w.show()

    def show_create_olymp_window_with_subj(self, subject):  # открытие и настройка окна создания олимпиады
        self.create_olymp_w = CreateOlympWithSubject(subject, self.olympiadsAll,
                                                     self.main_w, self)
        self.create_olymp_w.setWindowModality(Qt.ApplicationModal)
        self.create_olymp_w.setWindowTitle('Создание олимпиады')

        self.create_olymp_w.show()

    def show_login_window(self):  # открытие и настройка окна входа и регистрации
        self.login_w = Login(self.usersAll, self.main_w)
        self.login_w.setWindowModality(Qt.ApplicationModal)
        self.login_w.setWindowTitle('Вход')

        self.login_w.show()

    def show_favorites_olymps_window(self):  # открытие и настройка окна избранных олимпиад
        self.fav_olymps_w = FavoritesOlymps(self.usersAll, self.main_w,
                                            self.main_w.current_user, self.program)
        self.fav_olymps_w.setWindowModality(Qt.ApplicationModal)
        self.fav_olymps_w.setWindowTitle('Любимые олимпиады')
        self.fav_olymps_w.show()

    def passed_olymp(self, olympiad, win):  # настройка для прошедших олимпиад
        if datetime.date.today() > olympiad.date:
            win.label_passed.setText('Олимпиада завершена')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../Images/icon.png'))
    print("[PID]:", QCoreApplication.applicationPid())

    window = MainWindow()

    sys.exit(app.exec_())
