import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "12345678901")

@pytest.fixture
def company_account():
    return CompanyAccount("Kremówki SA", "1234567890")

class TestLoan:

    @pytest.mark.parametrize(
        "history,loan_amount,expected_success,expected_balance",
        [
            ([100, 50, 300], 100, True, 100),
            ([100, 50, 300, -50, -100], 100, True, 100),
            ([100, 50], 100, False, 0),
            ([100, 50, -50, 200, -250], 100, False, 0),
        ]
    )
    def test_submit_for_loan(self, personal_account, history, loan_amount, expected_success, expected_balance):
        personal_account.history = history
        result = personal_account.submit_for_loan(loan_amount)

        assert result == expected_success
        assert personal_account.balance == expected_balance

class TestCompanyLoan: 
    @pytest.mark.parametrize(
        "balance, history, loan_amount, expected_result, expected_balance",
        [
            (4000, [-100, -1775, 300], 1500, True, 5500),
            (4000, [100, -1000, 300], 1500, False, 4000),
            (2500, [-1775, 500, -200], 1500, False, 2500),
            (1000, [200, 100, 300], 1500, False, 1000),
            # Dodatkowe przypadki testowe
            (3000, [-1775], 1500, True, 4500),  # dokładnie 2x amount
        ]
    )
    def test_take_loan(self, company_account, balance, history, loan_amount, expected_result, expected_balance):
        company_account.balance = balance
        company_account.history = history
        result = company_account.take_loan(loan_amount)
        assert result == expected_result
        assert company_account.balance == expected_balance

    def test_company_loan_updates_balance_correctly(self, company_account):
        """Test że pożyczka firmowa poprawnie aktualizuje balance"""
        company_account.balance = 4000
        company_account.history = [-1775, 100]
        initial_balance = company_account.balance
        loan_amount = 1500
        
        result = company_account.take_loan(loan_amount)
        
        assert result is True
        assert company_account. balance == initial_balance + loan_amount