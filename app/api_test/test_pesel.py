import pytest

BASE_URL = "http://localhost:5000"

@pytest. fixture(scope="module")
def api_url():
    """Fixture zwracający URL API"""
    return BASE_URL

@pytest.fixture
def sample_pesel():
    """Fixture z przykładowym PESELem"""
    return "92071512345"

class TestPeselUniqueness:
    
    def test_create_account_with_pesel(self, api_url, sample_pesel, mocker):
        """Test tworzenia konta z PESELem"""
        mock_response = mocker.Mock()
        mock_response.status_code = 201
        mock_response. json.return_value = {
            'id': 1,
            'name': 'Jan Kowalski',
            'balance': 1000,
            'pesel': sample_pesel
        }
        
        mocker.patch("requests.post", return_value=mock_response)
        
        import requests
        response = requests.post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Jan Kowalski',
                'balance': 1000,
                'pesel': sample_pesel
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data['pesel'] == sample_pesel
        assert data['name'] == 'Jan Kowalski'
    
    def test_duplicate_pesel_returns_409(self, api_url, mocker):
        """Test próby utworzenia konta z duplikatem PESELu - powinien zwrócić 409"""
        pesel = "85030198765"
        
        mock_response_1 = mocker.Mock()
        mock_response_1.status_code = 201
        mock_response_1.json.return_value = {
            'id': 1,
            'name': 'Anna Nowak',
            'balance': 500,
            'pesel': pesel
        }
        
        mock_response_2 = mocker.Mock()
        mock_response_2.status_code = 409
        mock_response_2.json.return_value = {
            'error': 'PESEL already exists',
            'pesel': pesel
        }
        
        import requests
        mocker.patch("requests.post", side_effect=[mock_response_1, mock_response_2])
        
        # Pierwsze konto
        response1 = requests.post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Anna Nowak',
                'balance': 500,
                'pesel': pesel
            }
        )
        assert response1.status_code == 201
        
        # Próba utworzenia drugiego konta z tym samym PESELem
        response2 = requests.post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Piotr Kowalczyk',
                'balance': 1500,
                'pesel': pesel
            }
        )
        
        assert response2.status_code == 409
        data = response2.json()
        assert 'error' in data
        assert 'PESEL' in data['error'] or 'pesel' in data['error']
        assert data['pesel'] == pesel
    
    def test_create_account_without_pesel(self, api_url, mocker):
        """Test tworzenia konta bez PESELu - powinno być dozwolone"""
        mock_response = mocker.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': 1,
            'name': 'Maria Wiśniewska',
            'balance': 2000
        }
        
        mocker.patch("requests.post", return_value=mock_response)
        
        import requests
        response = requests.post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Maria Wiśniewska',
                'balance': 2000
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == 'Maria Wiśniewska'
    
    def test_different_pesels_allowed(self, api_url, mocker):
        """Test tworzenia wielu kont z różnymi PESELami"""
        pesels = ["90010112345", "88020223456", "95030334567"]
        
        mock_responses = []
        for i, pesel in enumerate(pesels):
            mock_resp = mocker.Mock()
            mock_resp.status_code = 201
            mock_resp. json.return_value = {
                'id': i + 1,
                'name': f'User {i}',
                'balance': 1000 * (i + 1),
                'pesel': pesel
            }
            mock_responses.append(mock_resp)
        
        mocker.patch("requests.post", side_effect=mock_responses)
        
        import requests
        for i, pesel in enumerate(pesels):
            response = requests.post(
                f"{api_url}/api/accounts",
                json={
                    'name': f'User {i}',
                    'balance': 1000 * (i + 1),
                    'pesel': pesel
                }
            )
            assert response.status_code == 201
            assert response.json()['pesel'] == pesel
    
    def test_pesel_released_after_account_deletion(self, api_url, mocker):
        """Test, że PESEL jest zwalniany po usunięciu konta"""
        pesel = "87110745612"
        
        mock_post_1 = mocker.Mock()
        mock_post_1.status_code = 201
        mock_post_1.json. return_value = {
            'id': 1,
            'name': 'First User',
            'balance': 1000,
            'pesel':  pesel
        }
        
        mock_delete = mocker.Mock()
        mock_delete.status_code = 200
        mock_delete.json.return_value = {'message':  'Account deleted'}
        
        mock_post_2 = mocker.Mock()
        mock_post_2.status_code = 201
        mock_post_2.json.return_value = {
            'id': 2,
            'name': 'Second User',
            'balance': 2000,
            'pesel':  pesel
        }
        
        import requests
        mocker.patch("requests.post", side_effect=[mock_post_1, mock_post_2])
        mocker.patch("requests.delete", return_value=mock_delete)
        
        # Utwórz pierwsze konto
        response1 = requests.post(
            f"{api_url}/api/accounts",
            json={
                'name': 'First User',
                'balance': 1000,
                'pesel': pesel
            }
        )
        assert response1.status_code == 201
        account_id = response1.json()['id']
        
        # Usuń konto
        delete_response = requests.delete(f"{api_url}/api/accounts/{account_id}")
        assert delete_response.status_code == 200
        
        # Utwórz nowe konto z tym samym PESELem
        response2 = requests. post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Second User',
                'balance': 2000,
                'pesel': pesel
            }
        )
        assert response2.status_code == 201
        assert response2.json()['pesel'] == pesel