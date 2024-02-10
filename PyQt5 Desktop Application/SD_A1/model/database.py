import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("tickets.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                           (id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shows
                           (name TEXT NOT NULL,
                            singer TEXT NOT NULL,
                            date TEXT NOT NULL,
                            num_tickets INTEGER NOT NULL,
                            genre TEXT NOT NULL);''')
        self.conn.commit()

    def execute(self, statement, params=None):
        if params is None:
            self.cursor.execute(statement)
        else:
            self.cursor.execute(statement, params)
        self.conn.commit()

    def query(self, statement, params=None):
        if params is None:
            self.cursor.execute(statement)
        else:
            self.cursor.execute(statement, params)
        return self.cursor.fetchall()
