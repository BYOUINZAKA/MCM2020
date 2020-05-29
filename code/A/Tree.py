'''
@Author: Hata
@Date: 2020-05-29 23:04:51
@LastEditors: Hata
<<<<<<< HEAD
@LastEditTime: 2020-05-30 01:22:45
=======
@LastEditTime: 2020-05-30 01:19:36
>>>>>>> ea04485e8c209a4a74112f37888b38ae2a40a7b1
@FilePath: \MCM2020\code\A\Tree.py
@Description: 
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from data import Data


class MST:
    def __init__(self, datares):
        self.matrix, self.translator = datares

    def Build(self, first: int):
        lines = []
        selected = [first]
        candidate = [i for i in range(0, len(self.matrix))]
        candidate.remove(first)

        while len(candidate) > 0:
            begin, end, minl = 0, 0, np.Infinity
            for i in selected:
                for j in candidate:
                    if self.matrix[i][j] < minl:
                        minl = self.matrix[i][j]
                        begin = i
                        end = j
            
            lines.append((begin, end, minl))
            selected.append(end)
            candidate.remove(end)

        self.lines = np.array(lines)
        return self.lines

    def Draw(self, ax):
        for line in self.lines:
            begin = self.translator(line[0])
            end = self.translator(line[1])
            if (('V' in begin[1]) or ('A' in begin[1])) and (('V' in end[1]) or ('A' in end[1])):
                color = 'red'
                lw = 1
            else:
                color = 'green'
                lw = 0.5
            ax.plot((begin[-2], end[-2]), (begin[-1], end[-1]),
                    linewidth=lw, c=color, linestyle='--')


def distance(p1, p2):
    if p1[0] == p2[0]:
        return 0
    x1, y1 = p1[-2:]
    x2, y2 = p2[-2:]
    return np.sqrt((x1-x2)**2+(y1-y2)**2)


if __name__ == "__main__":
<<<<<<< HEAD
    figure, ax = plt.subplots()
    data = Data('.\\code\\A\\data.csv')
    mst = MST(data.Translate('[V|P]'))
    lines = mst.Build(0)
=======
    data = Data('.\\code\\A\\data.csv')
    mst = MST(data.Translate('[V|P]'))
    lines = mst.Build(0)
    figure, ax = plt.subplots()
>>>>>>> ea04485e8c209a4a74112f37888b38ae2a40a7b1
    mst.Draw(ax)

    vlist = data.GetType('V')
    a = data.Get(0)
    mindis = 0x3f3f3f
    for i in vlist:
        if mindis > distance(i, a):
            mindis = distance(i, a)
            minx, miny = i[-2:]
    ax.plot([a[-2], minx], [a[-1], miny], linewidth=1, c='red', linestyle='-.')

    data.Draw(ax)
    plt.show()
