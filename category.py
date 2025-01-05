from flask import request, jsonify
from sqlalchemy import func
from models import Expense  # Import the Expense model
from config import get_db_session  # Import the function to get a DB session


def handle_category():
    try:
        with get_db_session() as session:
            if request.method == "GET":
                # Group expenses by category with total amount
                expense_categories_query = (
                    session.query(
                        Expense.category, func.sum(Expense.amount).label("total_amount")
                    )
                    .group_by(Expense.category)
                    .order_by(func.sum(Expense.amount).desc())
                )
                expense_categories = [
                    {"category": category, "total_expense": total_amount}
                    for category, total_amount in expense_categories_query
                ]

                # Fetch all expenses grouped by category
                categories_expenses = {}
                for category_info in expense_categories:
                    category = category_info["category"]
                    expenses = session.query(Expense).filter_by(category=category).all()
                    categories_expenses[category] = [
                        {
                            "id": expense.id,
                            "amount": expense.amount,
                            "category": expense.category,
                            "description": expense.description,
                            "date": expense.date,
                        }
                        for expense in expenses
                    ]

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
