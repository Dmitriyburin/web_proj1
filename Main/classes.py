import sqlite3
import pymysql.cursors
from mysql.connector import connect, Error
import datetime


class User:
    def __init__(self):
        self.status = 'unregistered'


class UserRegistered(User):
    def __init__(self, id, name, password, class_count):
        super().__init__()
        self.id = id
        self.name = name
        self.password = password
        self.class_count = class_count
        self.status = 'registered'


class Admin(UserRegistered):
    def __init__(self, id, name, password, class_count):
        super().__init__(id, name, password, class_count)
        self.status = 'admin'


class Olympiad:
    def __init__(self, id: int, subject: str, title: str, school_class: int,
                 description: str, duration: int, link: str, date: datetime.date):
        self.title = title
        self.sch_class = school_class
        self.subject = subject
        self.des = description
        self.dur = duration
        self.link = link
        self.date = date
        self.id = id


class OlympiadsAll:
    def __init__(self):
        self.all_olymp_dict = {}

        # Подключиться к базе данных
        connection = self.getConnection('main')
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM olympiads')
                for olymp in cursor.fetchall():
                    if olymp['subject'] in self.all_olymp_dict:
                        self.all_olymp_dict[olymp['subject']].append(
                            Olympiad(olymp['id'], olymp['subject'], olymp['title'],
                                     olymp['school_class'],
                                     olymp['description'], olymp['duration'], olymp['link'], olymp['date']))
                    else:
                        self.all_olymp_dict[olymp['subject']] = [
                            Olympiad(olymp['id'], olymp['subject'], olymp['title'],
                                     olymp['school_class'],
                                     olymp['description'], olymp['duration'], olymp['link'], olymp['date'])]
        finally:
            # Закрыть соединение (Close connection).
            connection.commit()
            connection.close()
        print(self.all_olymp_dict)
        self.update_all_olymp_dict()
        # self.add_olymp(self.getConnection('main'), 'ГЕОМЕТРИЯ', 'ЖИЗНЬ', '9', 'круто', '90', 'ссылка', '14')

    def getConnection(self, name_database):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='admin',
                                     db=name_database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def add_olymp_db(self, con, olymp: Olympiad):
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO `olympiads` VALUES"
                    " (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                    "".format(olymp.subject, olymp.title, olymp.sch_class, olymp.des, olymp.dur, olymp.link,
                              olymp.date))
                cursor.execute('SELECT * FROM olympiads')
                print('\nДОБАВЛЕНО\n')
        finally:
            con.commit()
            con.close()

    def delete_olymp_db(self, con, olymp: Olympiad):
        try:
            with con.cursor() as cursor:
                cursor.execute('DELETE FROM olympiads WHERE id = "{}"'.format(olymp.id))
                print('\nУДАЛЕНО\n')
        finally:
            con.commit()
            con.close()

    def add_olymp(self, olymp: Olympiad):

        if olymp.subject in self.all_olymp_dict:
            self.all_olymp_dict[olymp.subject].append(
                Olympiad(self.getId(self.getConnection('main')) + 1, olymp.subject, olymp.title, olymp.sch_class,
                         olymp.des,
                         olymp.dur, olymp.link, olymp.date))
        else:
            self.all_olymp_dict[olymp.subject] = [
                Olympiad(self.getId(self.getConnection('main')) + 1, olymp.subject, olymp.title, olymp.sch_class,
                         olymp.des,
                         olymp.dur, olymp.link, olymp.date)]
        self.update_all_olymp_dict()
        self.add_olymp_db(self.getConnection('main'), olymp)

    def delete_olymp(self, olympiad: Olympiad):
        self.all_olymp_dict[olympiad.subject].pop(self.all_olymp_dict[olympiad.subject].index(olympiad))
        self.update_all_olymp_dict()
        self.delete_olymp_db(self.getConnection('main'), olympiad)

    def update_all_olymp_dict(self):
        for subject, olymps in self.all_olymp_dict.copy().items():
            if len(olymps) == 0:
                del self.all_olymp_dict[subject]
        self.all_olymp_dict = dict(sorted(self.all_olymp_dict.items()))

    def getId(self, con):
        try:
            with con.cursor() as cursor:
                cursor.execute('SELECT * FROM olympiads ORDER BY ID DESC LIMIT 1')
                if len(cursor.fetchall()) != 0:
                    cursor.execute('SELECT * FROM olympiads ORDER BY ID DESC LIMIT 1')
                    return cursor.fetchall()[0]['id']
                else:
                    return 0
        finally:
            con.commit()
            con.close()


