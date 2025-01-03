# Finance365 Application Programming Interface
## Project Overview
Finance360 is a comprehensive API designed to help users manage their personal finances in a secure and efficient way. It enables users to seamlessly track their income, categorize their expenses, and monitor their overall financial health. Whether you're budgeting, tracking spending habits, or looking to save more, Finance360 provides an intuitive and easy-to-use platform for managing all aspects of your financial life.

The system includes core features such as the ability to add, update, view, and delete income and expense records. Users can categorize their expenses into specific types—such as food, rent, entertainment, and more—and generate monthly summaries automatically. This gives users a clear and concise view of their financial situation and helps them stay on top of their spending habits.

![](https://mymagnifi.org/images/pfm.jpg)

## Below contains endpoint tests documentaion for the API consumers

To test the API routes in your browser or with tools like Postman, here are some steps you can follow for each endpoint. Since your browser primarily supports `GET` requests, we’ll focus on testing `GET` routes directly through the browser and demonstrate how you can use Postman or curl for `POST`, `PUT`, and `DELETE` requests.

### 1. **Testing the `GET` Routes in the Browser**

#### Home Route
- URL: `http://localhost:5000/`
- Expected Response: 
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


### Summary
- Use the browser for `GET` routes like `/`, `/income`, `/expense`, `/report`, and `/category`.
- Use Postman for testing `POST`, `PUT`, and `DELETE` routes with the appropriate JSON payloads.
  
  ## Collaborators
* Abdul-Majeed Saidatu
* Nyande Talatu

## Getting Started
``` bash
  First , fork this repository and then
  git clone https://github.com/Majeedsaida/Finance365.git
  ```
  ## Tech stack
  * Python
  * Flask
  * SQLite
  * Flask Routes