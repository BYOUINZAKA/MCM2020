'''
@Author: Hata
@Date: 2020-05-29 23:04:51
@LastEditors: Hata
@LastEditTime: 2020-06-04 08:18:56
@FilePath: \MCM2020\code\A\tree.py
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
        candidate = list(range(0, len(self.matrix)))
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
