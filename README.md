Welcome to Finance365 Application Programming Interface

Below contains endpoint tests documentaion for the API consumers

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

### 3. **Using Curl for Quick Testing**

If you're using a terminal, you can use `curl` to test non-GET routes:

#### Add Income Example:
```bash
curl -X POST http://localhost:5000/income -H "Content-Type: application/json" -d '{"id": 1, "source": "Salary", "amount": 2000, "date": "2025-01-01"}'
```

#### Delete Income Example:
```bash
curl -X DELETE "http://localhost:5000/income?id=1"
```

#### Add New Category Example:
```bash
curl -X POST http://localhost:5000/category -H "Content-Type: application/json" -d '{"name": "Healthcare"}'
```

### Summary
- Use the browser for `GET` routes like `/`, `/income`, `/expense`, `/report`, and `/category`.
- Use Postman or `curl` for testing `POST`, `PUT`, and `DELETE` routes with the appropriate JSON payloads.
  
Let me know if you need assistance with automating these tests using a testing framework like `unittest`!