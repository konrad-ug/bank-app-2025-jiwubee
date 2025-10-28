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
