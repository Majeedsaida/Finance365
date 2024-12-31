from flask import Blueprint, request, jsonify

# Create a Blueprint for the routes
app_routes = Blueprint("app_routes", __name__)


# Home Route (Root)
@app_routes.route("/")
def home():
    return (
        jsonify(
            {
                "message": "Welcome to the Finance365! Your Personal Finance Management System"
            }
        ),
        200,
    )


# Income Routes
@app_routes.route("/income")
def income():
    # Placeholder for adding income functionality
    return jsonify({"message": "Add income functionality"}), 200


# Expense Routes
@app_routes.route("/expense")
def expense():
    # Placeholder for adding expense functionality
    return jsonify({"message": "Add expense functionality"}), 200


@app_routes.route("/report/income-vs-expenses")
def report():
    # Placeholder for generating income vs expenses report functionality
    return jsonify({"message": "Income vs Expenses report functionality"}), 200


# Expense Categorization Route
@app_routes.route("/category")
def category():
    # Placeholder for categorizing expense functionality
    return jsonify({"message": "Categorize expense functionality"}), 200
