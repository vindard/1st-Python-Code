'''
Code to generate a random number from a set of 2^n numbers using a standard deck
of 52 playing cards. The max value for n is 225 (log_2(52!) ~= 225).

The methodology used here is similar to how one would create a base-x number.

Overall methodology was inspired from:
https://github.com/trichoplax/Playing-card-entropy-source/blob/master/PlayingCardEntropySource.py


BASE-X NUMBERS & ENDIANNESS

e.g. The number 20 can be expressed as follows:
     - Base-2 : 10100
     - Base-16:    14
     - Base-10:    20

Effectively, each digit column represents a multiple by which that digit should
be multiplied. If we use the prior examples we get:

                    Base-2
        [ 2^4] | [ 2^3] | [ 2^2]  | [ 2^1] | [ 2^0]
         [16]  |  [ 8]  |  [ 4]   |  [ 2]  | [ 1] 
Digits:    1        0        1        0        0  
Values:   16        0        4        0        0

Sum as normal number = 16 + 0 + 4 + 0 + 0 = 20


                    Base-16
        [16^4] | [16^3] | [16^2]  | [16^1] | [16^0]
         [..]  |  [..]  |  [64]   |  [16]  | [ 1]         
Digits:    0        0        0        1        4  
Values:    0        0        0       16        4

Sum as normal number =  0 + 0 + 0 + 16 + 4 = 20


                    Base-10
        [10^4] | [10^3] | [10^2]  | [10^1] | [10^0]
         [..]  |  [..]  |  [100]  |  [10]  | [ 1]                 
Digits:    0        0        0        2        0  
Values:    0        0        0       20        0

Sum as normal number =  0 + 0 + 0 + 20 + 0 = 20



The numbers we use regularly are also organised with the larger value digits to the
left and the smaller value ones to the right. This is a known as 'Big Endian'.

Numbers can also be written with the smaller values first to the left and bigger
values to the right. This is known as 'Little Endian' and looks as follows:

                          BASE-10
                        Big Endian
        [10^4] | [10^3] | [10^2]  | [10^1] | [10^0]
         [..]  |  [..]  |  [100]  |  [10]  | [ 1]                 
Digits:    0        0        0        2        0  
Values:    0        0        0       20        0

                      Little Endian
        [10^0] | [10^1] | [10^2]  | [10^3] | [10^4]
         [ 1]  |  [10]  |  [100]  |  [..]  |  [..]                 
Digits:    0        2        0         0        0  
Values:    0       20        0         0        0

So the number '20' written in:
Little Endian Base-10 is 02
Little Endian Base-16 is 41
Little Endian Base-2  is 00101

---------------------------------------------

DECK OF CARDS AND ENTROPY

Entropy can be loosely considered as a measure of randomness. It represents the number of 
equal probability outcomes one can produce from a system and the higher the entropy the more
random the information produced.

Entropy can be measured as a logarithm-base-2 outcome where the outcome is expressed in bits. e.g.:
- 1 fair coin flip  has  an entropy of 1 bit  (log_2(2) = 1) which maps to 2 possible outcomes (i.e. 2**1)
- 3 fair coin flips have an entropy of 3 bits (log_2(8) = 3) which maps to 8 possible outcomes (i.e. 2**3)

A single shuffled deck of cards can produce a maximum of 52! possible outcomes and so has a 
maximum entropy of ~225 bits (log_2(52!)).

52! comes from the decreasing number space that each card is drawn from. i.e.: the 1st draw has 
52 possible options, the 2nd draw has 51 possible options, the 3rd has 50 etc. The function of the number
of possible outcomes therefore looks like '52 x 51 x 50 x ... x 3 x 2 x 1  =  52!'. 

We can also use a deck of cards to produce smaller entropy numbers by drawing less cards. E.g.:
- if I draw only 3 cards, my number space is '52 x 51 x 50 = 52!/49!' and my entropy is
log_2(52!/49!) = 17 bits


---------------------------------------------
METHODOLOGY
---------------------------------------------

The idea here is to be able to generate a number from 0 to 2**n, where n is the number of bits.

To be effective (i.e. truly random), the algorithm will have to give each of those numbers an
equal probabilty of being selected with each shuffled deck.

The way this was accomplished was by choosing a number of cards (c) to draw that would bring the 
range size closest to and no less than 2**n. 
For example, for a 128 bit number, drawing 24 cards (log_2(52!/28!)) would give an entropy of 
127.63 bits and so we would have to draw 25 cards instead to capture the entire 128-bit (2**128) range.

After this, each card was assigned a value in the respective range of possible cards to be multiplied 
by the corresponding factorial quotient for that range. i.e.:
                    DECK VALUE ASSIGNMENT
                        Little Endian
        [52!/52!] | [52!/51!] | [52!/51!] | [52!/51!]  |   ....
           [ 1]   |   [52]    |  [52x51]  | [52x51x50] |   ....
Digits:      a          b           c           d          ....        
Values:      a       52 x b     1,652 x c   132,600 x d    ....

---------------------------------------------

DRIFTING BASE AND DRIFTING CARD RANGE

Instead of a Base-52 representation, a drifting base was used (reflected by the
factorial quotients). This was done so as to capture every number between 
0 and 52!/(52-c)! as some configuration of decks shuffled.

                        Little Endian
Base-52         [ 1]   |   [52]    |  [52x52]  | [52x52x52] |   ....
Drifting base   [ 1]   |   [52]    |  [52x51]  | [52x51x50] |   ....

Also important, cards were not assigned fixed values, but rather were shifted after each card pull.
The cards are merely a way to evenly choose a digit for each corresponding power and so if they 
remained fixed, we would still only be able to produce 52!/(52-c)! numbers, but drawn unevenly
from a range of 0 - 52!

To illustrate this, take the example of choosing 1 of 5 cards followed by choosing 1 of the 
remaining 4 cards below:

1ST DRAW
[Range 0 - 4]
 AS  |  2S  |  3S  |  4S  |  5S
'0'  | '1'  | '2'  | '3'  | '4'
>> Draw 3S, equivalent digit is '2'.


2ND DRAW
[Range 0 - 3, NO card drift]
 AS  |      |  3S  |  4S  |  5S
'0'  |      | '2'  | '3'  | '4'
>> Draw 5S, equivalent digit is '4'.

[Range 0 - 3, WITH card drift]
 AS  |  3S  |  4S  |  5S  
'0'  | '1'  | '2'  | '3'  
>> Draw 5S, equivalent digit is '3'.

In the case of no card drift, a '4' is selected for the '0 - 3' column range which could give
a number outside of the range we're looking to select from. In this deck instance too, there 
would be no configurations possible where the 2nd digit is represented by a '2' which would 
exclude an entire sub-range of possible from our intended range.

As such, it is the range of numbers that is the priority, and the cards are simply a means to 
choose from that range. This is why they are shifted to match the corresponding number range.

This insight is especially important for the next part of this algorithm.

---------------------------------------------

TIGHTENING RANGE FOR N-BIT NUMBER SELECTION

In the case where what is needed is a random n-bit number (i.e. number in range 0 - 2**n), then
to maintain the randomness the total range of numbers should be limited to exactly '0 - 2**n'. 

Since we are working with a drifting base-(52!/(52-c)!) number generated from the deck, the
algorithm would need to discard the extra numbers above the range to maintain the evenness of
the number selection.

The first step in this process can be accomplished by tightening the range of the most significant
digit in the generated number from the deck. For e.g.:
    
    For an 8-bit number, our number space is 256 numbers big (range 0 - 255) but we would have to
    draw 2 cards to get this giving us a selection space of 2652 (range 0 - 2655). The instinctive
    solution would be to discard any two cards drawn that gives a number above 255, but this would
    be inefficient since in this case ~90.3% of shuffled decks would need to be discarded.
    
A more efficient step would be to limit the range of numbers for the most significant digit to
reduce the number space.

In this instance, limiting the last card drawn (most significant digit) to represent a range
of '0 - 4' (5 possible digits) would bring our number space down to '0 - 259' 
(52!/((52-c)+1)! x 5 = 260 possible digits). At this point we can simply discard the last drawn
card until we get a card representing one from the range '0 - 4' instead of reshuffling the 
entire deck. 
Instead of discarding ~90.3% of decks, we now only discard ~1.5% of shuffled deck, but we still
would have to discard ~90.2% of last cards drawn.

This can further be optimised by grouping all the possible outcomes for the last card into 
a number of sets representing the number of outcomes we are trying to get. In the example, the range
of cards '0 - 50' can be grouped into 5 sets of 10 cards with only one non-assigned card remaining.
A card drawn from each corresponding set would correspond to the digit for that set so that for this
last draw, instead of each card mapping to one digit we would have multiple cards within sets mapping
to those same respective digits.
By doing this, we are able to reduce having to discard ~90.2% of last cards drawn to just ~2.0%
instead.
(Inspiration for this last optimisation: https://math.stackexchange.com/a/1314473)

To summarise, the result in the case of the 8-bit number example is that we move from:
1. Discarding ~90.3% of shuffled decks, to
2. Discarding ~1.5% of shuffled decks, but discarding ~90.2% of last cards drawn within each deck, to
3. Discarding ~1.5% of shuffled decks and ~2.0% of last cards drawn within each deck

---------------------------------------------

'''

