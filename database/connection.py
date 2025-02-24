import sqlite3
from contextlib import contextmanager

# Database file path
DATABASE_FILE = "orders.db"

# Initialize the database
def init_db():
    with get_db_connection() as conn:
        
        cursor = conn.cursor()
        
        cursor.execute('''
            DROP TABLE orders
        ''')
        

        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL CHECK(LENGTH(symbol) <= 5 AND symbol = UPPER(symbol)),
                price FLOAT NOT NULL CHECK(price > 0),
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                order_type TEXT NOT NULL CHECK(order_type IN ('buy', 'sell'))
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