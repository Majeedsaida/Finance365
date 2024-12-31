from flask import Flask
from routes import app_routes
from app.utility.database import init_db

# Initialize the Flask app
app = Flask(__name__)

# Initialize the database
init_db()

# Register the routes
app.register_blueprint(app_routes)

if __name__ == "_main_":
    # Run the app
    app.run(debug=True)