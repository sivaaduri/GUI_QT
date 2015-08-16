import serial, os, sys , traceback
from string import atoi

class OIKOS: 
	def __init__(self):
		self.c=0
		
		self.ser.close()
		self.connect()
	def connect(self):
		print "I am here"
		try:
			self.c=1
			self.ser=serial.Serial(17,baudrate=9600,timeout=1)
			self.angle=0
			self.ser.write("1")
			c=ser.read(6)
			print "going to loop"
			for i in range(0,6):
				print ord(c[i]),i,"loop"
			print c
			if((ord(c[2])==92)):
				if((ord(c[3])==110)):
					x=0b0000;
					x=ord(c[1]);
					print x
					x=x<<8|ord(c[0])
					print x,hex(x)
					q="i am here"
					print q
			ser.close()
		except:
			self.c=0
			traceback.print_exc(file=sys.stdout)
	def update(self):
		try:
			self.ser.open()
			self.ser.close()
			self.ser.open()
			self.ser.write("1")
			self.c=1
		except:
			self.c=0 
        #read_val = ser.read(57)
		#rvh=read_val.encode('hex')
		self.rvh=[0]*20
        
		for i in range(0,20):
			self.rvh[i]=self.ser.read().encode('hex')
		ang=self.rvh[0]
		ang2=self.rvh[1]
		ang3=str(ang2)+str(ang)
		self.angle=(atoi(ang3,base=16))
		print self.rvh

