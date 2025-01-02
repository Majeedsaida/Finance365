import sqlite3
from flask import jsonify

DB_PATH = "app/features/finance.db"  # Path to your SQLite database


def handle_income(request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if request.method == "POST":
            # Add income record
            data = request.json
            cursor.execute(
                """
                INSERT INTO income (amount, source, category, date)
                VALUES (?, ?, ?, ?)
                """,
                (data["amount"], data["source"], data["category"], data["date"]),
            )
            conn.commit()
            return jsonify({"message": "Income added successfully"}), 201

        elif request.method == "GET":
            # View income records
            cursor.execute("SELECT * FROM income")
            records = cursor.fetchall()
            income_list = [
                {
                    "id": row[0],
                    "amount": row[1],
                    "source": row[2],
                    "category": row[3],
                    "date": row[4],
                }
                for row in records
            ]
            return jsonify({"income_records": income_list}), 200

        elif request.method == "PUT":
            # Update income record
            data = request.json
            cursor.execute(
                """
                UPDATE income
                SET amount = ?, source = ?, category = ?, date = ?
                WHERE id = ?
                """,
                (
                    data["amount"],
                    data["source"],
                    data["category"],
                    data["date"],
                    data["id"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Income record updated successfully"}), 200

        elif request.method == "DELETE":
            # Delete income record
            record_id = request.args.get("id")
            if not record_id:
                return jsonify({"error": "Record ID is required"}), 400
            cursor.execute("DELETE FROM income WHERE id = ?", (record_id,))
            conn.commit()
            return jsonify({"message": "Income record deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
