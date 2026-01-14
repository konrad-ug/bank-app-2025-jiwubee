from flask import Flask, jsonify, request

app = Flask(__name__)

# Przechowywanie danych w pamięci
accounts = {}
next_account_id = 1
# Zbiór do śledzenia użytych PESELów
used_pesels = set()

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
    pesel = data.get('pesel')
    
    if not name:  
        return jsonify({"error": "Name is required"}), 400
    
    # Feature 16: Sprawdzenie unikalności PESELu
    if pesel: 
        if pesel in used_pesels:
            return jsonify({
                "error": "Account with this PESEL already exists",
                "pesel": pesel
            }), 409
        used_pesels.add(pesel)
    
    account = {
        'id': next_account_id,
        'name': name,
        'balance': balance,
        'pesel': pesel
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
        return jsonify({"error": "No data provided"}), 400
    
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
        return jsonify({"error": "Account not found"}), 404
    
    # Usuń PESEL z używanych
    pesel = accounts[account_id].get('pesel')
    if pesel and pesel in used_pesels:
        used_pesels.remove(pesel)
    
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

# Feature 17: Endpoint do przelewów
@app.route('/api/accounts/<string:pesel>/transfer', methods=['POST'])
def transfer(pesel):
    """Wykonaj przelew na/z konta"""
    # Znajdź konto po PESELu
    account = None
    account_id = None
    for acc_id, acc in accounts.items():
        if acc. get('pesel') == pesel:
            account = acc
            account_id = acc_id
            break
    
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    
    if not data: 
        return jsonify({"error": "No data provided"}), 400
    
    amount = data.get('amount')
    transfer_type = data.get('type')
    
    # Walidacja kwoty
    if amount is None: 
        return jsonify({"error": "Amount is required"}), 400
    
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error":  "Invalid amount"}), 400
    
    # Walidacja typu
    if transfer_type not in ['incoming', 'outgoing', 'express']:
        return jsonify({
            "error": "Invalid transfer type",
            "message": "Type must be one of: incoming, outgoing, express"
        }), 400
    
    # Wykonaj odpowiedni przelew
    if transfer_type == 'incoming':
        account['balance'] += amount
        return jsonify({
            "message": "Zlecenie przyjęto do realizacji",
            "account": account
        }), 200
    
    elif transfer_type == 'outgoing':
        if account['balance'] < amount: 
            return jsonify({
                "error": "Insufficient funds",
                "balance": account['balance'],
                "requested_amount": amount
            }), 422
        account['balance'] -= amount
        return jsonify({
            "message": "Zlecenie przyjęto do realizacji",
            "account":  account
        }), 200
    
    elif transfer_type == 'express':
        # Opłata za express to 1 dla kont osobistych (zakładamy domyślnie)
        express_fee = 1
        total_amount = amount + express_fee
        
        if account['balance'] < total_amount:
            return jsonify({
                "error": "Insufficient funds for express transfer",
                "balance":  account['balance'],
                "requested_amount": amount,
                "express_fee": express_fee,
                "total_required": total_amount
            }), 422
        
        account['balance'] -= total_amount
        return jsonify({
            "message": "Zlecenie przyjęto do realizacji",
            "account": account,
            "express_fee": express_fee
        }), 200

if __name__ == '__main__':  
    app.run(debug=True, port=5000)