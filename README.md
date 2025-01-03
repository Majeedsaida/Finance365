# Finance365 API Testing Documentation

Welcome to the Finance365 Application Programming Interface (API). This documentation provides the necessary steps to test the API endpoints. The API includes routes for managing income, expenses, categories, and authentication.

## 1. **GET Routes - Testing in the Browser**

### Home Route
- **URL**: `http://localhost:5000/`
- **Expected Response**:
```json
{
  "message": "Welcome to Finance365! Your Personal Finance Management System"
}
```

### View Income Records
- **URL**: `http://localhost:5000/income`
- **Expected Response**:
```json
{
  "income_records": []
}
```

### View Expense Records
- **URL**: `http://localhost:5000/expense`
- **Expected Response**:
```json
{
  "expense_records": []
}
```

### Report Route
- **URL**: `http://localhost:5000/report`
- **Expected Response**:
```json
{
    "summary": {
        "total_income": 5000.0,
        "total_expenses": 3000.0,
        "remaining_savings": 2000.0
    },
    "details": {
        "expense_breakdown": [
            {"category": "Food", "total": 1000.0},
            {"category": "Rent", "total": 1000.0},
            {"category": "Transport", "total": 500.0}
        ],
        "financial_status": "Your finances are in good shape! You have saved money this period."
    },
    "message": "This report provides a detailed overview of your financial health for the month 01."
}

```

### View Categories
- **URL**: `http://localhost:5000/category`
- **Expected Response**:
```json
{
    "expense_categories": [
        {"category": "transportation", "total_expense": 150.0},
        {"category": "food", "total_expense": 300.0}
    ],
    "categories_expenses": {
        "transportation": [
            {
                "id": 1,
                "amount": 50.0,
                "category": "transportation",
                "description": "Taxi fare",
                "date": "2024-01-01"
            },
            {
                "id": 2,
                "amount": 100.0,
                "category": "transportation",
                "description": "Bus fare",
                "date": "2024-01-02"
            }
        ],
        "food": [
            {
                "id": 3,
                "amount": 50.0,
                "category": "food",
                "description": "Lunch",
                "date": "2024-01-03"
            },
            {
                "id": 4,
                "amount": 250.0,
                "category": "food",
                "description": "Dinner",
                "date": "2024-01-03"
            }
        ]
    },
    "message": "This is a detailed categorization of your expenses."
}
```

## 2. **Non-GET Routes - Testing with Postman or Curl**

### Add Income
- **Method**: POST
- **URL**: `http://localhost:5000/income`
- **Body** (JSON):
```json
{
  "id": 1,
  "source": "Salary",
  "amount": 2000,
  "date": "2025-01-01",
  "category": "Salary"
}
```
- **Expected Response**:
```json
{
  "message": "Income added successfully",
  "data": {
    "id": 1,
    "source": "Salary",
    "amount": 2000,
    "date": "2025-01-01",
    "category": "Salary"
  }
}
```

### Update Income
- **Method**: PUT
- **URL**: `http://localhost:5000/income`
- **Body** (JSON):
```json
{
  "id": 1,
  "source": "Salary",
  "amount": 2500,
  "date": "2025-01-01",
  "category": "Salary"
}
```
- **Expected Response**:
```json
{
  "message": "Income record updated",
  "data": {
    "id": 1,
    "source": "Salary",
    "amount": 2500,
    "date": "2025-01-01",
    "category": "Salary"
  }
}
```

### Delete Income
- **Method**: DELETE
- **URL**: `http://localhost:5000/income?id=1`
- **Expected Response**:
```json
{
  "message": "Income record deleted"
}
```

### Add Expense
- **Method**: POST
- **URL**: `http://localhost:5000/expense`
- **Body** (JSON):
```json
{
  "id": 1,
  "category": "Food",
  "amount": 50,
  "date": "2025-01-01"
}
```
- **Expected Response**:
```json
{
  "message": "Expense added successfully",
  "data": {
    "id": 1,
    "category": "Food",
    "amount": 50,
    "date": "2025-01-01"
  }
}
```

### Add New Category
- **Method**: POST
- **URL**: `http://localhost:5000/category`
- **Body** (JSON):
```json
{
  "name": "Healthcare"
}
```
- **Expected Response**:
```json
{
  "message": "Category added",
  "categories": ["Food", "Rent", "Entertainment", "Utilities", "Others", "Healthcare"]
}
```

## 3. **Authentication Routes - Register and Login**

### Register User
- **Method**: POST
- **URL**: `http://localhost:5000/register`
- **Body** (JSON):
```json
{
  "username": "john_doe",
  "password": "password123"
}
```
- **Expected Response**:
```json
{
  "message": "User registered successfully"
}
```

### Login User
- **Method**: POST
- **URL**: `http://localhost:5000/login`
- **Body** (JSON):
```json
{
  "username": "john_doe",
  "password": "password123"
}
```
- **Expected Response**:
```json
{
  "access_token": "your_jwt_token_here"
}
```

## 4. **Quick Testing Using Curl**

### Add Income Example:
```bash
curl -X POST http://localhost:5000/income -H "Content-Type: application/json" -d '{"id": 1, "source": "Salary", "amount": 2000, "date": "2025-01-01", "category": "Salary"}'
```

### Delete Income Example:
```bash
curl -X DELETE "http://localhost:5000/income?id=1"
```

### Add New Category Example:
```bash
curl -X POST http://localhost:5000/category -H "Content-Type: application/json" -d '{"name": "Healthcare"}'
```

### Register User Example:
```bash
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username": "john_doe", "password": "password123"}'
```

### Login User Example:
```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username": "john_doe", "password": "password123"}'
```

---

### Summary:
- **GET** requests can be tested directly in the browser for routes like `/`, `/income`, `/expense`, `/report`, and `/category`.
- **POST**, **PUT**, and **DELETE** requests should be tested using Postman or `curl` with the appropriate JSON payloads.
- **Authentication** routes (`/register`, `/login`) are available for user management with JWT-based authentication.