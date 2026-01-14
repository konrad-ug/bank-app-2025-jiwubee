import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def api_url():
    """Fixture zwracający URL API"""
    return BASE_URL

@pytest.fixture
def sample_pesel():
    """Fixture z przykładowym PESELem"""
    return "92071512345"

class TestPeselUniqueness:
    
    def test_create_account_with_pesel(self, api_url, sample_pesel):
        """Test tworzenia konta z PESELem"""
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
    
    def test_duplicate_pesel_returns_409(self, api_url):
        """Test próby utworzenia konta z duplikatem PESELu - powinien zwrócić 409"""
        pesel = "85030198765"
        
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
    
    def test_create_account_without_pesel(self, api_url):
        """Test tworzenia konta bez PESELu - powinno być dozwolone"""
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
    
    def test_different_pesels_allowed(self, api_url):
        """Test tworzenia wielu kont z różnymi PESELami"""
        pesels = ["90010112345", "88020223456", "95030334567"]
        
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
    
    def test_pesel_released_after_account_deletion(self, api_url):
        """Test, że PESEL jest zwalniany po usunięciu konta"""
        pesel = "87110745612"
        
        # Utwórz konto
        response1 = requests.post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Tomasz Nowak',
                'balance': 3000,
                'pesel':  pesel
            }
        )
        assert response1.status_code == 201
        account_id = response1.json()['id']
        
        # Usuń konto
        delete_response = requests.delete(f"{api_url}/api/accounts/{account_id}")
        assert delete_response.status_code == 204
        
        # Spróbuj utworzyć nowe konto z tym samym PESELem
        response2 = requests. post(
            f"{api_url}/api/accounts",
            json={
                'name': 'Katarzyna Lewandowska',
                'balance': 2500,
                'pesel': pesel
            }
        )
        assert response2.status_code == 201
        assert response2.json()['pesel'] == pesel