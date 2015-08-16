from helper_functions import *
from crc import *

def compute_config(data):
	poly="101001101"
	sreg="00000000"
	data=data
	no_of_config_regs=19
	print "data: 0x"+data
	data=hex2bin(data,no_of_config_regs*8)
	print "data (binary): 0b"+data
	crc8=crc_compute(data,poly,sreg)
	print "b-step crc: (binary)", crc8

if __name__ == '__main__':
	data = str(raw_input("Values of 19 registers"))
	compute_config(data)