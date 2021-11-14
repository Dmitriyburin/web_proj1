import webbrowser

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt, QDate

from classes import *


class MyOlymp(QMainWindow):
    def __init__(self, olymp, olympsAll: OlympiadsAll, main_w, program, subject,
                 is_admin, usersAll: UsersAll):
        super().__init__()
        uic.loadUi('../ui_files/view_olymp.ui', self)

        self.olympiad = olymp
        self.olympsAll = olympsAll
        self.usersAll = usersAll
        self.main_w = main_w
        self.program = program
        self.subject = subject
        self.is_admin = is_admin
        if self.main_w.current_user:
            self.is_favorite = True if self.olympiad in\
                                       self.main_w.current_user.favorites_olymps else False
        else:
            self.is_favorite = False
        self.updateDisplay()
        self.deleteButton.clicked.connect(self.delete_olymp)
        self.changeButton.clicked.connect(self.change_olymp)
        self.favoritesButton.clicked.connect(self.add_favorite)
        self.linkButton.clicked.connect(self.open_link)

        self.deleteButton.show()
        self.changeButton.show()
        self.favoritesButton.show()
        if not self.is_admin:
            self.deleteButton.hide()
            self.changeButton.hide()
            self.setGeometry(100, 60, 457, 328)
            if not self.main_w.current_user:
                self.favoritesButton.hide()
        elif self.is_admin:
            self.setGeometry(100, 60, 457, 406)
        self.setFixedSize(self.size())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def updateDisplay(self):
        self.label_title.setText(self.olympiad.title)
        self.label_class.setText(f'{self.olympiad.sch_class} класс')
        self.label_description.setText(self.olympiad.des)
        self.label_duration.setText(f'{self.olympiad.dur} минут')
        self.label_date.setText(self.olympiad.date.strftime('%d %B %Y'))
        if self.is_favorite:
            self.favoritesButton.setText('Удалить из избранных')
            self.favoritesButton.setStyleSheet(
                'QPushButton {background-color: rgb(255, 247, 0);border-radius: 7px;color: '
                'rgb(0, 132, 255);border: 1px solid rgb(0, 132, 255);}'
                'QPushButton:hover {background-color: rgb(255, 243, 175);}')
        else:
            self.favoritesButton.setStyleSheet(
                'QPushButton {background-color: #fff;border-radius: 7px;color: '
                'rgb(0, 132, 255);border: 1px solid rgb(0, 132, 255);}'
                'QPushButton:hover {background-color: rgb(255, 243, 175);}')

    def delete_olymp(self):
        self.olympsAll.delete_olymp(self.olympiad)
        self.main_w.current_olymps = self.olympsAll.all_olymp_dict.copy()
        self.main_w.update_olymp(self.olympsAll.all_olymp_dict)  # обновление главного меню
        self.program.clicked_for_olymp()  # привязка clicked на олимпиады
        self.close()

    def change_olymp(self):
        self.main_w.current_olymps = self.olympsAll.all_olymp_dict.copy()
        self.change_olymp_w = ChangeOlymp(self.olympiad, self.olympsAll,
                                          self.main_w, self.program, self.subject)
        self.change_olymp_w.setWindowModality(Qt.ApplicationModal)
        self.change_olymp_w.show()
        self.close()

    def add_favorite(self):
        self.is_favorite = True if self.olympiad in self.main_w.current_user.favorites_olymps else False

        msg = QMessageBox(self)
        msg.setWindowTitle("Message Box")
        msg.setIcon(QMessageBox.Question)
        if not self.is_favorite:
            self.main_w.current_user.favorites_olymps.append(self.olympiad)
            self.is_favorite = True
            self.usersAll.add_favorite_olymp(self.usersAll.getConnection('main'),
                                             self.main_w.current_user,
                                             self.olympiad)
            msg.setText("Олимпиада добавлена в избранные")
        else:
            self.main_w.current_user.favorites_olymps.pop(
                self.main_w.current_user.favorites_olymps.index(self.olympiad))
            self.is_favorite = False
            self.usersAll.delete_favorite_olymp(self.usersAll.getConnection('main'),
                                                self.main_w.current_user,
                                                self.olympiad)
            msg.setText("Олимпиада удалена из избранных")
        msg.show()
        self.main_w.current_user.update_favorites_olymp()
        print(self.main_w.current_user.favorites_olymps_dict)
        self.close()

    def open_link(self):  # открытие ссылки в веббраузере
        webbrowser.get(using='windows-default').open_new_tab(self.olympiad.link)


class ChangeOlymp(QMainWindow):
    def __init__(self, olympiad: Olympiad, olympsAll: OlympiadsAll, main_w,
                 program, subject):
        super().__init__()
        uic.loadUi('../ui_files/new_olymp.ui', self)
        self.setFixedSize(self.size())

        self.saveButton.clicked.connect(self.change)
        self.olympiadsAll = olympsAll
        self.main_w = main_w
        self.program = program
        self.subject = subject

        self.olympiad = olympiad
        self.titleEdit.setText(self.olympiad.title)
        self.classEdit.setValue(int(self.olympiad.sch_class))
        self.dateEdit.setDate(self.olympiad.date)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QDate.currentDate())
        self.classEdit.setMinimum(1)
        self.classEdit.setMaximum(11)

        self.linkEdit.setText(self.olympiad.link)
        self.descrPlainEdit.setPlainText(self.olympiad.des)
        self.durPlainEdit.setPlainText(str(self.olympiad.dur))

    def change(self):
        flag = True
        for field in [self.titleEdit, self.linkEdit]:
            if len(field.text()) == 0:
                flag = False
                self.empty_field_style(field, False)
            else:
                self.empty_field_style(field, True)

        for field in [self.descrPlainEdit, self.durPlainEdit]:
            if len(field.toPlainText()) == 0:
                flag = False
                self.empty_field_style(field, False)
            else:
                self.empty_field_style(field, True)
        if flag:
            self.olympiadsAll.delete_olymp(self.olympiad)
            date = self.dateEdit.dateTime().toString('yyyy-M-d').split('-')
            year, month, day = int(date[0]), int(date[1]), int(date[2])
            date = datetime.date(year, month, day)
            print(self.subject)
            olymp = Olympiad(0, self.subject, self.titleEdit.text(),
                             int(self.classEdit.text()),
                             self.descrPlainEdit.toPlainText(),
                             int(self.durPlainEdit.toPlainText()),
                             self.linkEdit.text(), date)
            self.olympiadsAll.add_olymp(olymp)
            self.main_w.current_olymps = self.olympiadsAll.all_olymp_dict.copy()
            self.main_w.update_olymp(self.olympiadsAll.all_olymp_dict)  # обновление главного меню
            self.program.clicked_for_olymp()  # привязка clicked на олимпиады
            self.close()

    def empty_field_style(self, textEdit: QTextEdit, is_empty: bool):
        if not is_empty:
            textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid red; '
                                   f'border-radius: 10px;')
            return
        textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid rgb(0, 132, 255); '
                               f'border-radius: 10px;')
