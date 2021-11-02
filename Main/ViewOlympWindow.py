import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFrame, QScrollArea
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from classes import *


class MyOlymp(QMainWindow):
    def __init__(self, olymp, olympsAll: OlympiadsAll, main_w, program):
        super().__init__()
        uic.loadUi('../ui_files/view_olymp.ui', self)
        self.olympiad = olymp
        self.olympsAll = olympsAll
        self.main_w = main_w
        self.program = program

        self.updateDisplay()
        self.deleteButton.clicked.connect(self.delete_olymp)

    def updateDisplay(self):
        self.label_title.setText(self.olympiad.title)

        self.label_class.setText(f'{self.olympiad.sch_class} класс')
        self.label_description.setText(self.olympiad.des)
        self.label_duration.setText(f'{self.olympiad.dur} минут')
        self.label_date.setText(self.olympiad.date.strftime('%d %B %Y'))

    def delete_olymp(self):
        self.olympsAll.delete_olymp(self.olympiad)
        self.main_w.update_olymp(self.olympsAll.all_olymp_dict)  # обновление главного меню
        self.program.clicked_for_olymp()  # привязка clicked на олимпиады
        self.close()
