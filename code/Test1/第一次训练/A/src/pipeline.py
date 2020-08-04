
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
        sub_r = np.sqrt(double_r - (h - z)**2)
        patches.append(mpathes.Circle(
            (x, -y), sub_r, color='black', fill=True, linewidth=1))

    return PatchCollection(patches)

def addSubPlot(fig, num, title):
    ax = fig.add_subplot(num)
    ax.set_xbound(-256, 256)
    ax.set_ybound(-256, 256)
    plt.gca().set_aspect('equal', adjustable='box')
    ax.set_title(title)
    return ax

def showSolve(p, pic):
    df, fzx, fzy = p
    path = "code\\Test1\\第一次训练\\A\\A01bmp\\%d.bmp"
    fig=plt.figure(figsize=(6, 6))

    addSubPlot(fig, 222, "No treatment").add_collection(getSlice(df, pic, 30))

    addSubPlot(fig, 223, "After interpolate").add_collection(getSliceByInter((fzx, fzy), pic, 30))

    addSubPlot(fig, 221, "Origin %d.bmp" % pic).imshow(mpimg.imread(path % pic))

    plt.savefig("code\\Test1\\第一次训练\\A\\pic\\TEST-%d.png" % pic)


df = read_csv("code\\Test1\\第一次训练\\A\\circle_datas\\circles_s32.csv")
# df = read_csv("code\\Test1\\第一次训练\\A\\circles.csv")

y, x, z = df.to_numpy().T[1:4]
fzx = interpolate.interp1d(z, x, kind='slinear')
fzy = interpolate.interp1d(z, y, kind='slinear')

if __name__ == '__main__':
    showSolve((df, fzx, fzy), 1)
    showSolve((df, fzx, fzy), 14)
    showSolve((df, fzx, fzy), 45)
    showSolve((df, fzx, fzy), 50)
    showSolve((df, fzx, fzy), 67)
    showSolve((df, fzx, fzy), 99)


plt.show()


