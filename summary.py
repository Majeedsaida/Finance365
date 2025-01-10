from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from models import Income, Expense  # Importing the Income and Expense models
from config import get_db_session  # Function to get a SQLAlchemy session


def generate_summary():
    try:
        with get_db_session() as session:
            # Query the total income for each month in the year
            income_summary = (
                session.query(
                    func.extract("month", Income.date).label("month"),
                    func.sum(Income.amount).label("total_income"),
                )
                .group_by(func.extract("month", Income.date))
                .order_by("month")
                .all()
            )

            # Query the total expenses for each month in the year
            expense_summary = (
                session.query(
                    func.extract("month", Expense.date).label("month"),
                    func.sum(Expense.amount).label("total_expenses"),
                )
                .group_by(func.extract("month", Expense.date))
                .order_by("month")
                .all()
            )

            # Combine the income and expense summaries into a single summary
            monthly_summary = []
            for month in range(1, 13):
                # Find the income and expense for the current month
                income = next(
                    (item[1] for item in income_summary if item[0] == month), 0
                )
                expenses = next(
                    (item[1] for item in expense_summary if item[0] == month), 0
                )

                # Calculate net savings
                net_savings = income - expenses

                # Append the data for the month
                monthly_summary.append(
                    {
                        "month": month,
                        "total_income": income,
                        "total_expenses": expenses,
                        "net_savings": net_savings,
                    }
                )

            return jsonify({"monthly_summary": monthly_summary}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