from math import factorial
from math import log

# For decNum_to_card() accuracy (increase from 14 digits in float)
from decimal import *
getcontext().prec = 50
# --------------
    
deck_size = 52


def make_deck():
    '''
    Card order created using Unicode order.
    
    '''
    card_ranks = 'A23456789TJQK'
    card_suits = 'SHDC'
    card_deck  = [(rank + suit) for suit in card_suits for rank in card_ranks]
    
    return card_deck


def no_of_cards(bits=128):
    '''
    Function to determine how many cards to pull based on bits required.
    
    '''
    
    for num in reversed(range(1,deck_size + 1)):
        
        check = factorial(deck_size)/factorial(num)
        
        if check >= 2**bits:
            return deck_size - num


def alt_no_of_cards(bits=128):
    '''
    Alternative method of finding number of cards using logarithms
    (To check whether more memory efficient)
    
    MATH:
    log_2(52!/x!) = bits
    log_2(52!) - log_2(x!) = bits
    log_2(x!) = log_2(52!) - bits
    x! = 2**(log_2(52!) - bits)
    
    '''
    fx = 2**(log(factorial(deck_size), 2) - bits)
    
    # Loop to find equivalent 'x' for x! = fx
    i   = 0
    num = 0
    while num <= 1:
        i += 1
        num = factorial(i) / fx
    
    i -= 1
    return deck_size - i


