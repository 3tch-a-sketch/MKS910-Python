import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from MKS910 import MKS910
import os 
import sys

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xar = []
yar = []
mks = MKS910("COM3")
mks.open()

try:
    def animate(i):
        xar.append(time.time())
        yar.append(mks.read())

        ax1.clear()
        ax1.plot(xar,yar)

    def animateRolling(i):
        xar.append(time.time())
        yar.append(mks.read())

        ax1.clear()
        ax1.plot(xar[-100:],yar[-100:])

    ani = animation.FuncAnimation(fig, animateRolling, interval=50)
    plt.show()
except KeyboardInterrupt:
    mks.close()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)