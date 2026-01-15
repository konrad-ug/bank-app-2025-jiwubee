import pytest
from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount


@pytest.fixture
def registry():
    return AccountsRegistry()


@pytest.mark.parametrize(
    "accounts_to_add, expected_count",
    [
        ([], 0),
        ([("John", "Doe", "12345678901")], 1),
        ([("John", "Doe", "12345678901"),
          ("Jane", "Doe", "11111111111")], 2),
    ]
)
def test_add_and_count(registry, accounts_to_add, expected_count):
    for first, last, national_id in accounts_to_add:
        registry.add_account(PersonalAccount(first, last, national_id))

    assert registry.count() == expected_count


@pytest.mark. parametrize(
    "accounts, search_id, expected_found",
    [
        ([], "12345678901", None),
        ([("John", "Doe", "12345678901")], "12345678901", "12345678901"),
        ([("John", "Doe", "12345678901"),
          ("Jane", "Doe", "11111111111")], "11111111111", "11111111111"),
        ([("John", "Doe", "12345678901")], "00000000000", None),
    ]
)
def test_find_by_national_id(registry, accounts, search_id, expected_found):
    for first, last, national_id in accounts:
        registry. add_account(PersonalAccount(first, last, national_id))

    result = registry.find_by_national_id(search_id)

    if expected_found is None:
        assert result is None
    else:
        assert result.national_id == expected_found


@pytest.mark.parametrize(
    "accounts",
    [
        [],
        [("John", "Doe", "12345678901")],
        [("John", "Doe", "12345678901"),
         ("Jane", "Doe", "11111111111")],
    ]
)
def test_get_all_accounts(registry, accounts):
    for first, last, national_id in accounts:
        registry.add_account(PersonalAccount(first, last, national_id))

    result = registry. get_all_accounts()

    assert len(result) == len(accounts)

    for (expected_first, expected_last, expected_id), account in zip(accounts, result):
        assert account.national_id == expected_id