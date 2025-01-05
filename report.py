from flask import request, jsonify
from sqlalchemy import func, extract
from models import Income, Expense  # Import the Income and Expense models
from config import get_db_session  # Import the function to get a DB session


def generate_report():
    # Get the month from the POST request
    month = request.json.get("month")

    if not month:
        return jsonify({"error": "Month is required."}), 400

    if len(month) != 2 or not month.isdigit():
        return jsonify({"error": "Invalid month format. Please use 'MM' format."}), 400

    try:
        with get_db_session() as session:
            # Fetch total income for the given month
            total_income = (
                session.query(func.sum(Income.amount))
                .filter(extract("month", Income.date) == int(month))
                .scalar()
                or 0
            )

            # Fetch total expenses for the given month
            total_expenses = (
                session.query(func.sum(Expense.amount))
                .filter(extract("month", Expense.date) == int(month))
                .scalar()
                or 0
            )

            # Calculate remaining savings
            remaining_savings = total_income - total_expenses

            # Fetch category-wise breakdown of expenses for the given month
            expense_breakdown_query = (
                session.query(Expense.category, func.sum(Expense.amount).label("total"))
                .filter(extract("month", Expense.date) == int(month))
                .group_by(Expense.category)
                .order_by(func.sum(Expense.amount).desc())
            )
            expense_breakdown = [
                {"category": category, "total": total}
                for category, total in expense_breakdown_query
            ]

            # Determine financial health status
            if remaining_savings > 0:
                financial_status = (
                    "Your finances are in good shape! You have saved money this period."
                )
            elif remaining_savings == 0:
                financial_status = (
                    "You have broken even, with no savings or overspending."
                )
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
                "message": f"This report provides a detailed overview of your financial health for the month {month}.",
            }

            return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
