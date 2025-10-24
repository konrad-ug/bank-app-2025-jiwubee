from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.national_id == "12345678901"
    def test_account_invalid_national_id(self):
        too_long = Account("John", "Doe", "1234567890123")
        too_short = Account("John", "Doe", "123")
        invalid = Account("John", "Doe", "abc")
        assert too_long.national_id == "Invalid"
        assert too_short.national_id == "Invalid"
        assert invalid.national_id == "Invalid"
    def test_account_promo_code(self):
        valid_code = Account("John", "Doe", "87110745612", "PROM_XYZ")
        none_code = Account("John", "Doe", "12345678901")
        wrong_code = Account("John", "Doe", "12345678901", "PROMOXYZ")
        assert valid_code.balance == 50.0
        assert none_code.balance == 0.0
        assert wrong_code.balance == 0.0
    def test_age_validation(self):
        valid_age = Account("John", "Doe", "87110745612", "PROM_XYZ")
        invalid_age = Account("John", "Doe", "55031412347", "PROM_XYZ")
        assert valid_age.balance == 50.0
        assert invalid_age.balance == 0.0