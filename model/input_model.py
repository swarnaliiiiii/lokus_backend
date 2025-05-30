import sqlite3
import uuid
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
                    people_count INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
             ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")

    def save_budget_selection(self, budget, duration, people_count, type):
       try:
           conn = sqlite3.connect(self.db_path)
           cursor = conn.cursor()
           selection_id = str(uuid.uuid4())
           timestamp = datetime.utcnow().issoformat()
           cursor.execute('''
               INSERT INTO budget_selections (id, budget, duration, people_count, type, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
           ''', (selection_id, budget, duration, people_count, type, timestamp, timestamp))
           conn.commit()
           conn.close()
           return{
                    "status": "success",
                    "message": "User Input selection saved successfully.",
                    "id": selection_id
               }
       except Exception as e:
               print(f"Error saving budget selection: {e}")
               return {
                   "status": "error",
                   "message": f"Failed to save user input selection: {e}"
               }