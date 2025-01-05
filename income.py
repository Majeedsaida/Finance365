from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Income  # Importing the Income model
from config import get_db_session  # Function to get a SQLAlchemy session


def handle_income():
    try:
        with get_db_session() as session:
            if request.method == "POST":
                # Add income record
                data = request.json
                new_income = Income(
                    amount=data["amount"],
                    source=data["source"],
                    category=data["category"],
                    date=data["date"],
                )
                session.add(new_income)
                session.commit()
                return jsonify({"message": "Income added successfully"}), 201

            elif request.method == "GET":
                # View income records
                records = session.query(Income).all()
                income_list = [
                    {
                        "id": record.id,
                        "amount": record.amount,
                        "source": record.source,
                        "category": record.category,
                        "date": record.date,
                    }
                    for record in records
                ]
                return jsonify({"income_records": income_list}), 200

            elif request.method == "PUT":
                # Update income record
                data = request.json
                income_record = session.query(Income).filter_by(id=data["id"]).first()
                if income_record:
                    income_record.amount = data["amount"]
                    income_record.source = data["source"]
                    income_record.category = data["category"]
                    income_record.date = data["date"]
                    session.commit()
                    return (
                        jsonify({"message": "Income record updated successfully"}),
                        200,
                    )
                else:
                    return jsonify({"error": "Income record not found"}), 404

            elif request.method == "DELETE":
                # Delete income record
                record_id = data.get("id")
                if not record_id:
                    return jsonify({"error": "Record ID is required"}), 400
                income_record = session.query(Income).filter_by(id=record_id).first()
                if income_record:
                    session.delete(income_record)
                    session.commit()
                    return (
                        jsonify({"message": "Income record deleted successfully"}),
                        200,
                    )
                else:
                    return jsonify({"error": "Income record not found"}), 404

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
