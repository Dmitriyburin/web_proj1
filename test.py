import sys
import math
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QLayoutItem
from PyQt5.QtGui import QPixmap, QPainter, QColor


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружаем дизайн
        # QVBoxLayout(self).addItem()
        self.add_olymp('спидвагон')
        self.add_olymp('спидвагон')
        self.add_olymp('спидвагон')

    def add_olymp(self, name):
        label = QLabel(self)
        label.setText(name)
        label.setStyleSheet('QLabel::hover {color: blue;}')
        # item = QLayoutItem(label)
        self.verticalLayout.addWidget(label)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
