import sqlite3
from contextlib import contextmanager

# Database file path
DATABASE_FILE = "orders.db"

# Initialize the database
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                symbol TEXT,
                price FLOAT,
                quantity INTEGER,
                order_type TEXT
            )
        ''')
        conn.commit()

# Context manager for database connections
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

# Context manager for database cursors
@contextmanager
def get_db_cursor():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            conn.commit()