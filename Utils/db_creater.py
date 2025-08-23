import sqlite3

class DBCreator
    def __init__(self, _path):
        self.conn = sqlite3.connect(_path)
        pass

    def drop_table(self):
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS schema")
        cur.execute("DROP TABLE IF EXISTS info")
        conn.commit()


    def init_schema(self):
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS schema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_type TEXT NOT NULL,
            platform_name TEXT NOT NULL,
            creator TEXT
        )
        ''')
        pass

    def __del__(self):
        self.conn.close()
