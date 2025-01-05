from flask import Flask
from personalfinance import app_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "KRANKEN007"
# Register the routes
app.register_blueprint(app_routes)

if __name__ == "__main__":
    # Run the app
    app.run(debug=True)
