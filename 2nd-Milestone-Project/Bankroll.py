class Bankroll():
    
    def __init__(self, curr_bet=0, player_bank=0, dealer_bank=0):
        self.curr_bet = curr_bet
        self.player_bank = player_bank
        self.dealer_bank = dealer_bank
        
    def deposit(self,dep_amt):
        self.player_bank += dep_amt
        print(f"New bankroll is {self.player_bank}")
        
    
    def withdraw(self,draw_amt):
        while draw_amt >= self.player_bank:
            while True:
                try:
                    draw_amt = int(input(f"Please enter a withdrawal amount under {self.player_bank}: "))
                except:
                    print("Whoops! That is not a number")                    
                else:
                    break
        self.player_bank -= draw_amt
        print(f"New bankroll is {self.player_bank}")
    
    def bet(self,bet_size):
        while bet_size > self.player_bank:
            while True:
                try:
                    bet_size = int(input(f"Please enter a bet less than {self.player_bank}: "))
                except:
                    print("Whoops! That is not a number")
                    continue
                else:
                    break
        
        self.curr_bet = bet_size
    
    def player_win(self):
        self.player_bank += bet_size
        self.dealer_bank -= bet_size
        print(f"New bankroll is {self.player_bank}")
    
    def dealer_win(self):
        self.player_bank -= self.curr_bet
        self.dealer_bank += self.curr_bet
        print(f"New bankroll is {self.player_bank}")