'''
@Author: Hata
@Date: 2020-06-05 11:56:56
@LastEditors: Hata
@LastEditTime: 2020-06-05 18:51:41
@FilePath: \MCM2020\code\anotherA\solve2.py
@Description: 
    由于II型管道市场供应不足，急需减少从一级供水站出发铺设的II型管道总里程，
    初步方案是将其中两个二级供水站升级为一级供水站。问选取哪两个二级供水站，自来
    水管道应该如何铺设才能使铺设的II型管道总里程最少？相对问题1的方案，II型管道
    的总里程减少了多少公里？
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
    i, j = edge[:2]

    # 如果搜索结果全部都是图尽头，说明i比j更接近高级水站，那么就升级j。
    if len(G[j]) <= 1:
        return True

    # 如果搜索到了某高级水站，说明j距离高级水站更近，所以应该升级i；
    type_j = df.GetType(j)
    if type_j is 'A' or type_j is 'V':
        return False

    for key in G[j]:
        if key is not i:
            if not dfs(df, G, (j, key)):
                return False
    return True


def smartUpgrade(df, G, count):
    # 需要记录升级的节点作为返回值
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
    # 升级2个处于最长边周围，并可以使图中出现环的节点，并删除这个环。
    uplist = smartUpgrade(df, G, upgradeCount)

    for i in uplist:
        msg = df.Get(i)
        print("升级了位于 (%d, %d) 处的 %d 号水站。" % (msg['X'], msg['Y'], i))

    print("管道总长为%.2fm，其中I型管道总长%.2fm，II型管道总长%.2fm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
    df.Draw()
    dfm.graphDraw(df, G)
    plt.savefig('.\\code\\anotherA\\result\\solve2.png')
    plt.show()
