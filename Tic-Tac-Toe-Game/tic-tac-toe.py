line_1 = {'key_1':'[1]','key_2':'[2]','key_3':'[3]',
          'key_4':'[4]','key_5':'[5]','key_6':'[6]',
          'key_7':'[7]','key_8':'[8]','key_9':'[9]'}


#Two players enter their names
def get_players():
    global player_1
    global player_2
    print "Player 1:"
    player_1 = raw_input()
    print "\nPlayer 2:"
    player_2 = raw_input()
    print ("\n""To play, simply type the number of the cell you would like to mark.")
    raw_input("> Hit 'Enter' to continue")
    
#prints the board
def print_board():
    print "\n"
    print "       |       |    "
    print "  {0}  |  {1}  |  {2}".format(line_1['key_1'],line_1['key_2'],line_1['key_3'])
    print "_______|_______|_______    "
    print "       |       |    "
    print "  {0}  |  {1}  |  {2}".format(line_1['key_4'],line_1['key_5'],line_1['key_6'])
    print "_______|_______|_______"
    print "       |       |    "
    print "  {0}  |  {1}  |  {2}".format(line_1['key_7'],line_1['key_8'],line_1['key_9'])
    print "       |       |    "
    
    
#returns 'True' if last player who played has just won
def win_check():
    #check for one of 8 possible key combinations
    win_options = {}
    win_options["Option 1"] = line_1['key_1'] + line_1['key_2'] + line_1['key_3']
    win_options["Option 2"] = line_1['key_4'] + line_1['key_5'] + line_1['key_6']
    win_options["Option 3"] = line_1['key_7'] + line_1['key_8'] + line_1['key_9']
    win_options["Option 4"] = line_1['key_1'] + line_1['key_4'] + line_1['key_7']
    win_options["Option 5"] = line_1['key_2'] + line_1['key_5'] + line_1['key_8']
    win_options["Option 6"] = line_1['key_3'] + line_1['key_6'] + line_1['key_9']
    win_options["Option 7"] = line_1['key_1'] + line_1['key_5'] + line_1['key_9']
    win_options["Option 8"] = line_1['key_3'] + line_1['key_5'] + line_1['key_7']
    
    if ' X  X  X ' in win_options.values():
        iswin = True
    elif ' O  O  O ' in win_options.values():
        iswin = True
    else:
        iswin = False
    
    return iswin


#function to get input for next move
def make_move():
    options = ['1','2','3','4','5','6','7','8','9']
    
    if play_count % 2 == 1: 
        current_player = player_1   #player 1 has odd plays
        symbol = 'X'
    else:
        current_player = player_2   #player 2 has even plays
        symbol = 'O'
        
    move = raw_input("{}'s ({}) move: ".format(current_player,symbol))
    while ((move in entered) or (move not in options)):  #checks for valid input
        print "Please enter a new number from 1 to 9: "
        move = raw_input("Your move: ")
        
    entered.append(move)
    line_1['key_'+move]=" "+symbol+" " #assigns move to board
    
    

#--------------------------------------------

#these global variables need to be set
play_count = 0
entered = []

#this function gets the player's names and gives instructions to play
get_players()

#this while loop runs the game
while win_check() == False:
    if len(entered) >= 9:
        break
    else:
        print_board()
        print "Play count is: {}\n".format(play_count)
        play_count += 1
        make_move()

#this block of code executes when game has ended
print "\n"
print_board()
if win_check() == False:
    print "\n Draw game :)"
elif play_count % 2 == 1:
    print "\n"+"{} wins! ".format(player_1)*3
else:
    print "\n"+"{} wins! ".format(player_2)*3
raw_input()
