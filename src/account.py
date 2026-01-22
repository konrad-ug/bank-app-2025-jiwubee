from smtp.smtp import SMTPClient
from datetime import date


class Account: 
    def incoming_transfer(self, amount):
        self.balance += amount
        self.history.append(amount)
    
    def outgoing_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)

    def express_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= (amount + self.express_transfer_fee)
            self.history.append(-amount)
            self.history.append(-(self.express_transfer_fee))
        return self.balance
    
    def send_history_via_email(self, email_address):
        from .personal_account import PersonalAccount
        subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        if isinstance(self, PersonalAccount):
            text = f"Personal account history: {self.history}"
        else:
            text = f"Company account history: {self.history}"

        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)