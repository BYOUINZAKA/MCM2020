'''
@Author: Hata
@Date: 2020-06-04 23:37:44
@LastEditors: Hata
@LastEditTime: 2020-06-05 12:39:01
@FilePath: \MCM2020\code\anotherA\solve1.py
@Description: 
'''
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import dataform as dfm

if __name__ == "__main__":
    center = 0

    df = dfm.DataForm(".\\code\\anotherA\\data.csv")
    G = nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')
    centralNeighbors = df.BuildGraph('A|V')[center]

    minWeight = np.Infinity
    for key in centralNeighbors:
        if centralNeighbors[key]['weight'] < minWeight:
            minWeight = centralNeighbors[key]['weight']
            target = key
    G.add_edge(center, target, weight=minWeight)

    dfm.graphDraw(df, G)
    df.Draw()
    print("管道总长为%.2fm，其中一级管道总长%.2fm，二级管道总长%.2fm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
    plt.show()
