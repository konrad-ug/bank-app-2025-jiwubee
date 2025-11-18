from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestLoan:
    def test_take_loan(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.history = [100, 50, 300]
        assert account.submit_for_loan(100) == True
        assert account.balance == 100
    def test_take_loan_five_transactions(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.history = [100, 50, 300, -50, -100]
        account.submit_for_loan(100) == True
        assert account.balance == 100
    def test_take_loan_not_enough_transactions(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.history = [100, 50]
        account.submit_for_loan(100)
        assert account.submit_for_loan(100) == False
        assert account.balance == 0
    def test_take_loan_not_enough_sum(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.history = [100, 50, -50, 200, -250]
        account.submit_for_loan(100)
        assert account.submit_for_loan(100) == False
        assert account.balance == 0