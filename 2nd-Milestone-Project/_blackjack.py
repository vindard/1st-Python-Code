from play_game import play_game

play_again = True
while play_again:
    play_game()
    if input("Play again? Y/N: ").upper() == "N":
        play_again = False

print("\nThanks for playing!")