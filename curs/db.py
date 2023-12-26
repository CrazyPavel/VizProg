import sqlite3

from PyQt5.QtSql import QSqlTableModel

class DatabaseManager:
    def __init__(self, db_name='bday.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS birthdays 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                secname TEXT,
                birthday DATE,
                left INTEGER,
                picture BLOB)
        """)

    # def create_tables_1(self):
    #     # Создание таблицы с информацией о событиях
    #     self.cur.execute('''
    #         CREATE TABLE IF NOT EXISTS events
    #             (id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             Name TEXT,
    #             date DATE,
    #             left INTEGER
    #         )
    #     ''')

        self.conn.commit()

    # def add_birthday(self, name,opis,date,left,image):
    #     # Вставка данных в базу данных
    #     print(name,opis,date,left,image)
    #     #self.cur.executemany("INSERT INTO birthdays (name, secname, birthday, left, picture) VALUES (?, ?, ?, ?, ?)", [(record[0],record[1],record[2],record[3], image) for record in data])
    #     self.cur.executemany("INSERT INTO birthdays (name, secname, birthday, left, picture) VALUES (?, ?, ?, ?, ?)",
    #                          [(name, opis,date,left,image)])
    #     self.conn.commit()

    def add_birthday(self, data):

        for item in data:
            if len(item) == 5 and item[4] is not None:
                self.cur.execute('''
                    INSERT INTO birthdays (name, secname, birthday, left, picture)
                    VALUES (?, ?, ?, ?, ?)
                ''', (*item[:4], item[4]))  # Используйте * для распаковки кортежа
            else:
                # Если бинарных данных для фотографии нет, вставляем данные без фотографии
                self.cur.execute('''
                    INSERT INTO birthdays (name, secname, birthday, left)
                    VALUES (?, ?, ?, ?)
                ''', (*item[:-1],))  # Используйте * для распаковки кортежа

        self.conn.commit()

    def delete_birthday_by_id(self, birthday_id):
        try:
            self.cur.execute('DELETE FROM birthdays WHERE id = ?', (birthday_id,))
            self.commit_connection()
        except sqlite3.Error as error:
            print(f"Error while deleting birthday by ID from the database: {error}")

    def delete_data_by_row(self, row):
        try:
            birthday_id = self.get_birthday_id_by_row(row)
            self.delete_birthday_by_id(birthday_id)
        except sqlite3.Error as error:
            print(f"Error while deleting data by row from the database: {error}")

    def get_birthday_id_by_row(self, row):
        try:
            self.cur.execute('SELECT id FROM birthdays ORDER BY id LIMIT 1 OFFSET ?', (row,))
            result = self.cur.fetchone()
            if result:
                return result[0]
        except sqlite3.Error as error:
            print(f"Error while getting birthday ID by row from the database: {error}")

    def fetch_data_from_database(self):
        try:
            self.cur.execute('SELECT name, secname, birthday, Left, picture AS bi FROM birthdays')
            data = self.cur.fetchall()
            return data

        except sqlite3.Error as error:
            print(f"Error while fetching data from the database: {error}")

    def close_connection(self):
        self.conn.close()

    def commit_connection(self):
        self.conn.commit()

