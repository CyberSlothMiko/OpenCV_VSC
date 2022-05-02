import numpy as np
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import sys

plt.rcParams['toolbar'] = 'None'
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

time.sleep(1)

def animate(i):
    try:
        rightleg = open('rightleg.csv','r').read()
        leftleg = open('leftleg.csv','r').read()
        rightlegline = rightleg.split('\n')
        leftlegline = leftleg.split('\n')
    except IOError:
        print('\nEnd of Video File :D\n')
        print('============================')
        sys.exit()

    xs = []
    ys = []

    xxs = []
    yys = []

    arr1 = []
    arr2 = []

    arr3 = []
    arr4 = []

    for rightlegvalue in rightlegline:
        if len(rightlegvalue) > 1:
            x, y = rightlegvalue.split(',')
            xs.append(float(x))
            ys.append(float(y))
            arr1.append(x)
            arr2.append(y)
    
    arr1 = np.array(arr1,dtype=np.double)
    arr2 = np.array(arr2,dtype=np.double)

    for leftlegvalue in leftlegline:
        if len(leftlegvalue) > 1:
            xx, yy = leftlegvalue.split(',')
            xxs.append(float(xx))
            yys.append(float(yy))
            arr3.append(xx)
            arr4.append(yy)

    arr3 = np.array(arr3,dtype=np.double)
    arr4 = np.array(arr4,dtype=np.double)

    Line_1 = LineString(np.column_stack((arr1, arr2)))
    Line_2 = LineString(np.column_stack((arr3, arr4)))

    intersection = Line_1.intersection(Line_2)

    ax1.clear()
    ax1.plot(xs, ys)
    ax1.plot(xxs, yys)
    if intersection.geom_type == 'MultiPoint':
        ax1.plot(*LineString(intersection).xy, 'ro')
    elif intersection.geom_type == 'Point':
        ax1.plot(*intersection.xy, 'go')

    x, y = LineString(intersection).xy


    with open("steps.txt", "w") as o:
        o.write((str(len(x))))
        o.write("\n")

    fig.canvas.manager.set_window_title('Knee Intersection Graph')
    ax1.set_title("Knee Intersection Graph")    

sys.tracebacklimit = 0
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()