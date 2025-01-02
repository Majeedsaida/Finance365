import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def generate_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Fetch total income
        cursor.execute("SELECT SUM(amount) FROM income")
        total_income = cursor.fetchone()[0] or 0

        # Fetch total expenses
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0

        # Calculate remaining savings
        remaining_savings = total_income - total_expenses

        # Fetch category-wise breakdown of expenses
        cursor.execute(
            """
            SELECT category, SUM(amount) 
            FROM expenses 
            GROUP BY category 
            ORDER BY SUM(amount) DESC
            """
        )
        expense_breakdown = [
            {"category": row[0], "total": row[1]} for row in cursor.fetchall()
        ]

        # Determine financial health status
        if remaining_savings > 0:
            financial_status = (
                "Your finances are in good shape! You have saved money this period."
            )
        elif remaining_savings == 0:
            financial_status = "You have broken even, with no savings or overspending."
        else:
            financial_status = "Your expenses have exceeded your income. Consider reviewing your spending habits."

        # Prepare detailed response
        report = {
            "summary": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "remaining_savings": remaining_savings,
            },
            "details": {
                "expense_breakdown": expense_breakdown,
                "financial_status": financial_status,
            },
            "message": "This report provides a detailed overview of your current financial health.",
        }

        return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
