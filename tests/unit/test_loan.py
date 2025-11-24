import pytest
from src.personal_account import PersonalAccount


@pytest.fixture
def empty_account():
    return PersonalAccount("John", "Doe", "12345678901")


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
    def test_submit_for_loan(self, empty_account, history, loan_amount, expected_success, expected_balance):
        empty_account.history = history
        result = empty_account.submit_for_loan(loan_amount)

        assert result == expected_success
        assert empty_account.balance == expected_balance
