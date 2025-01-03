import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def generate_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Fetch all unique months in the database (in 'MM' format)
        cursor.execute(
            """
            SELECT DISTINCT strftime('%m', date) AS month
            FROM income
            UNION
            SELECT DISTINCT strftime('%m', date) AS month
            FROM expenses
            ORDER BY month
            """
        )
        months = [row[0] for row in cursor.fetchall()]

        all_monthly_summary = []

        for month in months:
            # Filter income for the given month
            cursor.execute(
                """
                SELECT category, SUM(amount) AS total_amount 
                FROM income 
                WHERE strftime('%m', date) = ?
                GROUP BY category
                """,
                (month,),
            )
            income_summary = [
                {"category": row[0], "total_income": row[1]}
                for row in cursor.fetchall()
            ]

            # Filter expenses for the given month
            cursor.execute(
                """
                SELECT category, SUM(amount) AS total_amount 
                FROM expenses 
                WHERE strftime('%m', date) = ?
                GROUP BY category
                """,
                (month,),
            )
            expense_summary = [
                {"category": row[0], "total_expense": row[1]}
                for row in cursor.fetchall()
            ]

            # Total income for the month
            cursor.execute(
                "SELECT SUM(amount) FROM income WHERE strftime('%m', date) = ?",
                (month,),
            )
            total_income = cursor.fetchone()[0] or 0

            # Total expenses for the month
            cursor.execute(
                "SELECT SUM(amount) FROM expenses WHERE strftime('%m', date) = ?",
                (month,),
            )
            total_expenses = cursor.fetchone()[0] or 0

            # Calculate remaining savings for the month
            remaining_savings = total_income - total_expenses

            # Construct the summary for this month
            monthly_summary = {
                "month": month,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "remaining_savings": remaining_savings,
                "income_by_category": income_summary,
                "expense_by_category": expense_summary,
            }

            all_monthly_summary.append(monthly_summary)

        # Construct final response with summaries for all months
        response = {
            "monthly_summary": all_monthly_summary,
            "message": "Summary of income and expenses for all months.",
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