def last_card_range(bits=128):   
    '''
    Equivalent logic is using 8-bit num as example:
    
    52 x 51 x 50 x ...
    ------------------       is too large!
              50 x ...
              
    
    52 x  5 x 50 x ...
    ----------------------   reduces the number space
              50 x ...
    
    '''
    x = deck_size - no_of_cards(bits)
    x += 1    # to increment us up to the last-card slot for manipulation
    f1 = factorial(52)
    f2 = factorial(x)
    
    for i in range(1,x+1):
        check = ((f1*i)/(f2)) / 2**bits  
        if check >= 1:
            break
    
    discard_card_rate = ((x - i)/x) * 100
    discard_deck_rate = ((check-1)/check) * 100
    x -= 1   # to decrement us back from last-card slot
    
    # 'i'        gives no. of valid cards
    # 'x'        gives the number of cards not drawn
    return (i,discard_deck_rate,discard_card_rate,x)
        
        
def pull_another_card(pulled_cards):
    '''
    Pulls the next card from the deck, checks that card is legit,
    checks that card hasn't already been pulled.
    
    '''
    incorrect_card = True
        
    current_card = input("Please enter your next card: ").upper()
    while incorrect_card:
        if current_card in make_deck() and current_card not in pulled_cards:
            incorrect_card = False
        else:
            current_card = input("Invalid card, try again: ").upper()
    
    return current_card


def request_cards(bits):
    '''
    Function that requests the required no. of cards from a deck of 52. 
    The required no. of cards is based on the bit-size of number needed.
    
    It returns a set containing the pulled cards input by the user.
    
    '''
    print(f'We will now accept {no_of_cards(bits)} cards as follows.\n')
    
    pulled_cards_inst = []
    for i in range(no_of_cards(bits)):
        pulled_cards_inst.append(pull_another_card(pulled_cards_inst))
        print(f"{pulled_cards_inst}\n")
    
    return pulled_cards_inst

   
