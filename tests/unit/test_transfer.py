import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "12345678901")

@pytest.fixture
def company_account():
    return CompanyAccount("Kremówki SA", "1234567890")

class TestTransfer: 

    @pytest.mark.parametrize(
        "amount,expected_balance",
        [
            (100, 100),
            (250, 250),
        ]
    )
    def test_incoming_transfer(self, personal_account, amount, expected_balance):
        personal_account.incoming_transfer(amount)
        assert personal_account.balance == expected_balance

    @pytest.mark.parametrize(
        "initial_balance,amount,expected_balance",
        [
            (105, 100, 5),
            (80, 100, 80),
        ]
    )
    def test_outgoing_transfer(self, personal_account, initial_balance, amount, expected_balance):
        personal_account.balance = initial_balance
        personal_account.outgoing_transfer(amount)
        assert personal_account. balance == expected_balance

    @pytest.mark.parametrize(
        "initial_balance,amount,expected_balance",
        [
            (101, 100, 0),     
            (90, 100, 90),    
            (100, 100, -1),  
        ]
    )
    def test_express_transfer_personal(self, personal_account, initial_balance, amount, expected_balance):
        personal_account.balance = initial_balance
        personal_account.express_transfer(amount)
        assert personal_account.balance == expected_balance

    @pytest.mark.parametrize(
        "initial_balance,amount,expected_balance",
        [
            (105, 100, 0),
            (50, 100, 50),
            (100, 100, -5),
        ]
    )
    def test_express_transfer_company(self, company_account, initial_balance, amount, expected_balance):
        company_account. balance = initial_balance
        company_account.express_transfer(amount)
        assert company_account. balance == expected_balance

    def test_express_transfer_returns_balance(self, personal_account):
        """Test że express_transfer zwraca balance"""
        personal_account.balance = 101
        result = personal_account.express_transfer(100)
        assert result == 0

class TestHistory:

    @pytest.mark.parametrize(
        "account_fixture,expected",
        [
            ("personal_account", [500, -300, -1]),
            ("company_account", [500, -300, -5]),
        ]
    )
    def test_history_records(self, request, account_fixture, expected):
        account = request.getfixturevalue(account_fixture)
        account.incoming_transfer(500)
        account.express_transfer(300)
        assert account.history == expected

    def test_incoming_transfer_adds_to_history(self, personal_account):
        """Test że incoming_transfer dodaje do historii"""
        personal_account.incoming_transfer(100)
        assert 100 in personal_account.history

    def test_outgoing_transfer_adds_to_history(self, personal_account):
        """Test że outgoing_transfer dodaje do historii"""
        personal_account.balance = 200
        personal_account.outgoing_transfer(50)
        assert -50 in personal_account.history