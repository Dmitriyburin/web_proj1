import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFrame, QScrollArea
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from classes import *


class MyWidget(QMainWindow):
    def __init__(self, olympsAll, program):
        super().__init__()
        uic.loadUi('../ui_files/main.ui', self)
        self.olympiadsAll = olympsAll
        self.program = program
        self.current_olymps = self.olympiadsAll.all_olymp_dict.copy()
        self.searchButton.clicked.connect(self.search)
        self.classEdit.setMaximum(11)

        self.widget = QWidget(self)  # для корректного отображения олимп. на scrollArea
        self.layout = QVBoxLayout(self)  # для корректного отображения олимп. на scrollArea
        self.update_olymp(self.current_olymps)

    def update_olymp(self, olymp_dict: dict):
        for i in reversed(range(self.layout.count())):  # удаление всех элементов layout
            self.layout.itemAt(i).widget().deleteLater()

        for subject, value in olymp_dict.items():  # проходка по всем олимпиадам из словаря
            max_height_frame = len(value) * 30 + 30
            frame = QFrame(self)
            frame.setStyleSheet(f'background-color: #0084ff; border-radius: 25px; '
                                f'max-height: {max_height_frame}; max-width: 400px')
            layout_frame = QVBoxLayout(self)
            subject = QLabel(subject)
            subject = self.styleSheet_olymp(subject, 'subject')

            layout_frame.addWidget(subject)
            for olymp in value:
                layout_frame.addWidget(self.styleSheet_olymp(QLabel(olymp.title), 'olymp'))

            frame.setLayout(layout_frame)
            self.layout.addWidget(frame)
        self.widget.setLayout(self.layout)
        self.scrollArea.setWidget(self.widget)

    def styleSheet_olymp(self, title_label: QLabel, flag):
        if flag == 'olymp':
            title_label.setStyleSheet("""
                    QLabel {
                        color: #fff;
                    }
                    QLabel:hover {
                        color: #ababab;
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

    def search(self):
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




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()

    w.show()
    sys.exit(app.exec_())
