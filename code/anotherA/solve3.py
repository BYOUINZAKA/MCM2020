'''
@Author: Hata
@Date: 2020-06-09 17:32:49
@LastEditors: Hata
@LastEditTime: 2020-06-10 16:24:20
@FilePath: \MCM2020\code\anotherA\solve3.py
@Description: 
    在问题1基础上，假如现实中由于功率的影响，
    从一级供水站出发铺设的管道最多只能供水40公里（按从该一级供水站管道输送的总里程计算），
    但从中心供水站A出发铺设的管道供水不受此距离限制。为实现对所有供水站供水，
    需要将若干个二级供水站升级为一级供水站，但升级后从该供水站出发铺设的管道也最多只能供水40公里。
    问最少升级几个二级供水站，可实现对所有的供水站供水？
    在这种配置下铺设管道的总里程数最少是多少公里？

思路：
    在问题1的方案上，将无向图转化为以中心水站为起点的有向图。

    对水站功率做出以下解释，
    对于中心水站和一级水站来说，他们做的是把接收到的水存储并重新泵出（也就是重置功率），而经过二级水站的水就只是流过而已。
    而中心水站只能和一级水站相连，那么也就是中心水站和一级水站的直联点不受40km限制，其余的相连方式都要受到限制，
    如果不这样假设那么题目就没有意义，因为所有水站最终都是以中心水站为起点的。

    而对于本题的有向图来说：
    1、中心节点的入度永远为0
    2、设A、C为一级水站，B为二级水站，管道均为40km，那么A-->B-->C中C是没水的，而A-->B<--C中都是有水的。
    3、对于问题1方案做深度优先搜索，如果某个节点是没水的，那么以它作为根节点的子树都是没水的。
    4、如果要升级有水节点，那么应该优先升级距离无水根结点最近的节点；
    如果要升级无水节点，应该优先升级子树中中心性高的节点。（不确定）
    5、如果要升级有水节点，那么可以不用引入新管道；如果要升级无水节点，需要引入管道，但是可以断环。
    但总体上优先升级无水节点的管道开销总是更低的。
    6、升级数最少的方案可能有多个，而每个方案间的里程数也不尽相同，理论上其中一定存在一个全局最优方案，
    但按照题目的意思似乎是只要选用一个升级数最少的方案来讨论管道里程数。

    深度优先染色了一下，发现题目给的数据也太友好了，导致好几个分析都用不上，
    搜索结果是无水子树仅有一棵，而且节点数和距离都不怎么样（详情看result文件夹里的图片）
    那甚至用不着做有向图了，只需要升级与根节点相邻的节点就行了。
    升级1个水站，总里程和第一问一样。

    这个解法似乎不是这个问题的最优解，只是这个数据的最优解，我们应该需要证明升级有水节点要比升级无水节点要来的好。
'''
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import dataform as dfm


def fillWater(df, G, driedRoots=[], begin=None, end=0, power=np.Infinity):
    # 深度优先搜索，同时对节点染色，如果水流经一级节点还>=0的话，就重置为40，小于0时说明到头了，记录节点后返回。
    if power < 0:
        driedRoots.append(end)
        return
    if 'V' in df.GetType(end):
        power = 40.0
    G.nodes[end]['power'] = power
    for key in G[end]:
        if key is not begin:
            fillWater(df, G, driedRoots, end, key,
                      power - G[end][key]['weight'])


if __name__ == "__main__":
    center = 0
    df = dfm.DataForm(".\\code\\anotherA\\data.csv")

    G = nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')
    for_add = df.BestNeighbor(center)
    G.add_edge(*for_add[:2], weight=for_add[2])

    # 初始化节点权重。
    for i in G.nodes:
        G.nodes[i]['power'] = -1
    # 染色
    driedRoots = []
    fillWater(df, G, driedRoots)
    
    dfm.graphDraw(df, G)
    plt.savefig('.\\code\\anotherA\\result\\solve3_distance_compute.png')

    plt.clf()

    # 将无水树根节点的最近有水节点升级。
    node = driedRoots[0]
    for i in G[node]:
        if G.nodes[i]['power'] >= 0:
            df.Upgrade(i)
            break
    msg = df.Get(node)
    print("需要升级位于 (%d, %d) 处的 %d 号水站。" % (msg['X'], msg['Y'], i))

    # 再染一次色。
    fillWater(df, G)

    dfm.graphDraw(df, G)
    plt.savefig('.\\code\\anotherA\\result\\solve3.png')
    plt.show()
