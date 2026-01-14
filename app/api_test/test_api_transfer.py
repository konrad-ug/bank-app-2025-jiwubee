import pytest
import requests
import time

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="function")
def api_url():
    return BASE_URL

@pytest.fixture
def account_with_pesel(api_url):
    pesel = f"910506{int(time.time() * 1000) % 100000: 05d}"
    response = requests. post(
        f"{api_url}/api/accounts",
        json={
            'name': 'Test User',
            'balance':  1000,
            'pesel': pesel
        }
    )
    assert response.status_code == 201, f"Error:  {response.json()}"
    return response.json()

@pytest.fixture
def account_with_low_balance(api_url):
    pesel = f"890301{int(time.time() * 1000) % 100000:05d}"
    response = requests.post(
        f"{api_url}/api/accounts",
        json={
            'name': 'Poor User',
            'balance': 50,
            'pesel': pesel
        }
    )
    assert response.status_code == 201, f"Error: {response.json()}"
    return response.json()

@pytest.fixture
def account_with_high_balance(api_url):
    pesel = f"931207{int(time.time() * 1000) % 100000:05d}"
    response = requests.post(
        f"{api_url}/api/accounts",
        json={
            'name': 'Rich User',
            'balance': 10000,
            'pesel': pesel
        }
    )
    assert response.status_code == 201, f"Error: {response. json()}"
    return response. json()


class TestTransferAPI:
    
    def test_incoming_transfer_success(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        initial_balance = account_with_pesel['balance']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': 500,
                'type': 'incoming'
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == "Zlecenie przyjęto do realizacji"
        assert data['account']['balance'] == initial_balance + 500
    
    def test_outgoing_transfer_success(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        initial_balance = account_with_pesel['balance']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': 300,
                'type': 'outgoing'
            }
        )
        
        assert response.status_code == 200
        data = response. json()
        assert data['message'] == "Zlecenie przyjęto do realizacji"
        assert data['account']['balance'] == initial_balance - 300
    
    def test_outgoing_transfer_insufficient_funds(self, api_url, account_with_low_balance):
        pesel = account_with_low_balance['pesel']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount':  1000,
                'type': 'outgoing'
            }
        )
        
        assert response.status_code == 422
        data = response.json()
        assert 'error' in data
        assert 'Insufficient funds' in data['error']
    
    def test_express_transfer_success(self, api_url, account_with_high_balance):
        pesel = account_with_high_balance['pesel']
        initial_balance = account_with_high_balance['balance']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': 500,
                'type': 'express'
            }
        )
        
        assert response. status_code == 200
        data = response.json()
        assert data['message'] == "Zlecenie przyjęto do realizacji"
        assert data['account']['balance'] == initial_balance - 501
        assert data['express_fee'] == 1
    
    def test_express_transfer_insufficient_funds(self, api_url, account_with_low_balance):
        pesel = account_with_low_balance['pesel']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': 50,
                'type': 'express'
            }
        )
        
        assert response.status_code == 422
        data = response. json()
        assert 'error' in data
        assert 'Insufficient funds' in data['error']
    
    def test_transfer_account_not_found(self, api_url):
        response = requests.post(
            f"{api_url}/api/accounts/99999999999/transfer",
            json={
                'amount': 100,
                'type': 'incoming'
            }
        )
        
        assert response.status_code == 404
        data = response.json()
        assert 'error' in data
        assert 'not found' in data['error']. lower()
    
    def test_transfer_invalid_type(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': 100,
                'type': 'invalid_type'
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'Invalid transfer type' in data['error']
    
    def test_transfer_missing_amount(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        
        response = requests. post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'type': 'incoming'
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'Amount' in data['error']
    
    def test_transfer_negative_amount(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': -100,
                'type': 'incoming'
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'Invalid amount' in data['error']
    
    def test_transfer_zero_amount(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        
        response = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={
                'amount': 0,
                'type': 'outgoing'
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'Invalid amount' in data['error']
    
    def test_multiple_transfers_sequence(self, api_url, account_with_pesel):
        pesel = account_with_pesel['pesel']
        
        response1 = requests. post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={'amount': 200, 'type':  'incoming'}
        )
        assert response1.status_code == 200
        balance_after_incoming = response1.json()['account']['balance']
        
        response2 = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={'amount':  100, 'type': 'outgoing'}
        )
        assert response2.status_code == 200
        balance_after_outgoing = response2.json()['account']['balance']
        assert balance_after_outgoing == balance_after_incoming - 100
        
        response3 = requests.post(
            f"{api_url}/api/accounts/{pesel}/transfer",
            json={'amount': 50, 'type':  'express'}
        )
        assert response3.status_code == 200
        final_balance = response3.json()['account']['balance']
        assert final_balance == balance_after_outgoing - 51