import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('your_database_file')
        self.cursor = self.connection.cursor()

    def get_subs(self, status=True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'subs' WHERE status = ?", (status,)).fetchall()

    def is_in_database(self, user_id):
        with self.connection:
            return bool(self.cursor.execute("SELECT * FROM 'subs' WHERE user = ?", (user_id,)).rowcount)

    def add_sub(self, user_id, status=True):
        with self.connection:
            self.cursor.execute("INSERT INTO 'subs' ('user', 'status') VALUES (?, ?)", (user_id, status))

    def update_sub(self, user_id, status):
        with self.connection:
            self.cursor.execute("UPDATE 'subs' SET status = ? WHERE user = ?", (status, user_id))
