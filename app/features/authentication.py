import sqlite3
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

DB_PATH = "app/features/finance.db"  # Path to your SQLite database


def register_user(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if the user already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return jsonify({"error": "User already exists"}), 400

        # Hash the password and insert the user
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()


def login_user(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Retrieve the user record
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        record = cursor.fetchone()

        if not record or not check_password_hash(record[0], password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate JWT token
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()
