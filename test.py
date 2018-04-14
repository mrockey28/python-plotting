import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

N1=100000
N2=100000
BR1 = 1.82
BR2 = 2.01
DR = 0.78
Y=2000
x = []
y1 = []
y2 = []

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

while True:

    x.append(Y)
    y1.append(N1)
    y2.append(N2)

    Y = Y+1
    N1 = N1 + N1*((BR1-DR)/100)
    N2 = N2 + N2*((BR2-DR)/100)

    ax.clear()
    ax.plot(x,y1);
    ax.plot(x,y2);
    plt.draw()
    plt.pause(0.02)
    


