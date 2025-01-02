import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def handle_category(request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if request.method == "GET":
            # Group income by category
            cursor.execute(
                """
                SELECT category, SUM(amount) AS total_amount 
                FROM income 
                GROUP BY category 
                ORDER BY total_amount DESC
                """
            )
            income_categories = [
                {"category": row[0], "total_income": row[1]}
                for row in cursor.fetchall()
            ]

            # Group expenses by category
            cursor.execute(
                """
                SELECT category, SUM(amount) AS total_amount 
                FROM expenses 
                GROUP BY category 
                ORDER BY total_amount DESC
                """
            )
            expense_categories = [
                {"category": row[0], "total_expense": row[1]}
                for row in cursor.fetchall()
            ]

            # Combine results into a categorized summary
            response = {
                "income_categories": income_categories,
                "expense_categories": expense_categories,
                "message": "This is a detailed categorization of your income and expenses.",
            }

            return jsonify(response), 200

        elif request.method == "POST":
            # Add a new record with category
            data = request.json

            if "type" not in data or data["type"] not in ["income", "expense"]:
                return (
                    jsonify({"error": "Invalid type. Must be 'income' or 'expense'."}),
                    400,
                )

            if data["type"] == "income":
                cursor.execute(
                    "INSERT INTO income (amount, source, category, date) VALUES (?, ?, ?, ?)",
                    (data["amount"], data["source"], data["category"], data["date"]),
                )
            elif data["type"] == "expense":
                cursor.execute(
                    "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                    (data["amount"], data["category"], data["date"]),
                )

            conn.commit()
            return (
                jsonify(
                    {
                        "message": f"{data['type'].capitalize()} record added successfully"
                    }
                ),
                201,
            )

        else:
            return jsonify({"error": "Method not allowed"}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
