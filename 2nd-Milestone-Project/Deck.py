# Consider maybe doing a Deck class with these
# Things like Deck.shuffle, Deck.draw

from random import randint

class Deck():

    def __init__(self,dealt=[],player_hand=[],dealer_hand=[],
                 last_card=(),turn='',
                 player_count_A11=0, player_count_A1=0,dealer_count_A11=0,dealer_count_A1=0):
        
        self.dealt = dealt
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.last_card = last_card
        self.turn = turn
        self.player_count_A11 = player_count_A11
        self.player_count_A1 = player_count_A1
        self.dealer_count_A11 = dealer_count_A11
        self.dealer_count_A1 = dealer_count_A1                
    
    def shuffle(self):
        self.dealt = []
        self.player_hand = []
        self.dealer_hand = []
        self.last_card = ()
        self.player_count_A11 = 0
        self.player_count_A1 = 0
        self.dealer_count_A11 = 0
        self.dealer_count_A1 = 0
    
 
    # Internal module    
    def assign_card(self,num):
        suit = {0:"c",1:"d",2:"h",3:"s"}
        face = {9:"J",10:"Q",11:"K",12:"A"}
        deck = []

        if num % 13 < 9:
            card_num = (num % 13) + 2
        else:
            card_num = face[num % 13]

        self.last_card = ((num % 13) + 2, card_num, suit[num // 13])


    # Internal module
    def draw_card(self):     
        i = randint(0,51)

        while i not in self.dealt and len(self.dealt)<52:
            self.dealt.append(i)
            self.assign_card(i)
            # To alternate turns
            if self.turn == 'Player':
                self.player_hand.append(self.last_card)
            elif self.turn== 'Dealer':
                self.dealer_hand.append(self.last_card)
        

    # Internal module    
    def tally(self):
        if self.last_card[1] == 'A':
            local_score_A11 = 11
            local_score_A1 = 1
        elif self.last_card[0] > 10:
            local_score_A11 = 10
            local_score_A1 = 10
        else:
            local_score_A11 = self.last_card[0]
            local_score_A1 = self.last_card[0]
                        
        if self.turn == 'Player':
            self.player_count_A11 += local_score_A11
            self.player_count_A1 += local_score_A1
            local_total_A11 = self.player_count_A11
            local_total_A1 = self.player_count_A1
            #print(f"Ace-02 count : {self.player_count_A1} \nAce-10 count is {self.player_count_A11}")
        elif self.turn == 'Dealer':
            self.dealer_count_A11 += local_score_A11
            self.dealer_count_A1 += local_score_A1
            local_total_A11 = self.dealer_count_A11
            local_total_A1 = self.dealer_count_A1
            #print(f"Ace-02 count : {self.dealer_count_A1} \nAce-10 count is {self.dealer_count_A11}")
        
    
    def player_play(self,hit_stand):
        self.turn = 'Player'
        if hit_stand == 'H':
            self.draw_card()
            self.tally()
        else:
            # End turn
            pass
        
    def dealer_play(self,hit_stand):
        self.turn = 'Dealer'
        if hit_stand == 'H':
            self.draw_card()
            self.tally()
        else:
            # End turn
            pass     
        
    
    def score_check(self):
        
        all_scores = [(self.player_count_A11, self.player_count_A1),(self.dealer_count_A11, self.dealer_count_A1)]
        final_scores = {"player":0,"dealer":0}
    
        # Return larger number less than 21
        i = 0
        for a,b in all_scores:
            i += 1
            if a > 21 and b > 21:
                c = -1
                #print("1:")
            elif a > 21 or b > 21:
                c = min(a,b)
                #print("2:")
            else:
                c = max(a,b)
                #print("3:")
            
            if i == 1:
                final_scores["player"] = c
            else:    
                final_scores["dealer"] = c
                     
        #print(final_scores["player"])
        #print(final_scores["dealer"])
        
        score_vals = list(final_scores.values())
        score_keys = list(final_scores.keys())
        leader = score_keys[score_vals.index(max(score_vals))]
        
        return score_vals