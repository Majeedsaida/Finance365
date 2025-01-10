from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from income import handle_income
from expense import handle_expense
from category import handle_category
from report import generate_report
from summary import generate_summary
from authentication import register_user, login_user

# Create a Blueprint for the routes
app_routes = Blueprint("app_routes", __name__)

from collections import OrderedDict
from flask import Response
import json


# Home Route (Root)
@app_routes.route("/")
def home():
    data = OrderedDict(
        {
            "message": "Welcome to Finance365! Your Personal Finance Management System",
            "description": (
                "Finance365 helps you manage your income, expenses, and savings effectively. "
                "It provides a simple API for recording transactions, generating reports, "
                "categorizing records, summarizing data, and visualizing your financial health."
            ),
            "endpoints": OrderedDict(
                {
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
                    "/register": {
                        "POST": "Register a new user with a username and password",
                    },
                    "/login": {
                        "POST": "Authenticate a user and return a JWT access token",
                    },
                }
            ),
            "note": "All endpoints require proper request formatting and valid parameters where applicable.",
        }
    )
    return Response(json.dumps(data), mimetype="application/json")


# Authentication Routes
@app_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data)


@app_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_user(data)


# Income Routes
@app_routes.route("/income", methods=["POST", "GET", "PUT", "DELETE"])
@jwt_required()
def income():
    return handle_income()


# Expense Routes
@app_routes.route("/expenses", methods=["POST", "GET", "PUT", "DELETE"])
@jwt_required()
def expense():
    return handle_expense()


# Report Route
@app_routes.route("/report", methods=["GET"])
@jwt_required()
def report():
    return generate_report()


# Expense Categorization Route
@app_routes.route("/category", methods=["GET"])
@jwt_required()
def category():
    return handle_category()


# Summary Route
@app_routes.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    return generate_summary()
