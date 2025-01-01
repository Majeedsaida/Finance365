from flask import Blueprint, request, jsonify
from app.utility.database import (
    add_expense,
    update_expense,
    get_expense,
    delete_expense,
    add_category,
    get_all_categories,
    get_expenses_by_month,
    get_monthly_summary,
)

# Create a Blueprint for the expense routes
expense_routes = Blueprint("expense_routes", __name__)

# Add Category Route
@expense_routes.route("/category", methods=["POST"])
def add_category_route():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    add_category(name)
    return jsonify({"message": "Category added successfully!"}), 201


# Get All Categories Route
@expense_routes.route("/category", methods=["GET"])
def get_categories_route():
    categories = get_all_categories()
    return jsonify([dict(category) for category in categories]), 200


# Add Expense Route (with Category)
@expense_routes.route("/expense", methods=["POST"])
def add_expense_route():
    data = request.get_json()
    amount = data.get("amount")
    category_id = data.get("category_id")
    description = data.get("description")
    date = data.get("date")

    if not all([amount, category_id, description, date]):
        return jsonify({"error": "Missing required fields"}), 400

    add_expense(amount, category_id, description, date)
    return jsonify({"message": "Expense added successfully!"}), 201


# Monthly Summary Route
@expense_routes.route("/summary", methods=["GET"])
def monthly_summary_route():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if not year or not month:
        return jsonify({"error": "Both year and month are required"}), 400

    summary = get_monthly_summary(year, month)
    return jsonify(summary), 200


# View Expenses for a Specific Month
@expense_routes.route("/expense/month", methods=["GET"])
def view_expenses_by_month_route():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if not year or not month:
        return jsonify({"error": "Both year and month are required"}), 400

    expenses = get_expenses_by_month(year, month)
    return jsonify([dict(expense) for expense in expenses]), 200
