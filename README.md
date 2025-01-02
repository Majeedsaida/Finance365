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

#### View Income Records
- URL: `http://localhost:5000/income`
- Expected Response:
```json
{
  "income_records": []
}
```

#### View Expense Records
- URL: `http://localhost:5000/expense`
- Expected Response:
```json
{
  "expense_records": []
}
```

#### Report Route
- URL: `http://localhost:5000/report`
- Expected Response:
```json
{
  "total_income": 0,
  "total_expenses": 0,
  "remaining_savings": 0
}
```

#### View Categories
- URL: `http://localhost:5000/category`
- Expected Response:
```json
{
  "categories": ["Food", "Rent", "Entertainment", "Utilities", "Others"]
}
```

### 2. **Testing Non-GET Routes Using Postman**

#### Add Income
1. **Method**: POST  
2. **URL**: `http://localhost:5000/income`  
3. **Body** (JSON):
   ```json
   {
       "id": 1,
       "source": "Salary",
       "amount": 2000,
       "date": "2025-01-01"
   }
   ```
4. **Expected Response**:
   ```json
   {
       "message": "Income added successfully",
       "data": {
           "id": 1,
           "source": "Salary",
           "amount": 2000,
           "date": "2025-01-01"
       }
   }
   ```

#### Update Income
1. **Method**: PUT  
2. **URL**: `http://localhost:5000/income`  
3. **Body** (JSON):
   ```json
   {
       "id": 1,
       "source": "Salary",
       "amount": 2500,
       "date": "2025-01-01"
   }
   ```
4. **Expected Response**:
   ```json
   {
       "message": "Income record updated",
       "data": {
           "id": 1,
           "source": "Salary",
           "amount": 2500,
           "date": "2025-01-01"
       }
   }
   ```

#### Delete Income
1. **Method**: DELETE  
2. **URL**: `http://localhost:5000/income?id=1`  
3. **Expected Response**:
   ```json
   {
       "message": "Income record deleted"
   }
   ```

#### Add Expense
1. **Method**: POST  
2. **URL**: `http://localhost:5000/expense`  
3. **Body** (JSON):
   ```json
   {
       "id": 1,
       "category": "Food",
       "amount": 50,
       "date": "2025-01-01"
   }
   ```
4. **Expected Response**:
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

#### Add New Category
1. **Method**: POST  
2. **URL**: `http://localhost:5000/category`  
3. **Body** (JSON):
   ```json
   {
       "name": "Healthcare"
   }
   ```
4. **Expected Response**:
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