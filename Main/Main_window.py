import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFrame, QScrollArea
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from classes import *


class MyWidget(QMainWindow):
    def __init__(self, olympsAll):
        super().__init__()
        uic.loadUi('../ui_files/main.ui', self)
        self.olympiadsAll = olympsAll
        self.current_olymp = self.olympiadsAll.all_olymp_dict.copy()
        self.searchButton.clicked.connect(self.pas)

        self.widget = QWidget(self)  # для корректного отображения олимп. на scrollArea
        self.layout = QVBoxLayout(self)  # для корректного отображения олимп. на scrollArea
        self.update_olymp(self.current_olymp)

    def update_olymp(self, olymp_dict: dict):
        for i in reversed(range(self.layout.count())):  # удаление всех элементов layout
            self.layout.itemAt(i).widget().deleteLater()

        for subject, value in olymp_dict.items():  # проходка по всем олимпиадам из словаря
            max_height_frame = len(value) * 35 + 35
            frame = QFrame(self)
            frame.setStyleSheet(f'background-color: #0084ff; border-radius: 25px; '
                                f'max-height: {max_height_frame}; max-width: 400px')
            layout_frame = QVBoxLayout(self)
            subject = QLabel(subject)
            subject.setStyleSheet('font-size: 17px; color: #fff; font-weight: bold;')
            layout_frame.addWidget(subject)
            for olymp in value:
                layout_frame.addWidget(self.styleSheet_olymp(QLabel(olymp.title)))

            frame.setLayout(layout_frame)
            self.layout.addWidget(frame)
        self.widget.setLayout(self.layout)
        self.scrollArea.setWidget(self.widget)

    def styleSheet_olymp(self, title_label: QLabel):
        title_label.setStyleSheet("""
                QLabel {
                    color: #fff;
                }
                QLabel:hover {
                    color: #ababab;
                }
                """)
        return title_label

    def add_olymp(self):
        pass

    def pas(self):
        print('hi')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()

    w.show()
    sys.exit(app.exec_())