#  Tightening number range for n-bit number selection
def adjust_pulled_cards(pulled_cards,bits=128):
    
    '''
    Pass in pulled cards
    
    Remove all except last card from a full deck (list comprehension difference)
    
    Limits last card to set of valid cards by checking index in remaining_deck
    
    If last card not in valid cards then re-request until it is
    
    Math is, reduces invalid decks by iterating on last card to adjust numbers.
    
    Batching cards into sets reduces this even further (increases efficiency) by reducing the
    last card range to pull in as many valid cards as possible.
        
    '''
    remaining_cards = [card for card in make_deck() if card not in pulled_cards[:-1]]
    
    current_card = pulled_cards[-1]
    i = remaining_cards.index(current_card)
    
    # Unpacking the last_card_range function
    range_size        = last_card_range(bits)   
    cards_valid       = range_size[0]
    discard_deck_rate = range_size[1]
    discard_card_rate = range_size[2]
    cards_all         = range_size[3] + 1  # +1 to increment up to last-card slot
    
    # -------------BATCHES CARDS INTO SETS------------------
    split_size = cards_valid                                        #Locks the splits size
    range_split_into  = cards_all // split_size                     #Locks number of splits
    cards_valid   = cards_all - (cards_all % cards_valid)           #Resets no. of valid cards
    print(f"----------------------------- \n"
           "  FOR LAST CARD SELECTION"
           "----------------------------- \n")
    print(f"Entire range: {cards_all} || Reduce range to: {split_size}")
    print(f"Range split into: {range_split_into} sets of {split_size} each || Cards left outside range: {cards_all % cards_valid} \n")
    
    discard_card_rate = (cards_all % cards_valid) / cards_all * 100
    
    i_before = i
    #i //= range_split_into
    i %= split_size
    # -------------/BATCHES CARDS INTO SETS-----------------
    
    # This 'if loop' left outside 'while loop' below so that it only prints once
    if i_before >= cards_valid:
        print(f"Will need to rechoose last card {discard_card_rate:.2f}% of times || {cards_valid} of {cards_all} valid cards")
        print(f"Will need to discard {discard_deck_rate:.2f}% of decks shuffled")
        print(f"------------------")
    
    # (range_size-1) to account for index starting at 0
    while i_before >= cards_valid:
        print(f"Last card '{current_card}' too large! Please discard")
        current_card = pull_another_card(pulled_cards)
        i = remaining_cards.index(current_card)
        
        # -------------BATCHES CARDS INTO SETS------------------
        i_before = i
        #i //= range_split_into
        i %= split_size
        # -------------/BATCHES CARDS INTO SETS-----------------
        
    # -------------BATCHES CARDS INTO SETS------------------
    current_card_before = current_card
    current_card = remaining_cards[i]
    print(f"Last card before: {current_card_before} (i = {i_before}) || Last card after: {current_card} (i = {i})")
    # -------------/BATCHES CARDS INTO SETS-----------------
    
    pulled_cards.pop()
    pulled_cards.append(current_card)
     
        
    return pulled_cards


def _div_powers_of_2(big_num):
    '''
    Written as a sanity check to be used if user finds that too many 
    trailing zeroes are being returned in the binary representation
    of the num.
    
    The number of trailing zeroes should match with the power (function
    output) returned.
    
    '''
    x = 0
    i = 0

    while x == 0:
        i += 1
        if big_num == 0:
            break
        x = big_num % (2**i)
        #print(f"x: {x} |i= {2**i} (2**{i})")
    
    print(f"Check: {big_num} is divible up up to 2^{i-1} ({2**(i-1)})\n")
    return i - 1
    

#----------------------------------------------------------------------------
#  RANDOM NUMBER GENERATORS
#----------------------------------------------------------------------------

