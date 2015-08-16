'''
date: 2011-11-15

@author: heinzale
'''
from helper_functions import *

def crc_compute_int(data,no_data_bits,poly,sreg=0):
    if not (isinstance(data,int) or isinstance(data,long)):
        raise TypeError("data has to be of type int or long")
    if not isinstance(no_data_bits,int):
        raise TypeError("no_data_bits has to be of type int")
    if not isinstance(poly,int):
        raise TypeError("poly has to be of type int")
    if not isinstance(sreg,int):
        raise TypeError("sreg has to be of type int")
    
    if data<0:
        raise ValueError("data (%i) has to be >=0"%data)
    if no_data_bits<1:
        raise ValueError("no_data_bits (%i) has to be >=1"%no_data_bits)
    if poly<0:
        raise ValueError("poly (%i) has to be >=0"%poly)
    if sreg<0:
        raise ValueError("sreg (%i) has to be >=0"%sreg)
    
    data_max=(pow(2,no_data_bits)-1)
    
    if data>data_max:
        msg="data (%i) cannot be represented with no_data_bits (%i) bits"%(data,no_data_bits)
        raise ValueError(msg)
    if (poly & 1) != 1:
        msg="LSB of poly has to be 1"
        raise ValueError(msg)
    
    poly_order=0
    i=poly
    while i>0:
        i=i/2
        poly_order+=1
    if poly_order<=1:
        msg="the order of poly does not make sense for CRC computation (must be >1)"
        raise ValueError(msg)
    
    sreg_order=poly_order-1
    
    sreg_max=(pow(2,sreg_order)-1)

    if sreg>sreg_max:
        msg="sreg (%i) is incompatible with the defined polynomial (%i)"%(sreg,poly)
        raise ValueError(msg)
    
    for i in range(no_data_bits):
        msb_data=(data>>(no_data_bits-1))
        msb_sreg=(sreg>>(sreg_order-1))
        if msb_data!=msb_sreg:
            sreg=((sreg<<1) ^ poly ) & sreg_max
        else:
            sreg=((sreg<<1)        ) & sreg_max
        data=(data<<1) & data_max
        
    return sreg

#algorithm based on wikipedia
def crc_compute(data,poly,sreg):
    
#    if len(data)==21:
#        print "sreg ", sreg
        
    if sreg[0]!=data[0]:
        sreg=bin2dec(sreg+"0") ^ bin2dec(poly)
        sreg=int2bin(sreg,len(poly))
        sreg=sreg[1:]
    else:
        sreg=sreg[1:]+"0"
    data=data[1:]
    
    if len(data)>0:
        sreg=crc_compute(data,poly,sreg)
    return sreg

def crc3_magna(data_int_array):
    data=""
    for i in data_int_array:
        data+=str(i)
    
    poly="1011"
    sreg="101"
    
    crc3_str=crc_compute(sreg+data,poly,(len(poly)-1)*"0")
    crc3_int=bin2dec(crc3_str)
    return crc3_int
        

#general function for use with any polynomial
#data:string:regex:[01]+, poly:string:regex:[01]+
#poly example 1011=x^3+x^1+1
def crc_hw_try2_generic(data,poly):
    poly=poly[::-1]
    
    no_crc_bits=len(poly)-1
    
    b_old=(no_crc_bits)*[0]
    b=b_old[:]
    data_stop_pos=len(data)
    
    data+=no_crc_bits*"0"
    
    crc=""
    
    for i in range(len(data)):
        if i<data_stop_pos:
            fb=bin2dec(data[i])^b_old[-1]
        else:
            fb=0
            crc+=int2bin(b_old[-1],1)
        for i2 in range(len(b)):
            if i2==0:
                prev=0
            else:
                prev=b_old[i2-1]
            
            b[i2]=prev
            
            if poly[i2]=="1":# if feedback ...
                b[i2]^=fb
                
        b_old=b[:]
    return crc

