import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect("app/utility/finance.db")
    conn.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
    return conn

# Initialize database tables (called once to create tables)
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript(
            """
            -- Income Table
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            );

            -- Expense Table
            CREATE TABLE IF NOT EXISTS expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category INTEGER NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (category) REFERENCES category(id)
            );

            -- Category Table
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
            """
        )
        conn.commit()

# Function to add an income entry
def add_income(amount, description, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO income (amount, description, date) VALUES (?, ?, ?)",
            (amount, description, date),
        )
        conn.commit()

# Function to get all income entries
def get_income(income_id=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if income_id:
            cursor.execute("SELECT * FROM income WHERE id = ?", (income_id,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM income")
            return cursor.fetchall()

# Function to update an income entry
def update_income(income_id, amount, description, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE income SET amount = ?, description = ?, date = ? WHERE id = ?",
            (amount, description, date, income_id),
        )
        conn.commit()

# Function to delete an income entry
def delete_income(income_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
        conn.commit()

# Function to add an expense entry
def add_expense(amount, category_id, description, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expense (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (amount, category_id, description, date),
        )
        conn.commit()

# Function to get all expenses
def get_expense(expense_id=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if expense_id:
            cursor.execute("SELECT * FROM expense WHERE id = ?", (expense_id,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM expense")
            return cursor.fetchall()

# Function to update an expense
def update_expense(expense_id, amount, category_id, description, date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE expense SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?",
            (amount, category_id, description, date, expense_id),
        )
        conn.commit()

# Function to delete an expense
def delete_expense(expense_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expense WHERE id = ?", (expense_id,))
        conn.commit()

# Function to add a category
def add_category(name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO category (name) VALUES (?)", (name,))
        conn.commit()

# Function to get all categories
def get_all_categories():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM category")
        return cursor.fetchall()

# Get Income vs Expenses Report for a specific month
def get_income_vs_expenses_report(year, month):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Calculate total income for the month
        cursor.execute(
            "SELECT SUM(amount) FROM income WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?",
            (str(year), str(month).zfill(2)),
        )
        total_income = cursor.fetchone()[0] or 0

        # Calculate total expenses for the month
        cursor.execute(
            "SELECT SUM(amount) FROM expense WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?",
            (str(year), str(month).zfill(2)),
        )
        total_expenses = cursor.fetchone()[0] or 0

        # Net savings calculation
        net_savings = total_income - total_expenses

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_savings": net_savings,
        }

# Get Expense Breakdown by Category for a specific month
def get_expense_breakdown_by_category(year, month):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category.name, SUM(expense.amount) AS total_expense
            FROM expense
            JOIN category ON expense.category = category.id
            WHERE strftime('%Y', expense.date) = ? 
            AND strftime('%m', expense.date) = ?
            GROUP BY category.name
            """, (str(year), str(month).zfill(2)))
        
        return cursor.fetchall()
