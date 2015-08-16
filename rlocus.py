from control import matlab
import matplotlib.pyplot as plt
num=[.04147]
den = [1 -.7408]
rl=matlab.rlocus(matlab.tf(num,den),klist=None)
#plt.plot(rl)
print rl