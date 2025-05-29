import sqlite3
from datetime import datetime

class InputService:
    def __init__(self, db_path='lokus_db'):
        self.db_path = db_path
        self.__init__database()

    def __init__database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budget_selections (
                    id TEXT PRIMARY KEY,
                    budget TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    
                    user_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
             ''')
        except sqlite3.Error as e: