import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def generate_visualization_data(month=None, year=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # If month and year are both provided, filter by both
        if month and year:
            # Format month to ensure it's always two digits
            month = f"{int(month):02d}"

            # Fetch income and expense data for the specific month and year
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
                {"category": row[0], "total_income": row[1]}
                for row in cursor.fetchall()
            ]

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
                {"category": row[0], "total_expense": row[1]}
                for row in cursor.fetchall()
            ]

            # Calculate totals for the month
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

            remaining_savings = total_income - total_expenses

            # Prepare visualization data
            visualization_data = {
                "month": month,
                "year": year,
                "income_by_category": income_data,
                "expense_by_category": expense_data,
                "totals": {
                    "total_income": total_income,
                    "total_expenses": total_expenses,
                    "remaining_savings": remaining_savings,
                },
                "message": f"Visualization data for {month}/{year} generated successfully.",
            }

        # If only year is provided, visualize data for the entire year
        elif year:
            cursor.execute(
                """
                SELECT strftime('%m', date) AS month, SUM(amount) AS total_income
                FROM income
                WHERE strftime('%Y', date) = ?
                GROUP BY month
                ORDER BY month
                """,
                (year,),
            )
            income_data = [
                {"month": row[0], "total_income": row[1]} for row in cursor.fetchall()
            ]

            cursor.execute(
                """
                SELECT strftime('%m', date) AS month, SUM(amount) AS total_expense
                FROM expenses
                WHERE strftime('%Y', date) = ?
                GROUP BY month
                ORDER BY month
                """,
                (year,),
            )
            expense_data = [
                {"month": row[0], "total_expense": row[1]} for row in cursor.fetchall()
            ]

            # Calculate yearly totals
            cursor.execute(
                "SELECT SUM(amount) FROM income WHERE strftime('%Y', date) = ?", (year,)
            )
            total_income = cursor.fetchone()[0] or 0

            cursor.execute(
                "SELECT SUM(amount) FROM expenses WHERE strftime('%Y', date) = ?",
                (year,),
            )
            total_expenses = cursor.fetchone()[0] or 0

            remaining_savings = total_income - total_expenses

            # Prepare visualization data
            visualization_data = {
                "year": year,
                "income_by_month": income_data,
                "expense_by_month": expense_data,
                "totals": {
                    "total_income": total_income,
                    "total_expenses": total_expenses,
                    "remaining_savings": remaining_savings,
                },
                "message": f"Visualization data for {year} generated successfully.",
            }

        return jsonify(visualization_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
