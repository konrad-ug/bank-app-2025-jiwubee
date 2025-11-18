from .account import Account
class PersonalAccount(Account):
    express_transfer_fee = 1
    def __init__(self, first_name, last_name, national_id, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.national_id = self.validate_national_id(national_id)
        self.promo_code = promo_code
        self.validate_promo()
        self.history = []

    def validate_national_id(self, national_id):
        if len(national_id) == 11 and national_id.isdigit():
            return national_id
        return "Invalid"

    @staticmethod
    def get_birth_from_national_id(national_id):
        yy = int(national_id[:2])
        return 1900 + yy

    def validate_promo(self):
        if (
            self.promo_code
            and self.promo_code.startswith("PROM_")
            and self.national_id != "Invalid"
        ):
            if self.get_birth_from_national_id(self.national_id) > 1960:
                self.balance += 50.0
    def submit_for_loan(self, amount):
        if len(self.history) >= 3 and all(val > 0 for val in self.history):
            self.balance += amount
            return True
        elif len(self.history) >= 5 and sum(self.history) > amount:
            self.balance += amount
            return True
        else:
            return False