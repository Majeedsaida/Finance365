import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def generate_visualization_data(month, year):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Format month to ensure it's always two digits
        month = f"{int(month):02d}"

        # Income by category for the given month
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total_amount 
            FROM income 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
            """,
            (month, year),
        )
        income_data = [
            {"category": row[0], "total_income": row[1]} for row in cursor.fetchall()
        ]

        # Expenses by category for the given month
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total_amount 
            FROM expenses 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
            """,
            (month, year),
        )
        expense_data = [
            {"category": row[0], "total_expense": row[1]} for row in cursor.fetchall()
        ]

        # Total income and expenses for the month
        cursor.execute(
            "SELECT SUM(amount) FROM income WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?",
            (month, year),
        )
        total_income = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?",
            (month, year),
        )
        total_expenses = cursor.fetchone()[0] or 0

        # Prepare data for visualization
        visualization_data = {
            "month": month,
            "year": year,
            "income_by_category": income_data,
            "expense_by_category": expense_data,
            "totals": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "remaining_savings": total_income - total_expenses,
            },
            "message": f"Visualization data for {month}/{year} generated successfully.",
        }

        return jsonify(visualization_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