#specific function for polynomial 1011
#data:string:regex:[01]+
def crc_hw_try2(data):
    b2_old=0
    b1_old=0
    b0_old=0

    for i in range(len(data)):
        input=bin2dec(data[i])^b2_old
        b2=b1_old
        b1=b0_old^input
        b0=input
        
        b0_old=b0
        b1_old=b1
        b2_old=b2
        
    crc=""
    for i in range(3):
        input=0
        crc+=int2bin(b2_old,1)
        b2=b1_old
        b1=b0_old^input
        b0=input
        
        b0_old=b0
        b1_old=b1
        b2_old=b2
    
    return crc


#specific function for polynomial 1011
#similar to crc-3 but WITHOUT adding 0s to data - THIS IS NO REAL CRC!
#NOT USED - just an example for the more general function
#data:string:regex:[01]+
def crc_weird(data):
    b2_old=0
    b1_old=0
    b0_old=0
    
    for i in range(len(data)):
        b0=b2_old^bin2dec(data[i])
        b1=b2_old^b0_old
        b2=       b1_old
        
        b0_old=b0
        b1_old=b1
        b2_old=b2
    crc=b2*4+b1*2+b0
    return int2bin(crc,3)

#general function for use with any polynomial
#similar to crc-3 but WITHOUT adding 0s to data - THIS IS NO REAL CRC!
#data:string:regex:[01]+, poly:string:regex:[01]+
def crc_ifx_weird(data,poly):
    poly=poly[::-1]
    
    b_old=(len(poly)-1)*[0]
    b=b_old[:]
    
    for i in range(len(data)):
        fb=b_old[-1] #feedback
        for i2 in range(len(b)):
            
            if i2==0:
                prev=bin2dec(data[i])
            else:
                prev=b_old[i2-1]
            
            b[i2]=prev
            
            if poly[i2]=="1":# if feedback ...
                b[i2]^=fb
                
        b_old=b[:]
    crc=0
    for i in range(len(b)):
        crc+=b[i]*(1<<i)
    return int2bin(crc,len(b))

if __name__ == '__main__' and False:
    poly_str="111" #crc3
    poly=bin2dec(poly_str)
    
    for sreg in range(4):
        sreg_str=int2bin(sreg,len(poly_str)-1)
        
        for data in range(pow(2,8)):
            data_str=int2bin(data,8)
            old=bin2dec(crc_compute(data_str,poly_str,sreg_str))
            new=crc_compute_int(data,8,poly,sreg)
    #        if old!=new:
            print "data: %i, new: %i, old: %i (sreg: %i)"%(data,new,old,sreg)
        print "done"
        
if __name__ == '__main__' and False:
    input=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    input=[1,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0]
    print "crc magna", crc3_magna(input)

if __name__ == '__main__':
    #example for crc3
    poly="1011"
    sreg="000"
    data="111100111011111100000" #21 data bits
    data="000000000000000000000"
    crc3=crc_compute(data,poly,sreg)
    
#     data="100000110101110000000000"
    data="00000110101110000000"
    
    print len(data)
    sreg="101"
    
    
    print crc_compute(sreg+data,poly,(len(poly)-1)*"0")
    print crc_compute(data,poly,"100")
    
    print "-"
    
#    print "data:" ,data
#    print "poly:" ,poly
#    print "sreg:" ,sreg
#    print "crc3:" ,crc3
    
#    print crc3
    
    #example for crc8
    poly="101001101"
    sreg="00000000"
    
#    data="100000000000011110100000100100000011000000110000000100000001000001100000000011100000111010000101010000000000111000000010"
    data_str_default="80031C5607A09530701020600E0E85500E0200"

    data_str        ="80035D5607A09530701020600E0E85500E0200"
    data_str        ="80035C5667A09530301020600E0E85500E0209"
    data_str=data_str_default

    no_of_config_regs=19
    print "data: 0x"+data_str
    data=hex2bin(data_str,no_of_config_regs*8)
    print "data (binary): 0b"+data
    crc8=crc_compute(data,poly,sreg)
    print "b-step crc: (binary)", crc8
    
    data=hex2dec(data_str)
