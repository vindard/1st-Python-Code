from Deck import Deck
from Bankroll import Bankroll

def play_game():
    
    deck = Deck()
    bankroll = Bankroll()
    
    deck.shuffle()
    
    print(f"Current bankroll is {bankroll.player_bank}")
    dep_draw = input("Deposit/Withdraw? D/W or Enter to pass: ").upper()
            
    # BANKROLL: Deposit
    if dep_draw == "D" or bankroll.player_bank <= 0:
        while True:
            try:
                if bankroll.player_bank <=0:
                    print("Sorry your bankroll is 0!")
                bankroll.deposit(int(input("Please enter deposit amount: ")))
            except:
                print("Whoops! That is not a number")
            else:
                break

    # BANKROLL: Withdraw        
    if dep_draw == "W":
        while True:
            try:
                bankroll.withdraw(int(input("Please enter withdraw amount: ")))
            except:
                print("Whoops! That is not a number")
            else:
                break
    
    # BANKROLL: Place bet
    while True:
        try:
            bankroll.bet(int(input("Please place your bet: ")))
        except:
            print("Whoops! That is not a number")
        else:
            break
    
    
    # RUN GAME (Consider adding to 'Game' class as .deal_game)
    for i in range(4):
        if deck.turn == 'Player':
            deck.turn = 'Dealer'
        else:
            deck.turn = 'Player'
        
        deck.draw_card()
        deck.tally()
            
    print(f"Dealer: {deck.dealer_hand[0]}")
    print(f"Player: {deck.player_hand}")
    print(f"Player count: {deck.player_count_A11} & {deck.player_count_A1}")
    
    play = True
    hit_stand = ''
    while play:
        invalid_play = True
        while invalid_play:
            hit_stand = input("Hit or stand? H/S: ").upper()
            invalid_play = (hit_stand != 'H' and hit_stand != 'S')
            if invalid_play:
                print ("Please enter either 'H' or 'S'.")                      
        deck.player_play(hit_stand)  
        print(f"\nPlayer: {deck.player_hand}")
        print(f"Player count: {deck.player_count_A11} & {deck.player_count_A1}")
        play = ((deck.player_count_A11 < 21 or deck.player_count_A1 < 21) and
               (deck.player_count_A11 != 21 and deck.player_count_A1 != 21) and hit_stand == "H")
    
    if deck.player_count_A11 > 21 and deck.player_count_A1 > 21:
        # Player loses
        print("Bust")
    else:
        while (deck.score_check()[1] != -1) and (deck.score_check()[0]  > deck.score_check()[1]) and (deck.dealer_count_A1 < 17):
            deck.dealer_play("H")       
    
    print("\n")
    print(deck.player_hand)
    print(deck.dealer_hand)
    print(deck.dealt)
    print(f"Player count: {deck.player_count_A11} & {deck.player_count_A1}")
    print(f"Dealer count: {deck.dealer_count_A11} & {deck.dealer_count_A1}")
        
    if deck.score_check()[0]  > deck.score_check()[1]:        
        print("Player wins!")
        bankroll.player_bank += bankroll.curr_bet
        print(f"Your bankroll is now: {bankroll.player_bank}")
    elif deck.score_check()[0] == deck.score_check()[1]:
        print("Push! Bets returned")
        print(f"Your bankroll is now: {bankroll.player_bank}")
    else:
        print("Dealer wins!")
        bankroll.player_bank -= bankroll.curr_bet
        print(f"Your bankroll is now: {bankroll.player_bank}")
        
    make_deposit = "N"
    make_withdraw = "N"