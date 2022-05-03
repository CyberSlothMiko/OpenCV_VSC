import matplotlib.pyplot as plt
from shapely.geometry import LineString
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    rightleg = open('rightleg.csv','r').read()
    leftleg = open('leftleg.csv','r').read()

    rightlegline = rightleg.split('\n')
    leftlegline = leftleg.split('\n')
    
    xs = []
    ys = []

    xxs = []
    yys = []

    for rightlegvalue in rightlegline:
        if len(rightlegvalue) > 1:
            x, y = rightlegvalue.split(',')
            xs.append(float(x))
            ys.append(float(y))
    for leftlegvalue in leftlegline:
        if len(leftlegvalue) > 1:
            x, y = leftlegvalue.split(',')
            xxs.append(float(x))
            yys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)
    ax1.plot(xxs, yys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()