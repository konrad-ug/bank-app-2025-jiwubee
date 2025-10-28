from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfer:
    def test_incoming_transfer(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        assert account.balance == 100
    def test_outgoing_transfer_sufficient(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 105
        account.outgoing_transfer(100)
        assert account.balance == 5
    def test_outgoing_transfer_insufficient(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 80
        account.outgoing_transfer(100)
        assert account.balance == 80
    
    def test_express_transer_personal(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 101
        account.express_transfer(100)
        assert account.balance == 0
    def test_express_transfer_personal_insufficient(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 90
        account.express_transfer(100)
        assert account.balance == 90
    def test_express_transfer_personal_negative(self): 
        account = PersonalAccount("John", "Doe", "12345678901")
        account.balance = 100
        account.express_transfer(100)
        assert account.balance == -1
    def test_express_transer_company(self):
        company_account = CompanyAccount("Kremówki SA", "1234567890")
        company_account.balance = 105
        company_account.express_transfer(100)
        assert company_account.balance == 0
    def test_express_transfer_company_insufficient(self):
        company_account = CompanyAccount("Kremówki SA", "1234567890")
        company_account.balance = 50
        company_account.express_transfer(100)
        assert company_account.balance == 50
    def test_express_transfer_company_negative(self):
        company_account = CompanyAccount("Kremówki SA", "1234567890")
        company_account.balance = 100
        company_account.express_transfer(100)
        assert company_account.balance == -5

class TestHistory:
    def test_personal_account_history(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming_transfer(500)
        account.express_transfer(300)
        assert account.history == [500, -300, -1]
    def test_company_account_history(self):
        account = CompanyAccount("Kremówki SA", "1234567890")
        account.incoming_transfer(500)
        account.express_transfer(300)
        assert account.history == [500, -300, -5]

