from dicegame import DiceGame

class DiceGameAnalytical(DiceGame):
    def __init__(self, balance, house_edge=0.00):
        super().__init__(balance=balance, house_edge=house_edge)
        self.current_lose_streak = 0
        self.current_win_streak = 0
        self.max_lose_streak = 0
        self.max_win_streak = 0
    
    def win(self):
        self.current_lose_streak = 0
        self.current_win_streak += 1
        if self.current_win_streak > self.max_win_streak:
            self.max_win_streak = self.current_win_streak
        return super().win()
        
    def lose(self):
        self.current_win_streak = 0
        self.current_lose_streak += 1
        if self.current_lose_streak > self.max_lose_streak:
            self.max_lose_streak = self.current_lose_streak
        return super().lose()


if __name__ == "__main__":

    dg = DiceGameAnalytical(10000000000)
    dg.set_win_chance(75)
    print(dg.balance)
    print(dg.multiplier)
    dg.set_bet_amount(10)

    for i in range(100000000000):
        if dg.can_bet():
            dg.bet()
        else:
            print("Cannot bet anymore")
            break
        # print(dg.balance)

    print("Balance Amount:", dg.balance)
    print("Win count: ", dg.win_count)
    print("Loss count: ", dg.loss_count)

    print("Max loosing Streak:", dg.max_lose_streak)
    print("Max winning streak", dg.max_win_streak)