class UsersAll:
    def __init__(self):
        self.user_all = {}

        # Подключиться к базе данных
        connection = self.getConnection('main')
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users')
                for user in cursor.fetchall():
                    self.user_all[user['name']] = [
                            UserRegistered(user['id'], user['name'], user['password'], user['class'])]
        finally:
            # Закрыть соединение (Close connection).
            connection.commit()
            connection.close()

    def add_user_db(self, con, user: UserRegistered):
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO `users` VALUES"
                    " (NULL, '{}', '{}', '{}')"
                    "".format(user.name, user.password, user.class_count))
                cursor.execute('SELECT * FROM olympiads')
                print('\nДОБАВЛЕНО\n')
        finally:
            con.commit()
            con.close()

    def add_user(self, user: UserRegistered):
        self.user_all[user.name] = [
            UserRegistered(user.id, user.name, user.password, user.class_count)]
        self.add_user_db(self.getConnection('main'), user)

    # def delete_olymp(self, user: User):
    #     self.all_olymp_dict[olympiad.subject].pop(self.all_olymp_dict[olympiad.subject].index(olympiad))
    #     self.update_all_olymp_dict()
    #     self.delete_olymp_db(self.getConnection('main'), olympiad)

    def getConnection(self, name_database):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='admin',
                                     db=name_database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

# cur.execute('CREATE TABLE IF NOT EXISTS olympiads(subject text, title text, school_class integer,'
#             'description text, duration integer, link text, count int)')
# # cur.execute("INSERT INTO olympiads VALUES ('Информатика', 'Олимпиада', '9', 'очень круто', '90', 'ссылка', '0')")
# #             "('Русский язык', 'Медвежонок', 9, 'очень круто', 90, 'ссылка', '0'),"
# #             "('Математика', 'Олимпиада ВШЭ', 9, 'очень круто', 90, 'ссылка', '0'),"
# #             "('Физика', 'Сириус', 9, 'очень круто', 90, 'ссылка', '0'),"
# #             "('Химия', 'Сириус', 9, 'очень круто', 90, 'ссылка', '0'),"
# #             "('Английский язык', 'Бульдог', 9, 'очень круто', 90, 'ссылка', '0')")

# CREATE TABLE participations (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, id_user INTEGER,
# id_olymp INTEGER, FOREIGN KEY (id_user)  REFERENCES users (id),  FOREIGN KEY (id_olymp)  REFERENCES olympiads (id));

#  CREATE TABLE olympiads (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, name TEXT, password TEXT, class INTEGER);

# "INSERT INTO `olympiads` VALUES ('1', 'Информатика', 'Олимпиада', '9', 'очень интеренснооо', '90', 'ссылка', '13')"
#
# INSERT
# INTO
# olympiads
# VALUES(NULL, 'Информатика', 'Олимпиада', '9', 'очень круто', '90', 'ссылка', '0'),
# (NULL, 'Русский язык', 'Медвежонок', 9, 'очень круто', 90, 'ссылка', '0'),
# (NULL, 'Математика', 'Олимпиада ВШЭ', 9, 'очень круто', 90, 'ссылка', '0'),
# (NULL, 'Физика', 'Сириус', 9, 'очень круто', 90, 'ссылка', '0'),
# (NULL, 'Химия', 'Сириус', 9, 'очень круто', 90, 'ссылка', '0'),
# (NULL, 'Английский язык', 'Бульдог', 9, 'очень круто', 90, 'ссылка', '0')


# cursor.execute(
#     "INSERT INTO `olympiads` VALUES"
#     " (NULL, 'Информатика', 'Олимпиада', '9', 'очень интеренснооо', '90', 'ссылка', '13')")
# cursor.execute('SELECT * FROM olympiads')
# print(cursor.fetchall())
