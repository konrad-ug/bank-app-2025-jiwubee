from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestPersonalAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.national_id == "12345678901"
    def test_account_invalid_national_id(self):
        too_long = PersonalAccount("John", "Doe", "1234567890123")
        too_short = PersonalAccount("John", "Doe", "123")
        invalid = PersonalAccount("John", "Doe", "abc")
        assert too_long.national_id == "Invalid"
        assert too_short.national_id == "Invalid"
        assert invalid.national_id == "Invalid"
    def test_account_promo_code(self):
        valid_code = PersonalAccount("John", "Doe", "87110745612", "PROM_XYZ")
        none_code = PersonalAccount("John", "Doe", "12345678901")
        wrong_code = PersonalAccount("John", "Doe", "12345678901", "PROMOXYZ")
        assert valid_code.balance == 50.0
        assert none_code.balance == 0.0
        assert wrong_code.balance == 0.0
    def test_age_validation(self):
        valid_age = PersonalAccount("John", "Doe", "87110745612", "PROM_XYZ")
        invalid_age = PersonalAccount("John", "Doe", "55031412347", "PROM_XYZ")
        assert valid_age.balance == 50.0
        assert invalid_age.balance == 0.0

class TestCompanyAccount:
    def test_create__company_account(self):
        company_account = CompanyAccount("Kremówki SA", "1234567890")
        assert company_account.name == "Kremówki SA"
        assert company_account.tax_number == "1234567890"
    def test_create_company_account_invalid_tax_number(self):
        company_account_too_long = CompanyAccount("Kremówki SA", "12345678901")
        company_account_too_short = CompanyAccount("Kremówki SA", "1234590")
        assert company_account_too_long.tax_number == "Invalid"
        assert company_account_too_short.tax_number == "Invalid"