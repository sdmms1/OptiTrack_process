import csv
import numpy as np
from parameter import *

def get_index(arr, name):
    return np.where(arr == name)[0]

def get_points(file_name):
    m = 0.001

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
                    x.append(float('inf'))
                    y.append(float('inf'))
                    z.append(float('inf'))
            temp.append(x)
            temp.append(y)
            temp.append(z)
            arr.append(temp)
        return np.array(arr)[::GAP]  # [frame][3][37]


if __name__ == '__main__':
    arr = [1,2,float('inf')]
    arr = np.array(arr)
    print(arr[2] == np.inf)
