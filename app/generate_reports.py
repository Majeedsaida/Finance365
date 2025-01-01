from flask import Blueprint, request, jsonify
from app.utility.database import (
    get_income_vs_expenses_report,
    get_expense_breakdown_by_category,
)

# Create a Blueprint for the expense routes
expense_routes = Blueprint("expense_routes", __name__)

# Generate Income vs Expenses Report
@expense_routes.route("/report/income-vs-expenses", methods=["GET"])
def generate_income_vs_expenses_report():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if not year or not month:
        return jsonify({"error": "Both year and month are required"}), 400

    report = get_income_vs_expenses_report(year, month)
    return jsonify(report), 200

# Generate Expense Breakdown by Category Report
@expense_routes.route("/report/expense-breakdown", methods=["GET"])
def generate_expense_breakdown_report():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if not year or not month:
        return jsonify({"error": "Both year and month are required"}), 400

    breakdown = get_expense_breakdown_by_category(year, month)
    return jsonify([dict(record) for record in breakdown]), 200
