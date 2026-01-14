from flask import Flask, jsonify, request

app = Flask(__name__)

# Przechowywanie danych w pamięci
accounts = {}
next_account_id = 1

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Pobierz wszystkie konta"""
    return jsonify(list(accounts.values())), 200

@app.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """Pobierz konto o danym ID"""
    if account_id not in accounts:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(accounts[account_id]), 200

@app.route('/api/accounts', methods=['POST'])
def create_account():
    """Utwórz nowe konto"""
    global next_account_id
    
    data = request.get_json()
    
    if not data: 
        return jsonify({"error": "No data provided"}), 400
    
    name = data.get('name')
    balance = data.get('balance', 0)
    
    if not name: 
        return jsonify({"error": "Name is required"}), 400
    
    account = {
        'id': next_account_id,
        'name': name,
        'balance':  balance
    }
    
    accounts[next_account_id] = account
    next_account_id += 1
    
    return jsonify(account), 201

@app.route('/api/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    """Zaktualizuj konto"""
    if account_id not in accounts:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    
    if not data: 
        return jsonify({"error":  "No data provided"}), 400
    
    account = accounts[account_id]
    
    if 'name' in data:
        account['name'] = data['name']
    if 'balance' in data: 
        account['balance'] = data['balance']
    
    return jsonify(account), 200

@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Usuń konto"""
    if account_id not in accounts: 
        return jsonify({"error":  "Account not found"}), 404
    
    del accounts[account_id]
    return '', 204

@app.route('/api/accounts/<int:account_id>/deposit', methods=['POST'])
def deposit(account_id):
    """Wpłata na konto"""
    if account_id not in accounts:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    amount = data.get('amount')
    
    if amount is None or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400
    
    accounts[account_id]['balance'] += amount
    return jsonify(accounts[account_id]), 200

@app.route('/api/accounts/<int:account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    """Wypłata z konta"""
    if account_id not in accounts: 
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    amount = data.get('amount')
    
    if amount is None or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400
    
    if accounts[account_id]['balance'] < amount:
        return jsonify({"error": "Insufficient funds"}), 400
    
    accounts[account_id]['balance'] -= amount
    return jsonify(accounts[account_id]), 200

if __name__ == '__main__': 
    app.run(debug=True, port=5000)