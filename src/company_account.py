from .account import Account
class CompanyAccount(Account):
    express_transfer_fee = 5
    def __init__(self, name, tax_number):
        self.name = name
        self.tax_number = self.validate_tax_number(tax_number)
        self.balance = 0
        self.history = []
        
    def validate_tax_number(self, number):
        if len(number) == 10:
            return number
        else:
            return "Invalid"

    def take_loan(self, amount):
        has_zus_payment = -1775 in self.history
        enough_balance = self.balance >= 2* amount
        if has_zus_payment and enough_balance:
            self.balance += amount
            return True
        return False