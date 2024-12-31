from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta

# Initialize the app
app = Flask(__name__)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'  # Change to your preferred DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and JWT Manager
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class IncomeExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

# Routes

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # Password should be hashed in production

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# User Login (JWT Token Generation)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:  # In production, use password hashing!
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Add Income or Expense
@app.route('/transaction', methods=['POST'])
@jwt_required()
def add_transaction():
    current_user = get_jwt_identity()
    data = request.get_json()

    transaction_type = data.get('type')  # 'income' or 'expense'
    amount = data.get('amount')
    category = data.get('category')

    if transaction_type not in ['income', 'expense']:
        return jsonify({"message": "Invalid transaction type"}), 400

    new_transaction = IncomeExpense(type=transaction_type, amount=amount, category=category, user_id=current_user)
    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201

# Get Transactions
@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user = get_jwt_identity()
    transactions = IncomeExpense.query.filter_by(user_id=current_user).all()

    if not transactions:
        return jsonify({"message": "No transactions found"}), 404

    results = []
    for transaction in transactions:
        results.append({
            'type': transaction.type,
            'amount': transaction.amount,
            'category': transaction.category,
            'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({"transactions": results})

# Update Transaction
@app.route('/transaction/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    transaction = IncomeExpense.query.filter_by(id=transaction_id, user_id=current_user).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    transaction.amount = data.get('amount', transaction.amount)
    transaction.category = data.get('category', transaction.category)
    db.session.commit()

    return jsonify({"message": "Transaction updated successfully"}), 200

# Delete Transaction
@app.route('/transaction/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    current_user = get_jwt_identity()
    transaction = IncomeExpense.query.filter_by(id=transaction_id, user_id=current_user).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted successfully"}), 200

# Monthly Summary (Income vs Expenses)
@app.route('/monthly-summary', methods=['GET'])
@jwt_required()
def monthly_summary():
    current_user = get_jwt_identity()

    # Get current month and year
    current_date = datetime.utcnow()
    start_of_month = datetime(current_date.year, current_date.month, 1)
    end_of_month = datetime(current_date.year, current_date.month + 1, 1) if current_date.month != 12 else datetime(current_date.year + 1, 1, 1)

    # Calculate totals for income and expenses
    income_total = db.session.query(db.func.sum(IncomeExpense.amount)).filter(
        IncomeExpense.user_id == current_user,
        IncomeExpense.type == 'income',
        IncomeExpense.date >= start_of_month,
        IncomeExpense.date < end_of_month
    ).scalar() or 0

    expense_total = db.session.query(db.func.sum(IncomeExpense.amount)).filter(
        IncomeExpense.user_id == current_user,
        IncomeExpense.type == 'expense',
        IncomeExpense.date >= start_of_month,
        IncomeExpense.date < end_of_month
    ).scalar() or 0

    remaining_savings = income_total - expense_total

    return jsonify({
        'income': income_total,
        'expenses': expense_total,
        'remaining_savings': remaining_savings
    })

# Run the app
if __name__ == '__main__':
    db.create_all()  # Creates the tables in the database
    app.run(debug=True)