#    data=hex2bin("80033C5607A09530701020600E0E85500E02",18*8)
    
    crc8_int= crc_compute_int(data,no_of_config_regs*8,bin2dec(poly))
    
    print "b-step crc: 0x%X"%crc8_int
    
    
    data=hex2bin("8007A09030301010600E0E85400E02",15*8)
    crc8=crc_compute(data,poly,sreg)
    print "a-step default crc: ", crc8
    
    data=hex2dec("8007A09030301010600E0E85400E02")
    
    crc8_int= crc_compute_int(data,15*8,bin2dec(poly))
    
    print "a-step default crc 0x%X"%crc8_int



if __name__ == '__main__' and False:
    poly="1011" #crc3
    sreg="000"
    
         #123456789012345678901
    data="001010001110001000010"
    
    
#    poly="101001101" #crc8

    #make sure that poly starts with 1
    pos1_poly=poly.find("1") 
    poly=poly[pos1_poly:]
    
    poly_bitCount=len(poly)
    
    data1="1" + hex2bin("0",7) + hex2bin("d4",8) + 5*"0"
    data2="0" + hex2bin("26",7) + hex2bin("0",8) + 5*"0"
    data3="0" + hex2bin("21",7) + hex2bin("0",8) + 5*"0"
          #123456789012345678901
    data4="111111111111111111111"
    data5="1011010"
    data6="100000000000011110100000100100000011000000110000000100000001000001100000000011100000111010000101010000000000111000000010"
    data7="100000000000011110100000100100000011000000110000000100000001000001100000000011100000111010000101010000000000111000000001"
    data8=hex2dec("21")<<15
    print "%X"%data8
    data8=int2bin(data8,21)
    print data8
#    data8="100000100011000000000"
    for d in [data1,data2,data3,data4,data5,data6,data7,data8]:
        sreg="0"*(poly_bitCount-1)
        print "data: %s 0x%X"%(d,bin2dec(d))
#        print "weird crc: ", crc_weird(d+sreg)
#        print "gen crc  : ", crc_weird_general(d,poly)
#        crc=crc_ifx_weird(d,poly)
#        print "crc_ifx_weird : 0b%s 0x%s"%( crc , bin2hex(crc)) 
#        crc=crc_ifx_weird(d+len(sreg)*'0',poly)
#        print "crc_ifx_weird plus 0s: 0b%s 0x%s"%( crc , bin2hex(crc))
        crc=crc_hw_try2(d) 
        print "crc hw try2        : 0b%s 0x%s"%( crc , bin2hex(crc))
        sreg=crc_compute(d,poly,sreg)
        print "crc regular        : 0b%s 0x%s"%( sreg, bin2hex(sreg))
        crc=crc_hw_try2_generic(d,poly)
        print "crc hw try2 generic: 0b%s 0x%s"%( crc, bin2hex(crc))
    print "801805:"
    d=hex2dec("801805")
    d=d>>3
    d=int2bin(d,21)
    
    crc=crc_compute(d,poly,sreg)
    print d
    print "crc:"+crc
    
    data=bin2dec("111111111110111111111")
#    data=bin2dec("000000000000000000000")
#    data=bin2dec("0001000"*3)
    no_data_bits=21
    
    poly=bin2dec("1011")
    sreg=bin2dec("101")
    sreg=0
    
    print "new sreg: %s"%(int2bin(sreg,3))
    print "data: %s"%int2bin(data,21)
    print "crc_int: %s"%int2bin(crc_compute_int(data,no_data_bits,poly,sreg),3)
    
    print "crc_compute: %s"%crc_compute(int2bin(data,21),int2bin(poly,4),int2bin(sreg,3))
    
    i=0
    end=1<<21
    
    crc_array=[0,0,0,0,0,0,0,0]
    
    while i<end:
        data=i
        crc=crc_compute_int(data,no_data_bits,poly,sreg)
        crc_array[crc]+=1
        i+=1
    print crc_array
        
#    for i in range(1<<16):
#        d=int2bin(i,21)
#        crc_test=crc_hw_try2(d)
#        sreg="0"*(poly_bitCount-1)
#        crc_good=crc_compute(d,poly,sreg)
#        if crc_test!=crc_good:
#            print "problem detected"
