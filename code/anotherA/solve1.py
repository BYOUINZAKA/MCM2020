'''
@Author: Hata
@Date: 2020-06-04 23:37:44
@LastEditors: Hata
@LastEditTime: 2020-06-05 18:43:37
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

    # 构筑一级水站和二级水站间的最小生成树。
    G = nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')
    # 筛选出距离中心水站最近的一级水站，并加入图中。
    for_add = df.BestNeighbor(center)
    G.add_edge(*for_add[:2], weight=for_add[2])

    # 绘制
    dfm.graphDraw(df, G)
    df.Draw()
    print("管道总长为%.2fm，其中一级管道总长%.2fm，二级管道总长%.2fm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
    plt.savefig('.\\code\\anotherA\\result\\solve1.png')
    plt.show()
