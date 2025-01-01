from flask import Blueprint, request, jsonify
from app.utility.database import add_income, update_income, get_income, delete_income

# Create a Blueprint for the income routes
income_routes = Blueprint("income_routes", __name__)

# Add Income Route
@income_routes.route("/income", methods=["POST"])
def add_income_route():
    data = request.get_json()
    amount = data.get("amount")
    description = data.get("description")
    date = data.get("date")

    if not all([amount, description, date]):
        return jsonify({"error": "Missing required fields"}), 400

    # Add the income to the database
    add_income(amount, description, date)
    return jsonify({"message": "Income added successfully!"}), 201


# Update Income Route
@income_routes.route("/income/<int:income_id>", methods=["PUT"])
def update_income_route(income_id):
    data = request.get_json()
    amount = data.get("amount")
    description = data.get("description")
    date = data.get("date")

    if not all([amount, description, date]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the income exists
    income = get_income(income_id)
    if not income:
        return jsonify({"error": "Income not found"}), 404

    # Update the income record in the database
    update_income(income_id, amount, description, date)
    return jsonify({"message": f"Income with ID {income_id} updated successfully!"}), 200


# View Income Route (All Income or Specific Income by ID)
@income_routes.route("/income", methods=["GET"])
@income_routes.route("/income/<int:income_id>", methods=["GET"])
def view_income_route(income_id=None):
    if income_id:
        income = get_income(income_id)
        if income:
            return jsonify(dict(income)), 200
        else:
            return jsonify({"error": "Income not found"}), 404
    else:
        incomes = get_income()
        return jsonify([dict(income) for income in incomes]), 200


# Delete Income Route
@income_routes.route("/income/<int:income_id>", methods=["DELETE"])
def delete_income_route(income_id):
    # Check if the income exists
    income = get_income(income_id)
    if not income:
        return jsonify({"error": "Income not found"}), 404

    # Delete the income record from the database
    delete_income(income_id)
    return jsonify({"message": f"Income with ID {income_id} deleted successfully!"}), 200
