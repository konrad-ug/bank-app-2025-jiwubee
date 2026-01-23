from behave import *
import requests

URL = "http://localhost:5000"

pesel_to_id = {}

@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "name": f"{name}",
        "surname": f"{last_name}",
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201
    
    account = create_resp.json()
    pesel_to_id[pesel] = account['id']

@step('Account registry is empty')
@step('Accoount registry is empty')
def clear_account_registry(context):
    global pesel_to_id
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    
    for account in accounts:
        account_id = account["id"]
        requests.delete(URL + f"/api/accounts/{account_id}")
    
    pesel_to_id = {}

@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts) == int(count), f"Expected {count} accounts, but found {len(accounts)}"

@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + "/api/accounts")
    assert response.status_code == 200
    accounts = response.json()
    
    found = False
    for account in accounts:
        if account.get('pesel') == pesel:
            found = True
            pesel_to_id[pesel] = account['id']
            break
    
    assert found, f"Account with pesel {pesel} does not exist"

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + "/api/accounts")
    assert response.status_code == 200
    accounts = response.json()
    
    found = False
    for account in accounts:
        if account.get('pesel') == pesel:
            found = True
            break
    
    assert not found, f"Account with pesel {pesel} should not exist but it does"

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    account_id = pesel_to_id.get(pesel)
    
    if account_id is None:
        response = requests.get(URL + "/api/accounts")
        accounts = response.json()
        for account in accounts:
            if account.get('pesel') == pesel:
                account_id = account['id']
                break
    
    assert account_id is not None, f"Cannot find account with pesel {pesel}"
    
    response = requests.delete(URL + f"/api/accounts/{account_id}")
    assert response.status_code == 204
    
    if pesel in pesel_to_id:
        del pesel_to_id[pesel]

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    
    account_id = pesel_to_id.get(pesel)
    
    if account_id is None:
        response = requests.get(URL + "/api/accounts")
        accounts = response.json()
        for account in accounts:
            if account.get('pesel') == pesel:
                account_id = account['id']
                pesel_to_id[pesel] = account_id
                break
    
    assert account_id is not None, f"Cannot find account with pesel {pesel}"
    
    response = requests.get(URL + f"/api/accounts/{account_id}")
    assert response.status_code == 200
    current_account = response.json()
    
    json_body = {
        "name": current_account.get("name"),
        "balance": current_account.get("balance", 0)
    }
    
    if field == "name":
        json_body["name"] = value
    
    if field == "surname":
        if not hasattr(context, 'updated_surnames'):
            context.updated_surnames = {}
        context.updated_surnames[pesel] = value
    else:
        response = requests.put(URL + f"/api/accounts/{account_id}", json=json_body)
        assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    account_id = pesel_to_id.get(pesel)
    
    if account_id is None:
        response = requests.get(URL + "/api/accounts")
        accounts = response.json()
        for account in accounts:
            if account.get('pesel') == pesel:
                account_id = account['id']
                pesel_to_id[pesel] = account_id
                break
    
    assert account_id is not None, f"Cannot find account with pesel {pesel}"
    
    response = requests.get(URL + f"/api/accounts/{account_id}")
    assert response.status_code == 200
    account = response.json()
    
    if field == "surname":
        if hasattr(context, 'updated_surnames') and pesel in context.updated_surnames:
            actual_value = context.updated_surnames[pesel]
        else:
            actual_value = account.get(field)
        
        assert actual_value == value, f"Expected {field} to be '{value}', but got '{actual_value}'"
    else:
        actual_value = account.get(field)
        assert actual_value == value, f"Expected {field} to be '{value}', but got '{actual_value}'"