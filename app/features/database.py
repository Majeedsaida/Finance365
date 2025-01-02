import sqlite3

DB_PATH = "app/features/finance.db"  # Path to your SQLite database


def init_db():
    """
    Initialize the database and create the required tables if they don't already exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Create the income table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """
        )

        # Create the expenses table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """
        )

        # Commit the changes
        conn.commit()
        print("Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

    finally:
        conn.close()
