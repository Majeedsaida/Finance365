import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"


def handle_category(request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if request.method == "GET":
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

            # Now, for each category, fetch all expense records
            categories_expenses = {}
            for category in [row["category"] for row in expense_categories]:
                cursor.execute(
                    """
                    SELECT id, amount, category, description, date 
                    FROM expenses 
                    WHERE category = ?
                    """,
                    (category,),
                )
                expenses = [
                    {
                        "id": row[0],
                        "amount": row[1],
                        "category": row[2],
                        "description": row[3],
                        "date": row[4],
                    }
                    for row in cursor.fetchall()
                ]
                categories_expenses[category] = expenses

            # Combine categorized expenses with summary info
            response = {
                "expense_categories": expense_categories,
                "categories_expenses": categories_expenses,
                "message": "This is a detailed categorization of your expenses.",
            }

            return jsonify(response), 200

        else:
            return jsonify({"error": "Method not allowed"}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
