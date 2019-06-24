from matplotlib import pyplot as plt
from numpy import sin, cos, pi, arcsin, sign, round
import numpy as np

t = np.arange(0, 2, 0.001)

# angle = sin(2 * pi * t); title = "sin function"
# angle = round(sin(2*pi*t)); title = "round function"
# angle = sign(sin(2*pi*t)); title = "sign function"
angle = arcsin(sin(2*pi*t)); title = "arcsin function"

plt.plot(t, angle)
plt.grid()
plt.xlim(0, 2)
plt.xlabel('time [sec]')
plt.title(title)
plt.show()
