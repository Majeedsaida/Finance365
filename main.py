from flask import Flask
from app.routes.expense_features import expense_routes  # Routes for handling expenses, categories, and reports
from app.utility.database import init_db  # Initializes the database

# Initialize the Flask app
app = Flask(__name__)

# Initialize the database (run this function only once to create tables if needed)
init_db()

# Register the expense-related routes (includes adding expenses, viewing, updating, deleting, categorizing, and generating reports)
app.register_blueprint(expense_routes)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
