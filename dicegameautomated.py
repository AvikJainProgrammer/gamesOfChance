from dicegame import DiceGame

class DiceGameAutomated(DiceGame):
    def __init__(self, balance, house_edge = 0.00):
        super().__init__(balance=balance, house_edge=house_edge)
        self.original_bet_amount = self.bet_amount
        self.last_bet_won = None

    def win(self):
        self.last_bet_won = True
        return super().win()
    
    def lose(self):
        self.last_bet_won = False
        return super().lose()
    
    def set_bet_amount(self, bet_amount):
        self.original_bet_amount = bet_amount
        super().set_bet_amount(bet_amount)

    def auto_bet(self, bet_count = 10000,last_win_multiplier = None, last_loss_multiplier = None):
        for i in range(bet_count):
            if self.can_bet():
                self.bet()
            else:
                break
            if self.last_bet_won == True:
                if last_win_multiplier == None:
                    self.bet_amount = self.original_bet_amount
                else:
                    self.bet_amount = self.bet_amount * last_win_multiplier
            
            if self.last_bet_won == False:
                if last_loss_multiplier == None:
                    self.bet_amount = self.original_bet_amount
                else:
                    self.bet_amount = self.bet_amount * last_loss_multiplier

profit = 0
profit_count = 0
loss_count = 0

balance_amount = 10000
bet_amount = 0.01
win_chances = 75
bet_count = 10
loss_multiplier = 5
for i in range(10000000):
    dga = DiceGameAutomated(balance_amount)
    dga.set_bet_amount(bet_amount)
    dga.set_win_chance(win_chances)
    dga.auto_bet(bet_count,last_loss_multiplier=loss_multiplier)
    profit += (dga.balance - balance_amount)
    if dga.balance < balance_amount:
        loss_count += 1
    elif dga.balance > balance_amount:
        profit_count += 1

print("____")
print("Profit:",profit)
print("Profit percentage", (profit/balance_amount)*100)
print("Profit count:",profit_count)
print("Loss count:", loss_count)