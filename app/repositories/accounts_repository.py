from abc import ABC, abstractmethod

class AccountsRepository(ABC):
    """Interfejs dla repozytoriów kont"""
    
    @abstractmethod
    def save_all(self, accounts):
        """Zapisz wszystkie konta do repozytorium"""
        pass
    
    @abstractmethod
    def load_all(self):
        """Załaduj wszystkie konta z repozytorium"""
        pass