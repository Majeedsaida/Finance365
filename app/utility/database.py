import sqlite3


def get_db_connection():
    conn = sqlite3.connect("app/utility/finance.db")
    conn.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
    return conn


def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript(
            """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """
        )
        conn.commit()
