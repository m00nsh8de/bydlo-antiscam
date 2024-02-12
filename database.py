import sqlite3

class DatabaseManager:
    def __init__(self):
        self.db_name = 'banned_words.db'
        self.table_name = 'banned_words'
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        try:
            self.conn.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    word TEXT PRIMARY KEY
                )
            ''')
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")

    def add_banned_word(self, word):
        try:
            with self.conn:
                self.conn.execute(f"INSERT INTO {self.table_name} (word) VALUES (?)", (word,))
        except sqlite3.IntegrityError:
            print(f"Слово '{word}' уже существует в списке.")

    def remove_banned_word(self, word):
        try:
            with self.conn:
                self.conn.execute(f"DELETE FROM {self.table_name} WHERE word = ?", (word,))
        except Exception as e:
            print(f"Ошибка при удалении слова: {e}")

    def get_banned_words(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT word FROM {self.table_name}")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при извлечении списка запрещенных слов: {e}")
            return []

    def __del__(self):
        self.conn.close()
