import string

# Creates a dict to map digits for respective base
def setMapping(base):
    
    # Establish dict keys
    lett_digit_keys =   list(range(base))
    
    
    # dict values
    # For Base2 to Base36
    if base <= 36:
        lett_count      =   base - 10
        lett_digit_vals =   list(range(10)) \
                          + list(string.ascii_lowercase[:lett_count])
    
    # dict values
    # For Base64
    elif base == 64:        
        lett_digit_vals =   list(string.ascii_uppercase) \
                          + list(string.ascii_lowercase) \
                          + list(range(10))              \
                          + ['+','/']
    
    # dict values
    # for Base58 
    # assumed for Bitcoin, ordering different
    elif base == 58:        
        lett_digit_vals =   list(string.ascii_uppercase) \
                          + list(string.ascii_lowercase) \
                          + list(range(10))              \
                          + ['+','/']
        
        # Reorder numbers to front for use with Bitcoin
        for i in reversed(range(10)):
            lett_digit_vals.insert(0, lett_digit_vals.pop(lett_digit_vals.index(i)))
        
        # Convert Base64 list to Base58 list
        for i in [0,'O','I','l','+','/']:
            lett_digit_vals.pop(lett_digit_vals.index(i))
    
   
    return dict(zip(lett_digit_keys,lett_digit_vals))
    

# Allows for word-based inputs of base as well
def alphanumCheck(base):
    word_base_list = {'hex':16, 'bin':2, '64':64, '58':58, 
                      'oct':8, 'sex':60}
    
    if isinstance(base, int):
        return base
    
    for alpha_check in word_base_list:
        if alpha_check in base.lower():
            return word_base_list[alpha_check]
        
    
# Conversion method for decimal to base
def convertToBase(dec_num,base=16):
    
    base = alphanumCheck(base)
    mapping_dict = setMapping(base)
    
    # Initialise array to store converted num
    num_as_base = []
    
    # Iterate through decimal number to extract digits, reverse when done
    while dec_num > 0:
        digit = mapping_dict[dec_num % base]
        num_as_base.append(digit)
        dec_num //= base

    num_as_base = num_as_base[::-1]

    # Concatenate array into string representation of converted num
    base_num = "".join(str(x) for x in num_as_base)

    return base_num


# Conversion method for base to decimal
def convertToDec(base_num,base=16):

    base = alphanumCheck(base)
    mapping_dict = setMapping(base)

    # Initialise num where final output will be stored
    dec_num = 0
    
    # Iterate through base number in reverse to extract digits
    # Multiply each digit to respective power of 10 and add to final num
    for i,digit in enumerate(str(base_num)[::-1]):
        
        # Converts alphanum digit in decimal representation
        for k,v in mapping_dict.items():
            if str(v) == digit:
                digit = k
        
        dec_num += digit * base**i
                
    return dec_num