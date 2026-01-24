from pymongo import MongoClient
from .accounts_repository import AccountsRepository

class MongoAccountsRepository(AccountsRepository):
    """Repozytorium kont używające MongoDB"""
    
    def __init__(self, connection_string="mongodb://localhost:27017/", database_name="accounts_db"):
        """
        Inicjalizacja połączenia z MongoDB
        
        Args:
            connection_string: String połączenia do MongoDB
            database_name: Nazwa bazy danych
        """
        self._client = MongoClient(connection_string)
        self._db = self._client[database_name]
        self._collection = self._db["accounts"]
    
    def save_all(self, accounts):
        """
        Zapisz wszystkie konta do MongoDB
        Przed zapisem czyści kolekcję
        
        Args:
            accounts: Lista słowników z danymi kont
        """
        # Wyczyść kolekcję przed zapisem
        self._collection.delete_many({})
        
        # Zapisz wszystkie konta
        if accounts:
            for account in accounts:
                self._collection.update_one(
                    {"pesel": account.get("pesel")},
                    {"$set": account},
                    upsert=True
                )
    
    def load_all(self):
        """
        Załaduj wszystkie konta z MongoDB
        
        Returns:
            Lista słowników z danymi kont
        """
        accounts = []
        for doc in self._collection.find():
            # Usuń _id które dodaje MongoDB
            if '_id' in doc:
                del doc['_id']
            accounts.append(doc)
        return accounts
    
    def close(self):
        """Zamknij połączenie z MongoDB"""
        self._client.close()