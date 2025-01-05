from flask import jsonify
from sqlalchemy import func, extract, distinct
from models import Income, Expense  # Import Income and Expense models
from config import get_db_session  # Import function to get a DB session


def generate_summary():
    try:
        with get_db_session() as session:
            # Fetch all unique months from income and expenses
            months_query = (
                session.query(distinct(extract("month", Income.date)))
                .union(session.query(distinct(extract("month", Expense.date))))
                .order_by(extract("month", Income.date))
            )
            months = [str(month[0]).zfill(2) for month in months_query]

            all_monthly_summary = []

            for month in months:
                # Get income summary by category for the month
                income_summary_query = (
                    session.query(
                        Income.category, func.sum(Income.amount).label("total_income")
                    )
                    .filter(extract("month", Income.date) == int(month))
                    .group_by(Income.category)
                )
                income_summary = [
                    {"category": category, "total_income": total_income}
                    for category, total_income in income_summary_query
                ]

                # Get expense summary by category for the month
                expense_summary_query = (
                    session.query(
                        Expense.category,
                        func.sum(Expense.amount).label("total_expense"),
                    )
                    .filter(extract("month", Expense.date) == int(month))
                    .group_by(Expense.category)
                )
                expense_summary = [
                    {"category": category, "total_expense": total_expense}
                    for category, total_expense in expense_summary_query
                ]

                # Get total income and expenses for the month
                total_income = (
                    session.query(func.sum(Income.amount))
                    .filter(extract("month", Income.date) == int(month))
                    .scalar()
                    or 0
                )
                total_expenses = (
                    session.query(func.sum(Expense.amount))
                    .filter(extract("month", Expense.date) == int(month))
                    .scalar()
                    or 0
                )

                # Calculate remaining savings
                remaining_savings = total_income - total_expenses

                # Construct the summary for this month
                monthly_summary = {
                    "month": month,
                    "total_income": total_income,
                    "total_expenses": total_expenses,
                    "remaining_savings": remaining_savings,
                    "income_by_category": income_summary,
                    "expense_by_category": expense_summary,
                }

                all_monthly_summary.append(monthly_summary)

            # Construct final response
            response = {
                "monthly_summary": all_monthly_summary,
                "message": "Summary of income and expenses for all months.",
            }

            return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
