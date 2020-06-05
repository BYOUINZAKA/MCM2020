'''
@Author: Hata
@Date: 2020-06-04 23:37:44
@LastEditors: Hata
@LastEditTime: 2020-06-05 19:45:33
@FilePath: \MCM2020\code\anotherA\solve1.py
@Description: 
    从中心供水站A出发，自来水管道应该如何铺设才能使管道的总里程最少？
    以图形给出铺设方案，并给出I型管道和II型管道总里程数。

思路：
    相当于构筑一个最小生成树，只是中心水站只能与一级水站相接，
    那么就生成一个包含一级水站和二级水站的最小生成树，最后再加入中心水站。
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
    print("管道总长为%.2fkm，其中I型管道总长%.2fkm，II型管道总长%.2fkm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
    plt.savefig('.\\code\\anotherA\\result\\solve1.png')
    plt.show()
