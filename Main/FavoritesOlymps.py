from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from classes import *


class FavoritesOlymps(QMainWindow):
    def __init__(self, usersAll, main_w, current_user: UserRegistered):
        super().__init__()
        self.usersAll = usersAll
        self.main_w = main_w
        self.current_user = current_user
        uic.loadUi('../ui_files/favorites_olymp.ui', self)
        self.widget = QWidget(self)  # для корректного отображения олимп. на scrollArea
        self.layout = QVBoxLayout(self)  # для корректного отображения олимп. на scrollArea

        self.usersAll.update_fav_olymps(self.usersAll.getConnection('main'))  # обновление данных
        self.main_w.current_user.update_favorites_olymp()  # обновление данных
        self.update_olymp(self.current_user.favorites_olymps_dict)

    def update_olymp(self, olymp_dict: dict):  # обновление экрана с олимпиадами
        print(olymp_dict)
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
        self.layout.setContentsMargins(10, 10, 0, 400 - ((len(olymp_dict.values()) + len(olymp_dict.keys())) * 30))
        print(400 - ((len(olymp_dict.values()) + len(olymp_dict.keys())) * 30))
        print('сменилась')
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
