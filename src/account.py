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
            self.balance -= (amount+self.express_transfer_fee)
            self.history.append(-amount)
            self.history.append(-(self.express_transfer_fee))
        return self.balance