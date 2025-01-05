from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User  # Import the User model
from config import get_db_session  # Import the function to get a DB session


def register_user(data):
    try:
        # Get a session instance
        with get_db_session() as session:
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400

            # Check if the user already exists
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                return jsonify({"error": "User already exists"}), 400

            # Hash the password and insert the user
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            session.add(new_user)
            session.commit()

            return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def login_user(data):
    try:
        # Get a session instance
        with get_db_session() as session:
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400

            # Retrieve the user record
            user = session.query(User).filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                return jsonify({"error": "Invalid credentials"}), 401

            # Generate JWT token
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
