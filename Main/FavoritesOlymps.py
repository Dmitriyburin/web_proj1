from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QLabel, QWidget

from classes import *



class FavoritesOlymps(QMainWindow):
    def __init__(self, usersAll, main_w, current_user: UserRegistered, program):
        super().__init__()
        uic.loadUi('../ui_files/favorites_olymp.ui', self)
        self.setFixedSize(self.size())

        self.usersAll = usersAll
        self.main_w = main_w
        self.current_user = current_user
        self.program = program

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
            frame.setStyleSheet(f'background-color: #ff9718; border-radius: 25px; '
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
            self.layout.addWidget(QLabel('У вас нет ни одной избранной олимпиады'))
        self.layout.setContentsMargins(10, 10, 0, 310 - ((len(olymp_dict.values()) + len(olymp_dict.keys())) * 30))
        print(400 - ((len(olymp_dict.values()) + len(olymp_dict.keys())) * 30))
        print('сменилась')
        self.widget.setLayout(self.layout)
        self.scrollArea.setWidget(self.widget)
        self.clicked_for_olymp()

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
                        background-color: #ff9718; 
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
                        color: #dedede;
                    }
                    """)
            return title_label

    def clicked_for_olymp(self):
        self.olymp_label_class = {}  # словарь ключ: QLabel олимпиады, значение: объект Olympiads
        self.current_olymps = None
        self.current_olymp = None
        self.flag_subject = False
        for frame in self.scrollArea.findChildren(QFrame):  # привязка события на все олимпиады (QLabel)
            if type(frame) == QFrame:
                for count, olymp in enumerate(frame.findChildren(QLabel)):
                    if count == 0:
                        self.flag_subject = True
                        self.current_olymps = self.current_user.favorites_olymps_dict[olymp.text()]

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
                self.program.show_olymp_window(self.olymp_label_class[obj])
            else:
                if self.main_w.is_admin:
                    self.program.show_create_olymp_window(obj.text())
        return super(QMainWindow, self).eventFilter(obj, e)
