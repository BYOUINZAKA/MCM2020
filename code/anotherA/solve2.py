'''
@Author: Hata
@Date: 2020-06-05 11:56:56
@LastEditors: Hata
@LastEditTime: 2020-06-05 18:39:38
@FilePath: \MCM2020\code\anotherA\solve2.py
@Description: 
'''
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import dataform as dfm


def buildUncycleGraph(G):
    # 每次深度优先搜索时寻找一个环，并将环中最长的二级管道断开，直到图中没有环为止。
    while True:
        try:
            dfm.disconnectCycle(df, G, nx.find_cycle(G))
        except:
            break
    return G


def dfs(df, G, edge):
    # 以 i 为起点向 j 方向做深度优先搜索，直到尽头或是搜索到一级水站。
    # 如果搜索到了中心或者一级水站，说明j距离高级水站更近，所以应该升级i；
    # 如果搜索结果全部都是尽头，说明i比j更接近高级水站，那么就升级j。
    i, j = edge[:2]
    if len(G[j]) <= 1:
        return True
    type_j = df.GetType(j)
    if type_j is 'A' or type_j is 'V':
        return False
    for key in G[j]:
        if key is not i:
            if not dfs(df, G, (j, key)):
                return False
    return True


def smartUpgrade(df, G, count):
    uplist = []
    for _ in range(count):
        i, j = dfm.maxEdge(df, G)[:2]
        if dfs(df, G, (i, j)):
            df.Upgrade(j)
            upgraded = j
        else:
            df.Upgrade(i)
            upgraded = i
        uplist.append(upgraded)
        # 因为有节点升级了，所以需要添加新的一级管道。
        for_add = df.BestNeighbor(upgraded)
        G.add_edge(*for_add[:2], weight=for_add[2])
        # 移除最长管道。
        G.remove_edge(i, j)
    return uplist


if __name__ == "__main__":
    upgradeCount = 2
    df = dfm.DataForm(".\\code\\anotherA\\data.csv")

    # 将两个最小生成树接合成一个连通图。
    G = dfm.merge(nx.minimum_spanning_tree(df.BuildGraph('A|V'), algorithm='prim'),
                  nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim'))
    # dfs自动断环。
    buildUncycleGraph(G)
    # 升级最长边周围，并可以使图中出现环的节点，并删除环。
    uplist = smartUpgrade(df, G, upgradeCount)

    for i in uplist:
        msg = df.Get(i)
        print("升级了位于 (%d, %d) 处的 %d 号水站。" % (msg['X'], msg['Y'], i))
    
    print("管道总长为%.2fm，其中一级管道总长%.2fm，二级管道总长%.2fm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
    df.Draw()
    dfm.graphDraw(df, G)
    plt.savefig('.\\code\\anotherA\\result\\solve2.png')
    plt.show()
