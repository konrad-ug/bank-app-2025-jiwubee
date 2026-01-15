import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

@pytest.fixture
def valid_personal_data():
    return ("John", "Doe")


@pytest.fixture
def valid_company_name():
    return "Kremówki SA"

class TestPersonalAccount:

    def test_account_creation(self, valid_personal_data):
        first, last = valid_personal_data
        account = PersonalAccount(first, last, "12345678901")
        assert account.first_name == first
        assert account. last_name == last
        assert account.balance == 0.0
        assert account.national_id == "12345678901"

    @pytest.mark.parametrize("national_id", [
        "1234567890123",  # too long
        "123",            # too short
        "abc"             # non-numeric
    ])
    def test_account_invalid_national_id(self, valid_personal_data, national_id):
        first, last = valid_personal_data
        account = PersonalAccount(first, last, national_id)
        assert account.national_id == "Invalid"

    @pytest.mark.parametrize(
        "pesel,promo_code,expected_balance",
        [
            ("87110745612", "PROM_XYZ", 50. 0),   # valid age + valid code
            ("12345678901", None, 0.0),          # no promo
            ("12345678901", "PROMOXYZ", 0.0),    # invalid promo code
        ]
    )
    def test_account_promo_code(self, valid_personal_data, pesel, promo_code, expected_balance):
        first, last = valid_personal_data
        account = PersonalAccount(first, last, pesel, promo_code)
        assert account.balance == expected_balance

    @pytest.mark.parametrize(
        "pesel,expected_balance",
        [
            ("87110745612", 50.0),  # born after 1960 → promo applies
            ("55031412347", 0.0),   # born before 1960 → promo ignored
        ]
    )
    def test_age_validation(self, valid_personal_data, pesel, expected_balance):
        first, last = valid_personal_data
        account = PersonalAccount(first, last, pesel, "PROM_XYZ")
        assert account.balance == expected_balance

    def test_get_birth_from_national_id(self):
        """Test metody statycznej get_birth_from_national_id"""
        birth_year = PersonalAccount.get_birth_from_national_id("87110745612")
        assert birth_year == 1987

    def test_promo_code_with_invalid_national_id(self, valid_personal_data):
        """Test że promo nie działa z nieprawidłowym PESEL"""
        first, last = valid_personal_data
        account = PersonalAccount(first, last, "123", "PROM_XYZ")
        assert account.balance == 0.0

class TestCompanyAccount:

    def test_create_company_account(self, valid_company_name):
        company_account = CompanyAccount(valid_company_name, "1234567890")
        assert company_account.name == valid_company_name
        assert company_account.tax_number == "1234567890"

    @pytest.mark.parametrize("tax_number", [
        "12345678901",   # too long
        "1234590"        # too short
    ])
    def test_create_company_account_invalid_tax_number(self, valid_company_name, tax_number):
        company_account = CompanyAccount(valid_company_name, tax_number)
        assert company_account.tax_number == "Invalid"

    def test_company_account_initial_values(self, valid_company_name):
        """Test że konto firmowe ma poprawne wartości początkowe"""
        company_account = CompanyAccount(valid_company_name, "1234567890")
        assert company_account. balance == 0
        assert company_account.history == []
        assert company_account.express_transfer_fee == 5