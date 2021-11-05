import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt, QObject, QDate

from classes import *
from CreateOlympWindow import CreateOlymp


class MyOlymp(QMainWindow):
    def __init__(self, olymp, olympsAll: OlympiadsAll, main_w, program, subject):
        super().__init__()
        uic.loadUi('../ui_files/view_olymp.ui', self)
        self.olympiad = olymp
        self.olympsAll = olympsAll
        self.main_w = main_w
        self.program = program
        self.subject = subject
        self.updateDisplay()
        self.deleteButton.clicked.connect(self.delete_olymp)
        self.changeButton.clicked.connect(self.change_olymp)
        self.changeButton.clicked.connect(self.change_olymp)

    def updateDisplay(self):
        self.label_title.setText(self.olympiad.title)
        self.label_class.setText(f'{self.olympiad.sch_class} класс')
        self.label_description.setText(self.olympiad.des)
        self.label_duration.setText(f'{self.olympiad.dur} минут')
        self.label_date.setText(self.olympiad.date.strftime('%d %B %Y'))

    def delete_olymp(self):
        self.olympsAll.delete_olymp(self.olympiad)
        self.main_w.current_olymps = self.olympsAll.all_olymp_dict.copy()
        self.main_w.update_olymp(self.olympsAll.all_olymp_dict)  # обновление главного меню
        self.program.clicked_for_olymp()  # привязка clicked на олимпиады
        self.close()

    def change_olymp(self):
        self.main_w.current_olymps = self.olympsAll.all_olymp_dict.copy()
        self.change_olymp_w = ChangeOlymp(self.olympiad, self.olympsAll, self.main_w, self.program, self.subject)
        self.change_olymp_w.setWindowModality(Qt.ApplicationModal)
        self.change_olymp_w.show()
        self.close()


class ChangeOlymp(QMainWindow):
    def __init__(self, olympiad: Olympiad, olympsAll: OlympiadsAll, main_w, program, subject):
        super().__init__()
        uic.loadUi('../ui_files/new_olymp.ui', self)
        self.saveButton.clicked.connect(self.change)
        self.olympiadsAll = olympsAll
        self.main_w = main_w
        self.program = program
        self.subject = subject

        self.olympiad = olympiad
        self.titleEdit.setText(self.olympiad.title)
        self.classEdit.setValue(int(self.olympiad.sch_class))
        self.dateEdit.setDate(self.olympiad.date)
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
            olymp = Olympiad(0, self.subject, self.titleEdit.text(), int(self.classEdit.text()),
                             self.descrPlainEdit.toPlainText(), int(self.durPlainEdit.toPlainText()),
                             self.linkEdit.text(), date)
            self.olympiadsAll.add_olymp(olymp)
            self.main_w.current_olymps = self.olympiadsAll.all_olymp_dict.copy()
            self.main_w.update_olymp(self.olympiadsAll.all_olymp_dict)  # обновление главного меню
            self.program.clicked_for_olymp()  # привязка clicked на олимпиады
            self.close()

    def empty_field_style(self, textEdit: QTextEdit, is_empty: bool):
        if not is_empty:
            textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid red; border-radius: 10px;')
            return
        textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid rgb(0, 132, 255); border-radius: 10px;')
