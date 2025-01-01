from flask import Blueprint, request, jsonify
from app.utility.database import add_expense, update_expense, get_expense, delete_expense

# Create a Blueprint for the expense routes
expense_routes = Blueprint("expense_routes", __name__)

# Add Expense Route
@expense_routes.route("/expense", methods=["POST"])
def add_expense_route():
    data = request.get_json()
    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description")
    date = data.get("date")

    if not all([amount, category, description, date]):
        return jsonify({"error": "Missing required fields"}), 400

    # Add the expense to the database
    add_expense(amount, category, description, date)
    return jsonify({"message": "Expense added successfully!"}), 201


# Update Expense Route
@expense_routes.route("/expense/<int:expense_id>", methods=["PUT"])
def update_expense_route(expense_id):
    data = request.get_json()
    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description")
    date = data.get("date")

    if not all([amount, category, description, date]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the expense exists
    expense = get_expense(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    # Update the expense record in the database
    update_expense(expense_id, amount, category, description, date)
    return jsonify({"message": f"Expense with ID {expense_id} updated successfully!"}), 200


# View Expense Route (All Expenses or Specific Expense by ID)
@expense_routes.route("/expense", methods=["GET"])
@expense_routes.route("/expense/<int:expense_id>", methods=["GET"])
def view_expense_route(expense_id=None):
    if expense_id:
        expense = get_expense(expense_id)
        if expense:
            return jsonify(dict(expense)), 200
        else:
            return jsonify({"error": "Expense not found"}), 404
    else:
        expenses = get_expense()
        return jsonify([dict(expense) for expense in expenses]), 200


# Delete Expense Route
@expense_routes.route("/expense/<int:expense_id>", methods=["DELETE"])
def delete_expense_route(expense_id):
    # Check if the expense exists
    expense = get_expense(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    # Delete the expense record from the database
    delete_expense(expense_id)
    return jsonify({"message": f"Expense with ID {expense_id} deleted successfully!"}), 200
