'''
@Author: Hata
@Date: 2020-05-29 20:57:04
@LastEditors: Hata
@LastEditTime: 2020-05-30 01:23:43
@FilePath: \MCM2020\code\A\data.py
@Description: 
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Data:
    def __init__(self, path: str):
        self.DataFrame = pd.read_csv(path, encoding='utf-8')

    def Get(self, i):
        return self.DataFrame.loc[i].to_numpy()

    def GetType(self, types: str):
        return self.DataFrame[self.DataFrame['类型'].str.contains(
            types)].to_numpy()

    def Translate(self, types='[A|V|P]'):
        def distance(p1, p2):
            if p1[0] == p2[0]:
                return np.Infinity
            x1, y1 = p1[-2:]
            x2, y2 = p2[-2:]
            return np.sqrt((x1-x2)**2+(y1-y2)**2)
        pool = self.GetType(types)
        matrix = np.zeros((len(pool), len(pool)))

        def translator(i):
            return pool[int(i)]
        for i in range(0, len(pool)):
            for j in range(0, len(pool)):
                matrix[i, j] = distance(translator(i), translator(j))
        return (matrix, translator)

    def Draw(self, ax):
        A = self.GetType('A')
        V = self.GetType('V')
        P = self.GetType('P')

        ax.scatter(A['X坐标'], A['Y坐标'], marker='+', c='black', s=100)
        ax.scatter(V['X坐标'], V['Y坐标'], marker='*', c='red', s=20)
        ax.scatter(P['X坐标'], P['Y坐标'], marker='.', c='blue', s=5)


if __name__ == '__main__':
    data = Data('.\\code\\A\\data.csv')
    print(data.DataFrame)
    matrix = data.Translate('[V|P]')
    print(matrix)
    data.Draw(plt)
    plt.show()
