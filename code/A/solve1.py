'''
@Author: Hata
@Date: 2020-05-30 02:04:27
@LastEditors: Hata
@LastEditTime: 2020-05-31 17:59:03
@FilePath: \MCM2020\code\A\solve1.py
@Description: 
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from data import Data
from tree import MST


def distance(p1, p2):
    if p1[0] == p2[0]:
        return 0
    x1, y1 = p1[-2:]
    x2, y2 = p2[-2:]
    return np.sqrt((x1-x2)**2+(y1-y2)**2)


if __name__ == "__main__":
    figure, ax = plt.subplots()
    data = Data('.\\code\\A\\data.csv')
    mst = MST(data.Translate('V|P'))
    lines = mst.Build(0)
    mst.Draw(ax)

    vlist = data.GetType('V')
    a = data.Get(0)
    mindis = np.Infinity
    for i in vlist:
        if mindis > distance(i, a):
            mindis = distance(i, a)
            minx, miny = i[-2:]
    ax.plot([a[-2], minx], [a[-1], miny], linewidth=1, c='red', linestyle='-.')

    dissum = lines[:, -1].sum()
    print("最小管道里程数：", mindis + dissum)

    data.Draw(ax)
    plt.show()
