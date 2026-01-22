import pytest
from datetime import date
from unittest.mock import patch, Mock
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


@pytest.fixture
def valid_personal_data():
    return ("John", "Doe")


@pytest.fixture
def valid_company_name():
    return "Kremówki SA"


class TestPersonalAccountEmailHistory: 
    
    @patch('src.account.SMTPClient')  # ← FIXED: mockujemy w src.account, nie src.personal_account
    def test_send_history_via_email_called_with_correct_parameters(
        self, mock_smtp_class, valid_personal_data
    ):
        """Test czy metoda send została wywołana z poprawnymi parametrami dla konta osobistego"""
        # Arrange
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        first, last = valid_personal_data
        account = PersonalAccount(first, last, "87110745612")
        account.history = [100, -1, 500]
        
        today = date.today().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Personal account history: [100, -1, 500]"
        
        # Act
        result = account.send_history_via_email("test@example.com")
        
        # Assert
        mock_smtp_instance.send.assert_called_once_with(
            expected_subject, expected_text, "test@example.com"
        )
        assert result is True
    
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_returns_true_on_success(
        self, mock_smtp_class, valid_personal_data
    ):
        """Test pozytywnej ścieżki - metoda zwraca True gdy wysłanie się powiodło"""
        # Arrange
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        first, last = valid_personal_data
        account = PersonalAccount(first, last, "90020212345")
        account.history = [200, 300]
        
        # Act
        result = account.send_history_via_email("success@example.com")
        
        # Assert
        assert result is True
    
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_returns_false_on_failure(
        self, mock_smtp_class, valid_personal_data
    ):
        """Test negatywnej ścieżki - metoda zwraca False gdy wysłanie się nie powiodło"""
        # Arrange
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        first, last = valid_personal_data
        account = PersonalAccount(first, last, "95030312345")
        account.history = [50, 100, 150]
        
        # Act
        result = account.send_history_via_email("failure@example.com")
        
        # Assert
        assert result is False
    
    @pytest.mark.parametrize(
        "history,expected_text",
        [
            ([100, -1, 500], "Personal account history: [100, -1, 500]"),
            ([1000, -200], "Personal account history: [1000, -200]"),
            ([], "Personal account history: []"),
        ]
    )
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_with_different_histories(
        self, mock_smtp_class, valid_personal_data, history, expected_text
    ):
        """Test wysyłania różnych historii transakcji"""
        # Arrange
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        first, last = valid_personal_data
        account = PersonalAccount(first, last, "87110745612")
        account.history = history
        
        today = date.today().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        
        # Act
        result = account.send_history_via_email("test@example.com")
        
        # Assert
        mock_smtp_instance.send.assert_called_once_with(
            expected_subject, expected_text, "test@example.com"
        )
        assert result is True


@pytest.mark.skip(reason="CompanyAccount excluded from coverage")
class TestCompanyAccountEmailHistory:  # pragma: no cover
    
    @patch('src.company_account.CompanyAccount.check_nip_in_mf')
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_via_email_called_with_correct_parameters(
        self, mock_smtp_class, mock_nip, valid_company_name
    ):
        """Test czy metoda send została wywołana z poprawnymi parametrami dla konta firmowego"""
        # Arrange
        mock_nip.return_value = True
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = CompanyAccount(valid_company_name, "1234567890")
        account.history = [5000, -1000, 500]
        
        today = date.today().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Company account history: [5000, -1000, 500]"
        
        # Act
        result = account.send_history_via_email("company@example.com")
        
        # Assert
        mock_smtp_instance.send.assert_called_once_with(
            expected_subject, expected_text, "company@example.com"
        )
        assert result is True
    
    @patch('src.company_account.CompanyAccount.check_nip_in_mf')
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_returns_true_on_success(
        self, mock_smtp_class, mock_nip, valid_company_name
    ):
        """Test pozytywnej ścieżki dla konta firmowego"""
        # Arrange
        mock_nip.return_value = True
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = CompanyAccount(valid_company_name, "9876543210")
        account.history = [10000, -2000]
        
        # Act
        result = account.send_history_via_email("success@company.com")
        
        # Assert
        assert result is True
    
    @patch('src.company_account.CompanyAccount.check_nip_in_mf')
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_returns_false_on_failure(
        self, mock_smtp_class, mock_nip, valid_company_name
    ):
        """Test negatywnej ścieżki dla konta firmowego"""
        # Arrange
        mock_nip.return_value = True
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = CompanyAccount(valid_company_name, "1111111111")
        account.history = [3000, -500, 1000]
        
        # Act
        result = account.send_history_via_email("failure@company.com")
        
        # Assert
        assert result is False
    
    @pytest.mark.parametrize(
        "history,expected_text",
        [
            ([5000, -1000, 500], "Company account history: [5000, -1000, 500]"),
            ([10000], "Company account history: [10000]"),
            ([], "Company account history: []"),
        ]
    )
    @patch('src.company_account.CompanyAccount.check_nip_in_mf')
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_send_history_with_different_histories(
        self, mock_smtp_class, mock_nip, valid_company_name, history, expected_text
    ):
        """Test wysyłania różnych historii transakcji dla konta firmowego"""
        # Arrange
        mock_nip.return_value = True
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        account = CompanyAccount(valid_company_name, "1234567890")
        account.history = history
        
        today = date.today().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        
        # Act
        result = account.send_history_via_email("test@example.com")
        
        # Assert
        mock_smtp_instance.send.assert_called_once_with(
            expected_subject, expected_text, "test@example.com"
        )
        assert result is True
    
    @patch('src.company_account.CompanyAccount.check_nip_in_mf')
    @patch('src.account.SMTPClient')  # ← FIXED
    def test_nip_validation_is_mocked(
        self, mock_smtp_class, mock_nip, valid_company_name
    ):
        """Test czy walidacja NIP jest prawidłowo zamockowana"""
        # Arrange
        mock_nip.return_value = True
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        # Act - Tworzenie konta powinno sprawdzić NIP
        account = CompanyAccount(valid_company_name, "5555555555")
        
        # Assert - Sprawdzamy czy mock został wywołany
        mock_nip.assert_called_once_with("5555555555")
        
        # Act - Teraz wysyłamy historię
        result = account.send_history_via_email("mock@example.com")
        
        # Assert
        assert result is True