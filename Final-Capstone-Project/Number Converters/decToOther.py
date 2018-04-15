# Take decimal number and convert to hexadecimal

import string

def decToOther(dec,convertTo=16):
    
    tmp_list = []    # For storing individual digits of final hex
    check = True     # Used to count number of hex powers
    power = 0        # Used to store number of hex powers
    
    lett_digit_keys = list(range(10,36))
    lett_digit_vals = list(string.ascii_uppercase)
    num_to_letter = dict(zip(lett_digit_keys,lett_digit_vals))
    
    while dec > 0:
        
        # Get the number of powers of 16 in hex
        while check:
            check  = (dec > convertTo**power)
            power += 1

        
        # Set the value under each power
        for num in list(range(power))[::-1]:
            
            count = dec // (convertTo**num)
            
            if dec >= (convertTo**num):
                dec = dec - (count*(convertTo**num))
            
            if count > 9:
                count = num_to_letter[count]
            
            tmp_list.append(str(count))

        
        # Remove leading 0 from final hex number in certain cases
        if tmp_list[0] == '0':
            tmp_list[0] = ""

        
        return (''.join(tmp_list))
    
    else:
        
        return 0