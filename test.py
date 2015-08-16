import sys,serial,time
ser=serial.Serial(17,baudrate=115200,timeout=.01)
ser.close()
ser.open()
s="up"
c="e23a$"
s=s+c
p=ser.read(1)
print p
for i in range(0,len(s)):
	print s[i]
	ser.write(s[i])
	time.sleep(.01)
time.sleep(.1)
f=ser.readline()
print f,len(f)

