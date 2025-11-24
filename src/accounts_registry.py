from src.personal_account import PersonalAccount

class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def find_by_national_id(self, national_id: str):
        for acc in self.accounts:
            if acc.national_id == national_id:
                return acc
        return None

    def get_all_accounts(self):
        return self.accounts

    def count(self):
        return len(self.accounts)
