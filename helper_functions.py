def prepend_up_to_max_length(input,char="0",max_length=8):
    """adds char(s) at beginning of input until len(input)==max_length"""
    if len(input)<max_length:
        return prepend_up_to_max_length(char + input, char, max_length)
    else:
        return input

def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    return "%0X" % n
 
def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

def bin2dec(s):
    """return the integer value of a binary string s"""
    return int(s, 2)

def bin2hex(s):
    """return the hexadecimal string representation of binary string s"""
    return dec2hex(bin2dec(s))

def int2bin(n, count=8):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

def hex2bin(s,count=8):
    """returns the binary of hexadecimal string s, using count number of digits"""
    n=int(s, 16)
    return int2bin(n,count)

def bits_required(n):
    """returns the minumim number of bits required to represent integer n"""
    if n!=int(n) or n<0:
        raise ValueError("input is not an integer or < 0: " + str(n))
    if n==0:
        return 1
    else:
        r=0
        while n>0:
            r+=1
            n=n>>1
        return r

import datetime

def timestamp():
    return str(datetime.datetime.now())

def tc_to_int(bin): # two's complement to bin
    n = 0
    for i, b in enumerate(reversed(bin)):
        if b == '1':
            if i != (len(bin)-1):
                n += 2**i
            else: # MSB
                n -= 2**i 
    return n

if __name__ == '__main__':
#    str="11000000"
#    print tc_to_int(str)
    
    s="80031C5607A09530701020600E0E85500E02"
    print s
    print hex2bin(s,144)
    pass
