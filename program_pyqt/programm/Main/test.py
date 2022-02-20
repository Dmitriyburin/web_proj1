import pymysql


def getConnection(name_database):  # возвращает connection для работы с бд
    connection = pymysql.connect(host='5.23.55.52',
                                 user='root',
                                 password='main_admin',
                                 db=name_database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def test(con):
    with con.cursor() as cursor:
        cursor.execute('SELECT * FROM ')


print(getConnection('main'))
