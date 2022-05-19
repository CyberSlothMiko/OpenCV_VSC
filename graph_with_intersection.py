import numpy as np
from shapely.geometry import LineString, Point, MultiPoint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import sys

plt.rcParams['toolbar'] = 'None'
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

time.sleep(1)


def animate(i):
    try:
        rightleg = open('rightleg.csv', 'r').read()
        leftleg = open('leftleg.csv', 'r').read()
        rightlegline = rightleg.split('\n')
        leftlegline = leftleg.split('\n')
    except IOError:
        print('\nEnd of Video File :D\n')
        print('============================')
        sys.exit()

    x_values = []
    rightleg_y_values = []
    leftleg_y_values = []

    for rightlegvalue in rightlegline:
        if len(rightlegvalue) > 1:
            x, y = rightlegvalue.split(',')
            x_values.append(x)
            rightleg_y_values.append(y)

    x_values = np.array(x_values, dtype=np.double)
    rightleg_y_values = np.array(rightleg_y_values, dtype=np.double)

    for leftlegvalue in leftlegline:
        if len(leftlegvalue) > 1:
            xx, yy = leftlegvalue.split(',')
            leftleg_y_values.append(yy)

    leftleg_y_values = np.array(leftleg_y_values, dtype=np.double)

    line1 = LineString(np.column_stack((x_values, rightleg_y_values)))
    line2 = LineString(np.column_stack((x_values, leftleg_y_values)))

    intersections = line1.intersection(line2)
    intersection_points = []

    for intersection in intersections:
        if type(intersection) == Point:
            intersection_points.append(intersection)
        elif type(intersection) == LineString:
            intersection_points.append(Point(intersection.coords[0]))

    intersection_points.sort(key=(lambda point: point.x))
    intersection_points = MultiPoint(intersection_points)

    ax1.clear()
    ax1.plot(x_values, rightleg_y_values)
    ax1.plot(x_values, leftleg_y_values)
    if intersection_points.geom_type == 'MultiPoint':
        ax1.plot(*LineString(intersection_points).xy, 'ro')
    elif intersections.geom_type == 'Point':
        ax1.plot(*intersections.xy, 'go')

    with open("steps.txt", "w") as o:
        o.write((str(len(intersection_points))))
        o.write("\n")

    fig.canvas.manager.set_window_title('Knee Intersection Graph')
    ax1.set_title("Knee Intersection Graph")


sys.tracebacklimit = 0
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()
