import pytest
from ..app.repositories.mongo_accounts_repository import MongoAccountsRepository

class TestMongoAccountsRepository:
    
    @pytest.fixture
    def sample_accounts(self):
        """Przykładowe konta do testów"""
        return [
            {
                'id': 1,
                'name': 'Jan',
                'surname': 'Kowalski',
                'pesel': '90010112345',
                'balance': 1000
            },
            {
                'id': 2,
                'name': 'Anna',
                'surname': 'Nowak',
                'pesel': '85050567890',
                'balance': 500
            }
        ]
    
    def test_save_all_with_mock(self, mocker, sample_accounts):
        """Test save_all z użyciem mocka"""
        # Mockowanie kolekcji MongoDB
        mock_collection = mocker.Mock()
        
        # Tworzenie repozytorium z mockiem
        repo = MongoAccountsRepository()
        repo._collection = mock_collection
        
        # Wywołanie save_all
        repo.save_all(sample_accounts)
        
        # Sprawdzenie czy delete_many zostało wywołane
        mock_collection.delete_many.assert_called_once_with({})
        
        # Sprawdzenie czy update_one zostało wywołane dla każdego konta
        assert mock_collection.update_one.call_count == len(sample_accounts)
        
        # Sprawdzenie argumentów pierwszego wywołania
        first_call_args = mock_collection.update_one.call_args_list[0]
        assert first_call_args[0][0] == {"pesel": "90010112345"}
        assert first_call_args[1]["upsert"] == True
    
    def test_load_all_with_mock(self, mocker, sample_accounts):
        """Test load_all z użyciem mocka"""
        # Mockowanie kolekcji MongoDB
        mock_collection = mocker.Mock()
        
        # Dodanie _id do danych (jak MongoDB)
        accounts_with_id = []
        for acc in sample_accounts:
            acc_copy = acc.copy()
            acc_copy['_id'] = mocker.Mock()
            accounts_with_id.append(acc_copy)
        
        mock_collection.find.return_value = accounts_with_id
        
        # Tworzenie repozytorium z mockiem
        repo = MongoAccountsRepository()
        repo._collection = mock_collection
        
        # Wywołanie load_all
        loaded = repo.load_all()
        
        # Sprawdzenie czy find zostało wywołane
        mock_collection.find.assert_called_once()
        
        # Sprawdzenie czy zwrócono odpowiednią liczbę kont
        assert len(loaded) == len(sample_accounts)
        
        # Sprawdzenie czy _id zostało usunięte
        for account in loaded:
            assert '_id' not in account
    
    def test_save_all_clears_collection(self, mocker):
        """Test czy save_all czyści kolekcję przed zapisem"""
        mock_collection = mocker.Mock()
        
        repo = MongoAccountsRepository()
        repo._collection = mock_collection
        
        repo.save_all([])
        
        # Sprawdzenie czy delete_many zostało wywołane
        mock_collection.delete_many.assert_called_once_with({})