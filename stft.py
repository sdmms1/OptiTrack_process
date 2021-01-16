import utils
import numpy as np
import cv2
from parameter import *

if __name__ == '__main__':
    points = utils.get_points("data/20210116/1.csv") #[frame][3][37]
    print(points.shape)
    points = points[:,0,:] #[frame][50]
    print(points.shape)

    vs = []
    for i in range(1, points.shape[0]):
        v = []
        for j in range(points.shape[1]):
            if points[i][j] == np.inf or points[i-1][j] == np.inf:
                continue
            d = points[i][j] - points[i-1][j]
            v.append(int(d * 120 * TIME / GAP) + MAX_V)
        vs.append(v)

    img = np.zeros((MAX_V * 2, len(vs)))
    for i in range(len(vs)):
        for j in range(len(vs[i])):
            try:
                img[vs[i][j]][i] += 10
            except Exception:
                pass

    print(img.shape)
    # cv2.imshow("stft1", img)
    cv2.imshow("stft2", cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2)))
    cv2.waitKey()
