from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QMessageBox
from PyQt5.QtCore import QDate

from classes import *


class CreateOlymp(QMainWindow):
    def __init__(self, subject: str, olympsAll: OlympiadsAll, main_w, program):
        super().__init__()
        self.ui()
        self.subject = subject
        self.olympsAll = olympsAll
        self.main_w = main_w
        self.program = program
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setMinimumDate(QDate.currentDate())
        self.classEdit.setMinimum(1)
        self.classEdit.setMaximum(11)

    def ui(self):
        uic.loadUi('../ui_files/new_olymp.ui', self)
        self.saveButton.clicked.connect(self.save)
        self.setFixedSize(self.size())

    def save(self):
        date = self.dateEdit.dateTime().toString('yyyy-M-d').split('-')
        year, month, day = int(date[0]), int(date[1]), int(date[2])
        date = datetime.date(year, month, day)
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
        try:
            if flag:
                olymp = Olympiad(0, self.subject, self.titleEdit.text(),
                                 int(self.classEdit.text()),
                                 self.descrPlainEdit.toPlainText(),
                                 int(self.durPlainEdit.toPlainText()),
                                 self.linkEdit.text(), date)
                self.olympsAll.add_olymp(olymp)
                self.main_w.current_olymps = self.olympsAll.all_olymp_dict.copy()
                self.main_w.update_olymp(self.olympsAll.all_olymp_dict)  # обновление главного меню
                self.program.clicked_for_olymp()  # привязка clicked на олимпиады
                self.close()
        except Exception:
            QMessageBox.critical(self, 'Error', 'Введенные данные некорректны',
                                 buttons=QMessageBox.Ok)

    def empty_field_style(self, textEdit: QTextEdit, is_empty: bool):  # ccs стили для некорректных полей
        if not is_empty:
            textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid red; '
                                   f'border-radius: 10px;')
            return
        textEdit.setStyleSheet(f'{textEdit.styleSheet()} border: 1px solid rgb(0, 132, 255); '
                               f'border-radius: 10px;')


class CreateOlympWithSubject(CreateOlymp):
    def __init__(self, subject, olympsAll: OlympiadsAll, main_w, program):
        super().__init__(subject, olympsAll, main_w, program)

    def ui(self):
        uic.loadUi('../ui_files/new_olymp_with_subject.ui', self)
        self.saveButton.clicked.connect(self.click)
        self.setFixedSize(self.size())

    def click(self):
        self.subject = self.subjectEdit.text()
        self.save()
