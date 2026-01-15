from .account import Account
class CompanyAccount(Account):
    express_transfer_fee = 5
    def __init__(self, name, tax_number):
        self.name = name
        self.tax_number = self.validate_tax_number(tax_number)
        self.balance = 0
        self.history = []

        if self.tax_number != "Invalid":
            if not self.check_nip_in_mf(self.tax_number):
                raise ValueError("Company not registered!!")
        
    def validate_tax_number(self, number):
        if len(number) == 10:
            return number
        else:
            return "Invalid"

    @staticmethod
    def check_nip_in_mf(nip: str) -> bool:
        base_url = os.getenv(
            "BANK_APP_MF_URL",
            "https://wl-test.mf.gov.pl"
        )

        today = date.today().isoformat()
        url = f"{base_url}/api/search/nip/{nip}?date={today}"

        response = requests.get(url)
        data = response.json()

        print("MF RESPONSE:", data)

        subject = data.get("result", {}).get("subject")

        if not subject:
            return False

        return subject.get("statusVat") == "Czynny"
    def take_loan(self, amount):
        has_zus_payment = -1775 in self.history
        enough_balance = self.balance >= 2* amount
        if has_zus_payment and enough_balance:
            self.balance += amount
            return True
        return False