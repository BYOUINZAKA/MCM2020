
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import matplotlib.image as mpimg

from scipy import interpolate
from pandas import DataFrame, read_csv
from matplotlib.collections import PatchCollection


def getSlice(df: DataFrame, h: int, r: int):
    selected = df[(df['Z'] < h + r) & (df['Z'] >= h - r)].to_numpy()[:, 1:-1]

    double_r = float(r ** 2)
    patches = []

    for y, x, z in selected:
        sub_r = np.sqrt(double_r - np.abs(h - z)**2)
        patches.append(mpathes.Circle(
            (x, -y), sub_r, color='black', fill=True, linewidth=1))

    return PatchCollection(patches)


def getSliceByInter(funcs: tuple, h: int, r: int):
    fzx, fzy = funcs
    low = 0 if h - r <= 0 else h - r
    high = 99 if h + r >= 99 else h + r

    double_r = float(r ** 2)
    patches = []

    for z in np.linspace(low, high, 200):
        x, y = fzx(z), fzy(z)
        sub_r = np.sqrt(double_r - np.abs(h - z)**2)
        patches.append(mpathes.Circle(
            (x, -y), sub_r, color='black', fill=True, linewidth=1))

    return PatchCollection(patches)

pic = 99
path = "code\\Test1\\第一次训练\\A\\A01bmp\\%d.bmp"

if __name__ == '__main__':
    fig=plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(222)
    ax.set_xbound(-256, 256)
    ax.set_ybound(-256, 256)
    plt.gca().set_aspect('equal', adjustable='box')
    ax.set_title("No treatment")

    df = read_csv("code\\Test1\\第一次训练\\A\\circles.csv")

    ax.add_collection(getSlice(df, pic, 30))

    ax = fig.add_subplot(223)
    ax.set_xbound(-256, 256)
    ax.set_ybound(-256, 256)
    plt.gca().set_aspect('equal', adjustable='box')
    ax.set_title("After interpolate")

    datas = df.to_numpy().T
    y, x, z = datas[1:4]

    fzx = interpolate.interp1d(z, x, kind='slinear')
    fzy = interpolate.interp1d(z, y, kind='slinear')

    ax.add_collection(getSliceByInter((fzx, fzy), pic, 30))

    ax = fig.add_subplot(221)
    ax.set_xbound(-256, 256)
    ax.set_ybound(-256, 256)
    plt.gca().set_aspect('equal', adjustable='box')
    ax.set_title("Origin %d.bmp" % pic)

    plt.imshow(mpimg.imread(path % pic))




plt.show()


