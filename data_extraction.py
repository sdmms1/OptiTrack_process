import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

def get_index(arr, name):
    return np.where(arr == name)[0]


def get_points(fname, day):
    m = 1000 if day == "second" else 1
    with open(fname, 'r') as file:
        data = list(csv.reader(file))
        index = get_index(np.array(data[2]), 'Marker')

        arr = []
        for i in range(7, len(data)):
            x, y, z, temp = [], [], [], []
            for j in range(len(index) // 3):
                try:
                    x.append(float(data[i][index[3 * j]]) * m)
                    y.append(float(data[i][index[3 * j + 1]]) * m)
                    z.append(float(data[i][index[3 * j + 2]]) * m)
                except Exception:
                    continue
            temp.append(x)
            temp.append(y)
            temp.append(z)
            arr.append(temp)
        if day != "second":
            return arr #[frame][3][37]
        else:
            return arr[360:]

def update_2d_xy(arr):
    ax.cla()
    ax.set_xlabel('X')
    ax.set_xlim(-3000, 3000)
    ax.set_xticks(np.arange(-3000, 3000, 1000))
    ax.set_ylabel('Y')
    ax.set_ylim(-3000, 3000)
    ax.set_yticks(np.arange(-3000, 3000, 1000))
    # ax.set_ylabel('Z')
    # ax.set_ylim(0, 3000)
    pc = ax.scatter(arr[0], arr[2], c='r')
    return pc

def update_2d_xz(arr):
    ax.cla()
    ax.set_xlabel('X')
    ax.set_xlim(-3000, 3000)
    ax.set_xticks(np.arange(-3000, 3000, 1000))
    # ax.set_ylabel('Y')
    # ax.set_ylim(-3000, 0)
    ax.set_ylabel('Z')
    ax.set_ylim(0, 3000)
    ax.set_yticks(np.arange(0, 3000, 1000))
    pc = ax.scatter(arr[0], arr[1], c='r')
    return pc


def generate_gif_2d(n, file, points, type):
    arr = []
    for i in range(len(points) // n):
        arr.append(points[i * n])
    if type == "xy":
        ani = animation.FuncAnimation(fig=fig, func=update_2d_xy, frames=arr, interval=1000 // (120 // n))
    else:
        ani = animation.FuncAnimation(fig=fig, func=update_2d_xz, frames=arr, interval=1000 // (120 // n))


    plt.show()
    ani.save(file + "_" + type + ".gif")


def update_3d(arr):
    ax.view_init(10, -155)
    ax.cla()
    ax.set_xlabel('X')
    ax.set_xlim(-3000, 3000)
    ax.set_xticks(np.arange(-3000, 3000, 1000))
    ax.set_ylabel('Y')
    ax.set_ylim(-3000, 3000)
    ax.set_yticks(np.arange(-3000, 3000, 1000))
    ax.set_zlabel('Z')
    ax.set_zlim(0, 3000)
    ax.set_zticks(np.arange(0, 3000, 1000))
    pc = ax.scatter(arr[0], arr[2], arr[1], c='r')
    return pc


def generate_gif_3d(n, file, points):
    arr = []
    for i in range(len(points) // n):
        arr.append(points[i * n])


    ani = animation.FuncAnimation(fig=fig, func=update_3d, frames=arr, interval= 1000 // (120 // n))

    plt.show()
    ani.save(file + "_xzy.gif")

day = "second"
move = "jumpj"
idx = 7
src_path = "F:\cs\group_project\code\dataset\data\%s\%s\%d"%(day, move, idx)
des_path = "F:\cs\group_project\code\dataset\\result\%s_%s_%d"%(day, move, idx)

points = get_points(src_path + ".csv", day)

fig = plt.figure()
ax = fig.add_subplot(111)
generate_gif_2d(10, des_path, points, "xz")
generate_gif_2d(10, des_path, points, "xy")

# fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")
# generate_gif_3d(2, des_path, points[360:960])
