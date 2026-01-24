from behave import *
import requests

URL = "http://localhost:5000"

@given('I save accounts to database')
@when('I save accounts to database')
@step('I save accounts to database')
def save_accounts_to_db(context):
    response = requests.post(URL + "/api/accounts/save")
    context.last_db_response = response
    print(f"Save response status: {response.status_code}")
    print(f"Save response body: {response.text}")

@given('I load accounts from database')
@when('I load accounts from database')
@step('I load accounts from database')
def load_accounts_from_db(context):
    response = requests.post(URL + "/api/accounts/load")
    context.last_db_response = response
    print(f"Load response status: {response.status_code}")
    print(f"Load response body: {response.text}")

@then('Save operation should succeed')
def check_save_success(context):
    response = context.last_db_response
    assert response.status_code == 200, \
        f"Expected status 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"].lower()

@then('Number of accounts saved should be "{count}"')
def check_saved_count(context, count):
    assert context.last_db_response.status_code == 200
    data = context.last_db_response.json()
    assert data.get("count") == int(count), \
        f"Expected {count} accounts saved, got {data.get('count')}"