import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def api_url():
    """Fixture zwracający URL API"""
    return BASE_URL

def test_create_account(api_url):
    """Test tworzenia nowego konta"""
    response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Jan Kowalski', 'balance': 1000}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['name'] == 'Jan Kowalski'
    assert data['balance'] == 1000

def test_get_all_accounts(api_url):
    """Test pobierania wszystkich kont"""
    # Najpierw utwórz konto
    requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Anna Nowak', 'balance': 500}
    )
    
    response = requests.get(f"{api_url}/api/accounts")
    
    assert response.status_code == 200
    data = response. json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_account_by_id(api_url):
    """Test pobierania konta po ID"""
    # Utwórz konto
    create_response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Piotr Wiśniewski', 'balance': 2000}
    )
    account_id = create_response.json()['id']
    
    # Pobierz konto
    response = requests.get(f"{api_url}/api/accounts/{account_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == account_id
    assert data['name'] == 'Piotr Wiśniewski'
    assert data['balance'] == 2000

def test_get_account_not_found(api_url):
    """Test pobierania nieistniejącego konta"""
    response = requests.get(f"{api_url}/api/accounts/9999")
    
    assert response.status_code == 404
    assert 'error' in response.json()

def test_update_account(api_url):
    """Test aktualizacji konta"""
    # Utwórz konto
    create_response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Maria Kowalczyk', 'balance': 1500}
    )
    account_id = create_response.json()['id']
    
    # Zaktualizuj konto
    response = requests.put(
        f"{api_url}/api/accounts/{account_id}",
        json={'name': 'Maria Nowak-Kowalczyk', 'balance': 2500}
    )
    
    assert response.status_code == 200
    data = response. json()
    assert data['name'] == 'Maria Nowak-Kowalczyk'
    assert data['balance'] == 2500

def test_update_account_not_found(api_url):
    """Test aktualizacji nieistniejącego konta"""
    response = requests.put(
        f"{api_url}/api/accounts/9999",
        json={'name': 'Test', 'balance': 100}
    )
    
    assert response.status_code == 404

def test_delete_account(api_url):
    """Test usuwania konta"""
    # Utwórz konto
    create_response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Tomasz Zieliński', 'balance': 3000}
    )
    account_id = create_response.json()['id']
    
    # Usuń konto
    response = requests.delete(f"{api_url}/api/accounts/{account_id}")
    
    assert response.status_code == 204
    
    # Sprawdź czy konto zostało usunięte
    get_response = requests.get(f"{api_url}/api/accounts/{account_id}")
    assert get_response.status_code == 404

def test_delete_account_not_found(api_url):
    """Test usuwania nieistniejącego konta"""
    response = requests. delete(f"{api_url}/api/accounts/9999")
    
    assert response.status_code == 404

def test_deposit(api_url):
    """Test wpłaty na konto"""
    # Utwórz konto
    create_response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Katarzyna Lewandowska', 'balance':  1000}
    )
    account_id = create_response.json()['id']
    
    # Wpłać pieniądze
    response = requests.post(
        f"{api_url}/api/accounts/{account_id}/deposit",
        json={'amount': 500}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['balance'] == 1500

def test_deposit_invalid_amount(api_url):
    """Test wpłaty nieprawidłowej kwoty"""
    # Utwórz konto
    create_response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Test User', 'balance': 1000}
    )
    account_id = create_response.json()['id']
    
    # Próba wpłaty ujemnej kwoty
    response = requests.post(
        f"{api_url}/api/accounts/{account_id}/deposit",
        json={'amount': -100}
    )
    
    assert response.status_code == 400

def test_withdraw(api_url):
    """Test wypłaty z konta"""
    # Utwórz konto
    create_response = requests. post(
        f"{api_url}/api/accounts",
        json={'name': 'Paweł Wójcik', 'balance': 2000}
    )
    account_id = create_response.json()['id']
    
    # Wypłać pieniądze
    response = requests.post(
        f"{api_url}/api/accounts/{account_id}/withdraw",
        json={'amount': 500}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['balance'] == 1500

def test_withdraw_insufficient_funds(api_url):
    """Test wypłaty przy niewystarczających środkach"""
    # Utwórz konto
    create_response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Test User 2', 'balance': 100}
    )
    account_id = create_response.json()['id']
    
    # Próba wypłaty większej kwoty niż dostępne środki
    response = requests.post(
        f"{api_url}/api/accounts/{account_id}/withdraw",
        json={'amount': 500}
    )
    
    assert response.status_code == 400
    assert 'error' in response.json()

def test_create_account_without_name(api_url):
    """Test tworzenia konta bez nazwy"""
    response = requests.post(
        f"{api_url}/api/accounts",
        json={'balance': 1000}
    )
    
    assert response.status_code == 400
    assert 'error' in response.json()