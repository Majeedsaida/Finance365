import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def generate_summary(month, year):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Format month to ensure it's always two digits
        month = f"{int(month):02d}"

        # Filter income for the given month and year
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total_amount 
            FROM income 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
            """,
            (month, year),
        )
        income_summary = [
            {"category": row[0], "total_income": row[1]} for row in cursor.fetchall()
        ]

        # Filter expenses for the given month and year
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total_amount 
            FROM expenses 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
            """,
            (month, year),
        )
        expense_summary = [
            {"category": row[0], "total_expense": row[1]} for row in cursor.fetchall()
        ]

        # Total income for the month
        cursor.execute(
            "SELECT SUM(amount) FROM income WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?",
            (month, year),
        )
        total_income = cursor.fetchone()[0] or 0

        # Total expenses for the month
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?",
            (month, year),
        )
        total_expenses = cursor.fetchone()[0] or 0

        # Calculate remaining savings for the month
        remaining_savings = total_income - total_expenses

        # Construct the summary
        summary = {
            "month": month,
            "year": year,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "remaining_savings": remaining_savings,
            "income_by_category": income_summary,
            "expense_by_category": expense_summary,
            "message": f"Summary for {month}/{year} showing categorized income and expenses.",
        }

        return jsonify(summary), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
