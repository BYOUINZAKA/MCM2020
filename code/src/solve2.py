'''
@Author: Hata
@Date: 2020-06-05 11:56:56
@LastEditors: Hata
@LastEditTime: 2020-06-14 20:56:34
@FilePath: \MCM2020\code\anotherA\solve2.py
@Description: 
    由于II型管道市场供应不足，急需减少从一级供水站出发铺设的II型管道总里程，
    初步方案是将其中两个二级供水站升级为一级供水站。问选取哪两个二级供水站，自来
    水管道应该如何铺设才能使铺设的II型管道总里程最少？相对问题1的方案，II型管道
    的总里程减少了多少公里？

思路：（不是很确定）
    为保证II型管道最短，那么便考虑优先使用I型管道。
    生成一个II型管道的最小生成树和I型管道的最小生成树，并接合在一起。
    这时候接合而成的图便会有环，环是不必要的，水站不需要两头输水，要断环。
    那么考虑题目便应该优先消除II型管道来消除环，每次消除环中最长的II型管道，
    便可以使II型管道的总长减到最小。

    对于以上操作可以发现，断环即是将环中最长的II型管道断开，那么考虑引入水站升级的情况，
    需要在升级水站后，将图中最长的II型管道包括在新的环内，这样便可以消除图中最长的II型管道了。
    那么解题方法就是需要构造一种情况：升级两个水站，并使图中出现两个环，
    两个环分别包含着图中最长和第二长的II型管道，便可以并消除它们了。

缺陷：
    除去构造图的时间，多次做深度优先搜索的时间复杂度有点高，似乎最坏情况有O(n^2)了
'''
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import dataform as dfm


def buildUncycleGraph(df, G):
    # 每次深度优先搜索时寻找一个环，并将环中最长的II型管道断开，直到图中没有环为止。
    while True:
        try:
            dfm.disconnectCycle(df, G, nx.find_cycle(G))
        except:
            break
    return G


def dfs(df, G, edge):
    # 以 i 为起点向 j 方向做深度优先搜索，直到尽头或是搜索到一级水站。
    i, j = edge[:2]

    # 终止条件1：如果搜索结果全部都是图尽头，说明i比j更接近高级水站，那么就升级j。
    if len(G[j]) <= 1:
        return True

    # 终止条件2：如果搜索到了一个高级水站，说明j距离高级水站更近，所以应该升级i。
    type_j = df.GetType(j)
    if type_j is 'A' or type_j is 'V':
        return False

    # 递归dfs。
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
        # 理论上升级节点构成的环只需要包含最长边似乎就行了，那就直接取最长边的边沿来升级。
        if dfs(df, G, (i, j)):
            df.Upgrade(j)
            upgraded = j
        else:
            df.Upgrade(i)
            upgraded = i

        uplist.append(upgraded)

        # 因为有节点升级了，所以需要添加新的I型管道。
        for_add = df.BestNeighbor(upgraded)
        G.add_edge(*for_add[:2], weight=for_add[2])

        # 添加了新管道图中就有环了，那么直接移除最长管道来断环，不需要再搜索了。
        G.remove_edge(i, j)

    return uplist


if __name__ == "__main__":
    upgradeCount = 2
    df = dfm.DataForm(".\\code\\anotherA\\data.csv")

    # 将两个最小生成树接合成一个连通图。
    G = dfm.merge(nx.minimum_spanning_tree(df.BuildGraph('A|V'), algorithm='prim'),
                  nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim'))

    dfm.graphDraw(df, G)
    plt.savefig('.\\code\\anotherA\\result\\solve2_base.png')
    plt.clf()

    # dfs自动断环。
    buildUncycleGraph(df, G)
    # 升级2个处于最长边周围，并可以使图中出现环的节点，并断开这些环。
    uplist = smartUpgrade(df, G, upgradeCount)

    # 输出
    for i in uplist:
        msg = df.Get(i)
        print("需要升级位于 (%d, %d) 处的 %d 号水站。" % (msg['X'], msg['Y'], i))

    print("管道总长为%.2fkm，其中I型管道总长%.2fkm，II型管道总长%.2fkm。（结果保留两位小数）"
          % dfm.weightStats(df, G))
    dfm.graphDraw(df, G)
    plt.savefig('.\\code\\anotherA\\result\\solve2.png')
    plt.show()
