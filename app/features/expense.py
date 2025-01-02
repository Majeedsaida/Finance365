import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"  # Path to your SQLite database


def handle_expense(request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if request.method == "POST":
            # Add expense record
            data = request.json
            cursor.execute(
                """
                INSERT INTO expenses (amount, category, description, date)
                VALUES (?, ?, ?, ?)
                """,
                (data["amount"], data["category"], data["description"], data["date"]),
            )
            conn.commit()
            return jsonify({"message": "Expense added successfully"}), 201

        elif request.method == "GET":
            # View expense records
            cursor.execute("SELECT * FROM expenses")
            records = cursor.fetchall()
            expense_list = [
                {
                    "id": row[0],
                    "amount": row[1],
                    "category": row[2],
                    "description": row[3],
                    "date": row[4],
                }
                for row in records
            ]
            return jsonify({"expense_records": expense_list}), 200

        elif request.method == "PUT":
            # Update expense record
            data = request.json
            cursor.execute(
                """
                UPDATE expenses
                SET amount = ?, category = ?, description = ?, date = ?
                WHERE id = ?
                """,
                (
                    data["amount"],
                    data["category"],
                    data["description"],
                    data["date"],
                    data["id"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Expense record updated successfully"}), 200

        elif request.method == "DELETE":
            # Delete expense record
            record_id = request.args.get("id")
            if not record_id:
                return jsonify({"error": "Record ID is required"}), 400
            cursor.execute("DELETE FROM expenses WHERE id = ?", (record_id,))
            conn.commit()
            return jsonify({"message": "Expense record deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
