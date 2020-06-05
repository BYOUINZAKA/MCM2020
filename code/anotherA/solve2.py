'''
@Author: Hata
@Date: 2020-06-05 11:56:56
@LastEditors: Hata
@LastEditTime: 2020-06-05 15:50:43
@FilePath: \MCM2020\code\anotherA\solve2.py
@Description: 
'''
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import dataform as dfm


def buildUncycle(G):
    # 每次深度优先搜索寻找一个环，并将环中最长的二级管道断开，直到图中没有环为止。
    while True:
        try:
            dfm.disconnectCycle(df, G, nx.find_cycle(G, orientation='ignore'))
        except:
            break
    return G


if __name__ == "__main__":
    df = dfm.DataForm(".\\code\\anotherA\\data.csv")

    # 将两个最小生成树接合成一个连通图。
    G = buildUncycle(dfm.merge(nx.minimum_spanning_tree(df.BuildGraph('A|V'), algorithm='prim'),
                               nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')))

    print("管道总长为%.2fm，其中一级管道总长%.2fm，二级管道总长%.2fm。（结果保留两位小数）"
          % dfm.weightStats(df, G))

    dfm.graphDraw(df, G)
    df.Draw()
    plt.show()
