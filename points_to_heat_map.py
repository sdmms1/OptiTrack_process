import csv
import time
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

day = "second"
size = 300
frq = 60
actions = ["jumpj", "jumpp", "sit", "squat", "throw", "push", "wave", "walk"]


def get_index(arr, name):
    return np.where(arr == name)[0]


def get_max(points):
    MX, MY, MZ = 0, 0, 0
    mx, my, mz = 0, 0, 0
    for e in points:
        MX, MY, MZ = max(MX, max(e[0])), max(MY, max(e[2])), max(MZ, max(e[1]))
        mx, my, mz = min(mx, min(e[0])), min(my, min(e[2])), min(mz, min(e[1]))
    print(MX, MY, MZ)
    print(mx, my, mz)


def get_points(file_name):
    m = 100 if day == "second" else 1

    with open(file_name, 'r') as file:
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
            return arr  # [frame][3][37]
        else:
            return arr[360:]


def slide(points, k=4, f=60, plain="xz"):
    select_points = points[600 * (k - 1):600 * k]
    length = len(select_points)
    # print(length)
    slided = []
    d = length / f
    for i in range(f):
        idx = int(d * i)

        if plain == "xy":
            slided.append([select_points[idx][2], select_points[idx][0]])
        else:
            slided.append([select_points[idx][1], select_points[idx][0]])

    print(len(slided))
    return slided


def rec2square(arr):
    d = [(arr[0] + arr[1]) // 2, (arr[2] + arr[3]) // 2, max(arr[1] - arr[0], arr[3] - arr[2]) // 2]
    result = [d[0] - d[2] - 5, d[0] + d[2] + 5, d[1] - d[2] - 5, d[1] + d[2] + 5]
    if result[0] < 0:
        result[0], result[1] = 0, 2 * d[2] + 10
    if result[1] >= 600:
        result[0], result[1] = 589 - 2 * d[2], 599
    if result[2] < 0:
        result[2], result[3] = 0, 2 * d[2] + 10
    if result[3] >= 600:
        result[2], result[3] = 589 - 2 * d[2], 599
    return result


def get_useful_region(img):
    idx = np.where(img != 0)
    try:
        r = [idx[0].min(), idx[0].max(), idx[1].min(), idx[1].max()]
    except Exception:
        return [255, 0, 255, 0]
    # print(r)
    return rec2square(r)


def generate_heat_map(slided, path=""):
    spots_pic = np.zeros((len(slided), size * 2, size * 2), dtype=np.uint8)
    heat_maps = []
    r = [255, 0, 255, 0]
    for i in range(len(slided)):
        for j in range(len(slided[i][0])):
            spots_pic[i][round(slided[i][0][j]) + size][round(slided[i][1][j]) + size] += 200
        spots_pic[i] = cv2.flip(spots_pic[i], 0)

        spots_pic[i] = cv2.GaussianBlur(spots_pic[i], (5, 5), 10)
        # spots_pic[i] = (spots_pic[i] != 0) * 255
        # # cv2.imshow("1", spots_pic[1])
        blur_img = cv2.GaussianBlur(spots_pic[i], (101, 101), 3)
        # # cv2.imshow("2", spots_pic[1])
        cv2.normalize(blur_img, blur_img, 255, 0, cv2.NORM_MINMAX)
        # # cv2.imshow("3", blur_img)

        # 生成rgb
        # heat_map = cv2.applyColorMap(blur_img, cv2.COLORMAP_JET)
        # 生成灰度图
        heat_map = blur_img

        tr = get_useful_region(heat_map)
        r = [min(tr[idx], r[idx]) if idx % 2 == 0 else max(tr[idx], r[idx]) for idx in range(4)]

        heat_maps.append(heat_map)

    # spots_pic[4] = cv2.GaussianBlur(spots_pic[4], (5, 5), 10)
    # spots_pic[4] = (spots_pic[4] != 0) * 255
    # # cv2.imshow("1", spots_pic[1])
    # blur_img = cv2.GaussianBlur(spots_pic[4], (101, 101), 3)
    # # cv2.imshow("2", spots_pic[1])
    # cv2.normalize(blur_img, blur_img, 255, 0, cv2.NORM_MINMAX)
    # cv2.imshow("grey", blur_img)
    # heat_map = cv2.applyColorMap(blur_img, cv2.COLORMAP_JET)  # 注意此处的三通道热力图是cv2专有的GBR排列
    # cv2.imshow("rgb", heat_map)

    # r = get_useful_region(blur_img)
    # en_blur_img = blur_img[r[0]: r[1], r[2]: r[3]]
    # cv2.imshow("useful_grey", en_blur_img)
    # en_heat_map = cv2.applyColorMap(en_blur_img, cv2.COLORMAP_JET)  # 注意此处的三通道热力图是cv2专有的GBR排列
    # cv2.imshow("useful_rgb", en_heat_map)

    r = rec2square(r)
    for i in range(len(heat_maps)):
        cv2.imwrite(path + "/%d.jpg" % (i + 1), heat_maps[i][r[0]:r[1], r[2]:r[3]])

    cv2.waitKey()

    return heat_maps


def generate_test(path):
    points = get_points(path)
    slided = slide(points)
    generate_heat_map(slided)


def generate(day, action, idx):
    data_path = "dataset/data/%s/%s/%s.csv" % (day, action, idx)
    dst_dir = "dataset/heat_map/%s" % action
    print(data_path)
    print(dst_dir)

    points = get_points(data_path)

    for i in range(1, 5):
        n = len(os.listdir(dst_dir)) + 1
        dst_path = dst_dir + "/%d" % n
        os.mkdir(dst_path)
        os.mkdir(dst_path + "/horizontal")
        os.mkdir(dst_path + "/vertical")

        slided = slide(points, k=i, f=frq, plain="xy")
        generate_heat_map(slided, dst_path + "/horizontal")

        slided = slide(points, k=i, f=frq, plain="xz")
        generate_heat_map(slided, dst_path + "/vertical")


# def get_gif(file_name):
#     points = get_points(file_name)
#     arrs = generate_heat_map(slide(points))
#     print(len(arrs))
#     ani = animation.FuncAnimation(fig=fig, func=update, frames=arrs, interval=100)
#     ani.save(file_name.split("/")[-1].split(".")[0] + ".gif")
#
# def update(f):
#     # pc = ax.pcolor(f[:, :], cmap='jet', norm=norm)
#     pc = ax.pcolormesh(f, cmap='jet')
#     return pc

if __name__ == '__main__':
    # 热力图生成测试
    # generate_test("dataset/data/second/jumpj/14.csv")

    # 生成所有数据热力图
    for action in actions:
        if action not in ["sit"]:
            continue
        try:
            os.mkdir("dataset/heat_map/%s" % action)
        except Exception:
            pass
        # print(action)
        for i in range(40):
            generate(day, action, i + 1)

    # fig, ax = plt.subplots()
    # get_gif("dataset/data/second/jumpj/7.csv")
