from behave import *
import requests

URL = "http://localhost:5000"

@step('Account with pesel "{pesel}" has balance: "{balance}"')
def set_account_balance(context, pesel, balance):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    
    account_id = None
    for account in accounts:
        if account.get('pesel') == pesel:
            account_id = account['id']
            break
    
    assert account_id is not None, f"Account with pesel {pesel} not found"
    
    json_body = {"balance": int(balance)}
    response = requests.put(URL + f"/api/accounts/{account_id}", json=json_body)
    assert response.status_code == 200

@when('I transfer "{amount}" from account "{from_pesel}" to account "{to_pesel}"')
def transfer_money(context, amount, from_pesel, to_pesel):
    json_body = {
        "amount": int(amount),
        "type": "outgoing"
    }
    response = requests.post(URL + f"/api/accounts/{from_pesel}/transfer", json=json_body)
    context.last_transfer_response = response
    assert response.status_code == 200, f"Outgoing transfer failed: {response.text}"
    
    json_body = {
        "amount": int(amount),
        "type": "incoming"
    }
    response = requests.post(URL + f"/api/accounts/{to_pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Incoming transfer failed: {response.text}"

@when('I attempt to transfer "{amount}" from account "{from_pesel}" to account "{to_pesel}"')
def attempt_transfer_money(context, amount, from_pesel, to_pesel):
    json_body = {
        "amount": int(amount),
        "type": "outgoing"
    }
    response = requests.post(URL + f"/api/accounts/{from_pesel}/transfer", json=json_body)
    context.last_transfer_response = response

@then('Transfer should fail with error "{error_message}"')
def check_transfer_error(context, error_message):
    assert context.last_transfer_response.status_code in [400, 404, 422], \
        f"Expected error status code, got {context.last_transfer_response.status_code}"
    
    try:
        error_data = context.last_transfer_response.json()
        error_text = error_data.get("error", "").lower()
        assert error_message.lower() in error_text, \
            f"Expected error message containing '{error_message}', got '{error_text}'"
    except:
        if "not found" in error_message.lower():
            assert context.last_transfer_response.status_code == 404
        elif "insufficient" in error_message.lower():
            assert context.last_transfer_response.status_code == 422

@when('I make express transfer of "{amount}" from account "{pesel}"')
def express_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "express"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.last_transfer_response = response
    assert response.status_code == 200, f"Express transfer failed: {response.text}"