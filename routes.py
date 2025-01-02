from flask import Blueprint, request, jsonify
from app.features.income import handle_income
from app.features.expense import handle_expense
from app.features.category import handle_category
from app.features.report import generate_report
from app.features.summary import generate_summary
from app.features.visualize import generate_visualization_data

# Create a Blueprint for the routes
app_routes = Blueprint("app_routes", __name__)


# Home Route (Root)
@app_routes.route("/")
def home():
    return (
        jsonify(
            {
                "message": "Welcome to Finance365! Your Personal Finance Management System",
                "description": (
                    "Finance365 helps you manage your income, expenses, and savings effectively. "
                    "It provides a simple API for recording transactions, generating reports, "
                    "categorizing records, summarizing data, and visualizing your financial health."
                ),
                "endpoints": {
                    "/income": {
                        "POST": "Add a new income record",
                        "GET": "Retrieve all income records",
                        "PUT": "Update an existing income record",
                        "DELETE": "Delete an income record",
                    },
                    "/expenses": {
                        "POST": "Add a new expense record",
                        "GET": "Retrieve all expense records",
                        "PUT": "Update an existing expense record",
                        "DELETE": "Delete an expense record",
                    },
                    "/report": {
                        "GET": "Generate an overall financial report, including income, expenses, and savings",
                    },
                    "/categorize": {
                        "GET": "Retrieve income and expense records grouped by category",
                    },
                    "/summary": {
                        "GET": "Get a summary of income and expenses for a specific month",
                    },
                    "/visualize": {
                        "GET": "Generate data for visualizations of income and expenses",
                    },
                },
                "note": "All endpoints require proper request formatting and valid parameters where applicable.",
            }
        ),
        200,
    )


# Income Routes
@app_routes.route("/income", methods=["POST", "GET", "PUT", "DELETE"])
def income():
    return handle_income(request)


# Expense Routes
@app_routes.route("/expenses", methods=["POST", "GET", "PUT", "DELETE"])
def expense():
    return handle_expense(request)


# Report Route
@app_routes.route("/report", methods=["GET"])
def report():
    return generate_report()


# Expense Categorization Route
@app_routes.route("/category", methods=["GET", "POST"])
def category():
    return handle_category(request)


# Summary Route
@app_routes.route("/summary", methods=["GET"])
def summary():
    month = request.args.get("month")
    year = request.args.get("year")
    if not month or not year:
        return jsonify({"error": "Month and Year are required"}), 400
    return generate_summary(month, year)


# Visualization Route
@app_routes.route("/visualize", methods=["GET"])
def visualize():
    return generate_visualization_data()
