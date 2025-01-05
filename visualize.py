from flask import jsonify
from sqlalchemy import func, extract
from models import Income, Expense  # Import your Income and Expense models
from config import get_db_session  # Import DB session configuration


def generate_visualization_data(month=None, year=None):
    try:
        with get_db_session() as session:
            if month and year:
                month = f"{int(month):02d}"  # Ensure month is two digits

                # Query income and expenses for specific month and year
                income_data_query = (
                    session.query(
                        Income.category, func.sum(Income.amount).label("total_income")
                    )
                    .filter(
                        extract("month", Income.date) == int(month),
                        extract("year", Income.date) == int(year),
                    )
                    .group_by(Income.category)
                )
                income_data = [
                    {"category": category, "total_income": total_income}
                    for category, total_income in income_data_query
                ]

                expense_data_query = (
                    session.query(
                        Expense.category,
                        func.sum(Expense.amount).label("total_expense"),
                    )
                    .filter(
                        extract("month", Expense.date) == int(month),
                        extract("year", Expense.date) == int(year),
                    )
                    .group_by(Expense.category)
                )
                expense_data = [
                    {"category": category, "total_expense": total_expense}
                    for category, total_expense in expense_data_query
                ]

                # Calculate monthly totals
                total_income = (
                    session.query(func.sum(Income.amount))
                    .filter(
                        extract("month", Income.date) == int(month),
                        extract("year", Income.date) == int(year),
                    )
                    .scalar()
                    or 0
                )
                total_expenses = (
                    session.query(func.sum(Expense.amount))
                    .filter(
                        extract("month", Expense.date) == int(month),
                        extract("year", Expense.date) == int(year),
                    )
                    .scalar()
                    or 0
                )

                remaining_savings = total_income - total_expenses

                visualization_data = {
                    "month": month,
                    "year": year,
                    "income_by_category": income_data,
                    "expense_by_category": expense_data,
                    "totals": {
                        "total_income": total_income,
                        "total_expenses": total_expenses,
                        "remaining_savings": remaining_savings,
                    },
                    "message": f"Visualization data for {month}/{year} generated successfully.",
                }

            elif year:
                # Income and expenses grouped by month for the given year
                income_data_query = (
                    session.query(
                        extract("month", Income.date).label("month"),
                        func.sum(Income.amount).label("total_income"),
                    )
                    .filter(extract("year", Income.date) == int(year))
                    .group_by("month")
                    .order_by("month")
                )
                income_data = [
                    {"month": f"{month:02d}", "total_income": total_income}
                    for month, total_income in income_data_query
                ]

                expense_data_query = (
                    session.query(
                        extract("month", Expense.date).label("month"),
                        func.sum(Expense.amount).label("total_expense"),
                    )
                    .filter(extract("year", Expense.date) == int(year))
                    .group_by("month")
                    .order_by("month")
                )
                expense_data = [
                    {"month": f"{month:02d}", "total_expense": total_expense}
                    for month, total_expense in expense_data_query
                ]

                total_income = (
                    session.query(func.sum(Income.amount))
                    .filter(extract("year", Income.date) == int(year))
                    .scalar()
                    or 0
                )
                total_expenses = (
                    session.query(func.sum(Expense.amount))
                    .filter(extract("year", Expense.date) == int(year))
                    .scalar()
                    or 0
                )

                remaining_savings = total_income - total_expenses

                visualization_data = {
                    "year": year,
                    "income_by_month": income_data,
                    "expense_by_month": expense_data,
                    "totals": {
                        "total_income": total_income,
                        "total_expenses": total_expenses,
                        "remaining_savings": remaining_savings,
                    },
                    "message": f"Visualization data for {year} generated successfully.",
                }

            return jsonify(visualization_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
