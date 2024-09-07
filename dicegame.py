import random

class DiceGame:
    def __init__(self, balance, house_edge = 0.00):
        self.win_count = 0
        self.loss_count = 0
        self.bet_amount = 0
        self.win_chance = 50
        self.balance = balance
        self.house_edge = house_edge
        self.last_bet_won = None
        self._set_multiplier_on_chance(self.win_chance)

    def set_bet_amount(self, bet_amount):
        self.bet_amount = bet_amount

    def _set_multiplier_on_chance(self,win_chance):
        self.multiplier = (99 / win_chance) * (1 - self.house_edge)

    def set_win_chance(self, win_chance):
        self.win_chance = win_chance
        self._set_multiplier_on_chance(self.win_chance)

    def roll_dice(self):
        return random.uniform(0, 100)
    
    def win(self):
        winning = self.bet_amount * (self.multiplier - 1)
        self.balance += winning
        self.win_count += 1
        return winning
    
    def lose(self):
        loss = self.bet_amount
        self.balance -= loss
        self.loss_count += 1
        return loss
    
    def can_bet(self):
        return self.bet_amount <= self.balance

    def bet(self):
        dice_value = self.roll_dice()
        if not self.can_bet():
            raise Exception("Cannot place bet")
        if dice_value < self.win_chance:
            self.win()
        else:
            self.lose()

if __name__ == "__main__":

    dg = DiceGame(10000)
    dg.set_win_chance(75)
    print(dg.balance)
    print(dg.multiplier)

    for i in range(1000000):
        dg.set_bet_amount(10)
        if dg.can_bet():
            dg.bet()
        else:
            print("Cannot bet anymore")
            break
        print(dg.balance)

    print("Win count: ", dg.win_count)
    print("Loss count: ", dg.loss_count)