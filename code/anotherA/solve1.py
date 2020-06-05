'''
@Author: Hata
@Date: 2020-06-04 23:37:44
@LastEditors: Hata
<<<<<<< HEAD
@LastEditTime: 2020-06-05 18:14:55
=======
@LastEditTime: 2020-06-05 12:39:01
>>>>>>> 7c0d5a655a4619ca1f5c1239af30c76d5c96e0db
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
<<<<<<< HEAD
    df = dfm.DataForm(".\\code\\anotherA\\data.csv")

    # 构筑一级水站和二级水站间的最小生成树。
    G = nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')
    # 筛选出距离中心水站最近的一级水站，并加入图中。
    for_add = df.BestNeighbor(center)
    G.add_edge(*for_add[:2], weight=for_add[2])

    # 绘制
=======

    df = dfm.DataForm(".\\code\\anotherA\\data.csv")
    G = nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')
    centralNeighbors = df.BuildGraph('A|V')[center]

    minWeight = np.Infinity
    for key in centralNeighbors:
        if centralNeighbors[key]['weight'] < minWeight:
            minWeight = centralNeighbors[key]['weight']
            target = key
    G.add_edge(center, target, weight=minWeight)

>>>>>>> 7c0d5a655a4619ca1f5c1239af30c76d5c96e0db
    dfm.graphDraw(df, G)
    df.Draw()
    print("管道总长为%.2fm，其中一级管道总长%.2fm，二级管道总长%.2fm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
<<<<<<< HEAD
    plt.savefig('.\\code\\anotherA\\result\\solve1.png')
=======
>>>>>>> 7c0d5a655a4619ca1f5c1239af30c76d5c96e0db
    plt.show()
