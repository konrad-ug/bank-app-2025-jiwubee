class Account: 
    def incoming_transfer(self, amount):
        self.balance += amount
    
    def outgoing_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount

    def express_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= (amount+self.express_transfer_fee)
        return self.balance