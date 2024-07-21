from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Dummy data for expenses
expenses = [
    {
        'id': 1,
        'title': 'Lunch',
        'amount': 10.5,
        'date': '2022-01-01',
        'category': 'Food'
    },
    {
        'id': 2,
        'title': 'Clothes',
        'amount': 50.0,
        'date': '2022-01-02',
        'category': 'Clothing'
    }
]

# Get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

# Get a specific expense
@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = next((expense for expense in expenses if expense['id'] == expense_id), None)
    if expense:
        return jsonify(expense)
    else:
        return jsonify({'message': 'Expense not found'}), 404

# Create a new expense
@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    # Validate the input data
    if 'title' not in data or 'amount' not in data or 'date' not in data or 'category' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    if float(data['amount']) < 0:
        return jsonify({'message': 'Amount cannot be negative'}), 400
    if data['category'] not in ['Food', 'Clothing', 'Housing', 'Transportation']:
        return jsonify({'message': 'Invalid category'}), 400
    # Add the new expense to the list
    new_expense = {
        'id': len(expenses) + 1,
        'title': data['title'],
        'amount': float(data['amount']),
        'date': data['date'],
        'category': data['category']
    }
    expenses.append(new_expense)
    return jsonify(new_expense), 201

# Update an existing expense
@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = next((expense for expense in expenses if expense['id'] == expense_id), None)
    if expense:
        data = request.get_json()
        # Validate the input data
        if 'title' in data:
            expense['title'] = data['title']
        if 'amount' in data:
            if data['amount'] < 0:
                return jsonify({'message': 'Amount cannot be negative'}), 400
            expense['amount'] = data['amount']
        if 'date' in data:
            expense['date'] = data['date']
        if 'category' in data:
            if data['category'] not in ['Food', 'Clothing', 'Housing', 'Transportation']:
                return jsonify({'message': 'Invalid category'}), 400
            expense['category'] = data['category']
        return jsonify(expense)
    else:
        return jsonify({'message': 'Expense not found'}), 404

# Delete an expense
@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = next((expense for expense in expenses if expense['id'] == expense_id), None)
    if expense:
        expenses.remove(expense)
        return jsonify({'message': 'Expense deleted'})
    else:
        return jsonify({'message': 'Expense not found'}), 404

if __name__ == '__main__':
    app.run()