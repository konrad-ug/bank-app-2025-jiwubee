import pytest

BASE_URL = "http://localhost:5000"

@pytest. fixture(scope="module")
def api_url():
    """Fixture zwracający URL API"""
    return BASE_URL

def test_create_account(api_url, mocker):
    """Test tworzenia nowego konta"""
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        'id': 1,
        'name': 'Jan Kowalski',
        'balance': 1000
    }
    
    mocker.patch("requests.post", return_value=mock_response)
    
    import requests
    response = requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Jan Kowalski', 'balance': 1000}
    )
    
    assert response.status_code == 201
    data = response. json()
    assert 'id' in data
    assert data['name'] == 'Jan Kowalski'
    assert data['balance'] == 1000

def test_get_all_accounts(api_url, mocker):
    """Test pobierania wszystkich kont"""
    mock_post = mocker.Mock()
    mock_post.status_code = 201
    
    mock_get = mocker.Mock()
    mock_get.status_code = 200
    mock_get.json.return_value = [
        {'id': 1, 'name': 'Anna Nowak', 'balance': 500}
    ]
    
    import requests
    mocker.patch("requests.post", return_value=mock_post)
    mocker.patch("requests.get", return_value=mock_get)
    
    # Najpierw utwórz konto
    requests.post(
        f"{api_url}/api/accounts",
        json={'name': 'Anna Nowak', 'balance':  500}
    )
    
    response = requests.get(f"{api_url}/api/accounts")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_account_by_id(api_url, mocker):
    """Test pobierania konta po ID"""
    mock_post = mocker.Mock()
    mock_post.status_code = 201
    mock_post.json.return_value = {'id': 123, 'name': 'Piotr Wiśniewski', 'balance': 2000}
    
    mock_get = mocker.Mock()
    mock_get.status_code = 200
    mock_get.json.return_value = {'id': 123, 'name': 'Piotr Wiśniewski', 'balance': 2000}
    
    import requests
    mocker.patch("requests.post", return_value=mock_post)
    mocker.patch("requests. get", return_value=mock_get)
    
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

def test_get_account_not_found(api_url, mocker):
    """Test pobierania nieistniejącego konta"""
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response. json.return_value = {'error': 'Account not found'}
    
    mocker.patch("requests.get", return_value=mock_response)
    
    import requests
    response = requests.get(f"{api_url}/api/accounts/9999")
    
    assert response.status_code == 404
    assert 'error' in response.json()

def test_update_account(api_url, mocker):
    """Test aktualizacji konta"""
    mock_post = mocker.Mock()
    mock_post.status_code = 201
    mock_post. json.return_value = {'id': 456, 'name': 'Maria Kowalczyk', 'balance': 1500}
    
    mock_put = mocker.Mock()
    mock_put.status_code = 200
    mock_put.json.return_value = {'id': 456, 'name': 'Maria Nowak-Kowalczyk', 'balance': 2500}
    
    import requests
    mocker.patch("requests.post", return_value=mock_post)
    mocker.patch("requests.put", return_value=mock_put)
    
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
    data = response.json()
    assert data['name'] == 'Maria Nowak-Kowalczyk'
    assert data['balance'] == 2500

def test_update_account_not_found(api_url, mocker):
    """Test aktualizacji nieistniejącego konta"""
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    
    mocker.patch("requests. put", return_value=mock_response)
    
    import requests
    response = requests.put(
        f"{api_url}/api/accounts/9999",
        json={'name': 'Test', 'balance': 100}
    )
    
    assert response.status_code == 404

def test_delete_account(api_url, mocker):
    """Test usuwania konta"""
    mock_post = mocker.Mock()
    mock_post.status_code = 201
    mock_post.json.return_value = {'id': 789, 'name': 'To Delete', 'balance': 100}
    
    mock_delete = mocker.Mock()
    mock_delete.status_code = 200
    mock_delete. json.return_value = {'message': 'Account deleted'}
    
    import requests
    mocker.patch("requests.post", return_value=mock_post)
    mocker.patch("requests.delete", return_value=mock_delete)
    
    # Utwórz konto
    create_response = requests. post(
        f"{api_url}/api/accounts",
        json={'name': 'To Delete', 'balance': 100}
    )
    account_id = create_response.json()['id']
    
    # Usuń konto
    response = requests.delete(f"{api_url}/api/accounts/{account_id}")
    
    assert response.status_code == 200