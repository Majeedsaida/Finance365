from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Expense  # Importing the Expense model
from config import get_db_session  # Function to get a SQLAlchemy session


def handle_expense():
    try:
        with get_db_session() as session:
            if request.method == "POST":
                # Add expense record
                data = request.json
                new_expense = Expense(
                    amount=data["amount"],
                    category=data["category"],
                    description=data["description"],
                    date=data["date"],
                )
                session.add(new_expense)
                session.commit()
                return jsonify({"message": "Expense added successfully"}), 201

            elif request.method == "GET":
                # View expense records
                expenses = session.query(Expense).all()
                expense_list = [
                    {
                        "id": expense.id,
                        "amount": expense.amount,
                        "category": expense.category,
                        "description": expense.description,
                        "date": expense.date,
                    }
                    for expense in expenses
                ]
                return jsonify({"expense_records": expense_list}), 200

            elif request.method == "PUT":
                # Update expense record
                data = request.json
                expense = session.query(Expense).filter_by(id=data["id"]).first()
                if expense:
                    expense.amount = data["amount"]
                    expense.category = data["category"]
                    expense.description = data["description"]
                    expense.date = data["date"]
                    session.commit()
                    return (
                        jsonify({"message": "Expense record updated successfully"}),
                        200,
                    )
                else:
                    return jsonify({"error": "Expense record not found"}), 404

            elif request.method == "DELETE":
                # Delete expense record
                record_id = data.get("id")
                if not record_id:
                    return jsonify({"error": "Record ID is required"}), 400

                expense = session.query(Expense).filter_by(id=record_id).first()
                if expense:
                    session.delete(expense)
                    session.commit()
                    return (
                        jsonify({"message": "Expense record deleted successfully"}),
                        200,
                    )
                else:
                    return jsonify({"error": "Expense record not found"}), 404

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