def cards_to_decNum(bits=128):
    '''
    Function that prompts for a certain number of cards based on 
    the bitsize required for the final number.
    
    The function then converts those pulled cards into a single
    decimal number and return that number. 
    
    It does this by assuming that each card pulled represents a 
    value to the power of the factorial. First card is treated as
    smallest value digit.
    (clean up this para)
    
    Note: set of cards is little endian. This is to allow manipulation
    of last card to get better randomness accuracy (can change the last
    digit to reduce factorial).
    
    To get big endian simply reverse the pulled_cards in 'for' loop below.
    
    '''
    remaining_cards = make_deck()
    pulled_cards = request_cards(bits)
    
    # Tightens range, reduces tries
    pulled_cards = adjust_pulled_cards(pulled_cards,bits)
        
    print(
          "------------------\n"
          "CALCULATIONS BELOW\n"
          "------------------\n")

    # Loop to convert pulled cards into a single decimal number
    dec_num = 0
    for i,card in enumerate(pulled_cards):
        
        dec_digit = remaining_cards.index(card.upper())
        remaining_cards.pop(dec_digit)
        print(f"card: {card.upper()} || digit: {dec_digit} || from set of: 0 - {len(remaining_cards)}")

        f1 = factorial(52)
        f2 = factorial(52-i)
        
        # Works down the factorial list starting with 52!/52!      
        dec_num += dec_digit * (f1 / f2)
        print(f"{dec_digit} x {52}!/{52-i}! = {dec_digit * (f1 / f2)}")
        print(f"dec_num = {dec_num}\n-----")
        
    print(f"\ndec_num = {dec_num}")
    #_div_powers_of_2(dec_num) # A check used in development
    
    return int(dec_num)


def cards_to_binNum(num_of_bits=128):
    '''
    A function that requests cards (using cards_to_decNum function)
    and then converts the output of that function to raw bin num.
    
    '''           
    return bin(cards_to_decNum(num_of_bits))[2::]


def cards_to_bits(num_of_bits=128):
    '''
    A function that requests cards (using cards_to_binNum function)
    and then converts the output of that function to required number
    of bits.
    
    '''
    dec_num = int(cards_to_binNum(num_of_bits), 2)
    
    # Cuts range to exactly 2^no_of_bits numbers
    while dec_num >= 2**num_of_bits:
        
        print(f"Sorry, invalid deck (happens {last_card_range(num_of_bits)[1]:.2f} in 100 times)\n"
              f"Please shuffle again and start over!\n"
              f"--------------\n")
        
        dec_num = cards_to_decNum(num_of_bits)
    
    
    truncated_num = bin(dec_num)[2::]
    num_as_bin = truncated_num
    
    if len(num_as_bin) > num_of_bits:
        truncated_num = num_as_bin[:num_of_bits]
    else:
        for i in range(num_of_bits-len(num_as_bin)):
            truncated_num = '0' + truncated_num
            
    
    print(f"Length original binary: {len(num_as_bin)}")
    print(f"Length binary as bits: {len(truncated_num)}")
    
    return truncated_num


def decNum_to_cards(num_to_change,num_of_bits=128):
    '''
    Takes a decimal number and converts it into a set of cards according to 
    the method outlined in cards_to_decNum().
    
    Starts by selecting the for each power place and then goes on to convert
    each of those to a card.
    
    The digits are created in a Big Endian format to make it easier to pull
    with the way python calcs & decimals work. The selecting range we iterate
    through is reversed for this reason.
    
    The cards are assigned in Little Endian format though.
    
    '''
    
    temp_num_list = []
    f1 = Decimal(factorial(52))
    
    for i in reversed(range(no_of_cards(num_of_bits))):

        f2 = Decimal(factorial(52-i))

        digit = Decimal(num_to_change // (f1/f2))
        temp_num_list.append(int(digit))
        num_to_change = Decimal(num_to_change % (f1/f2))
        
    print(f"Here are the {no_of_cards(num_of_bits)} digits to be converted to cards:")
    print(temp_num_list)
    
    
    remaining_cards = make_deck()
    pulled_cards=[]
    
    # Reversed because we need to pop the smallest value digit-place 1st
    for x in reversed(temp_num_list):
        pulled_cards.append(remaining_cards.pop(x))
        
    # Produced list is Little Endian, so for Big Endian we reverse
    #pulled_cards.reverse()
    
    print(f"----------------")
    print(f"Here are your {no_of_cards(num_of_bits)} cards:")
    print(pulled_cards)
    
    return pulled_cards


if __name__ == "__main__":
    
    print("Please enter your cards in the format: 'suit+rank', where \n"
          "suit is one of: 'SHDC', and\n"
          "rank is one of: 'A23456789TJQK'\n")
    again = "Y"
    while again != 'N':
        bits = int(input("How many bits?:"))
        print(f"\nNumber as bits: {cards_to_bits(bits)}")
        again = input("\nWould you like to go again? Y/N:").upper()