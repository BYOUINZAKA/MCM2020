'''
@Author: Hata
@Date: 2020-06-04 21:58:22
@LastEditors: Hata
@LastEditTime: 2020-06-05 16:01:46
@FilePath: \MCM2020\code\anotherA\dataform.py
@Description:
'''

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def euclideanDistance(p1, p2):
    x1, y1 = p1[-2:]
    x2, y2 = p2[-2:]
    return np.sqrt((x1-x2)**2+(y1-y2)**2)


class DataForm:
    ''' 数据表封装类
    封装从csv文件中读取的水站数据，并可以对其进行一定的操作。

    @Attributes:
        df{pandas.DataFrame} : 存储的数据表
    '''

    def __init__(self, path: str):
        ''' 构造函数

        @Args: 
            path{str} : 读取的csv路径
        '''
        self.df = pd.read_csv(path, encoding='utf-8')

    def Get(self, i) -> pd.DataFrame:
        ''' 读取数据表中的一行

        @Args: 
            i{int} : 所要读取的id
        @Return: pandas.DataFrame
            返回一个包含指定id行的内容的数据表
        '''
        return self.df.loc[i]

    def GetType(self, types: str) -> pd.DataFrame:
        ''' 读取某一类型的水站数据

        @Args: 
            types{str} : 所要读取的类型，格式为'X'或'X|Y|...'
        @Return: pandas.DataFrame
            返回一个包含指定类型的所有内容的数据表
        @Example: 
            dataform.Get('V') : 读取某一种类型。
            dataform.Get('A|V|P') : 读取多种类型。
        '''
        return self.df[self.df['TYPE'].str.contains(types)]

    def CheckRoute(self, i: int, j: int) -> bool:
        ''' 查看两个水站之间的管道类型

        @Args: 
            i{int}, j{int}: 管道头尾节点。
        @Return: bool
            True表示为一级管道，False表示二极管道。
        '''
        p1 = self.Get(i)
        p2 = self.Get(j)
        return (('V' in p1['TYPE']) or ('A' in p1['TYPE'])) and (('V' in p2['TYPE']) or ('A' in p2['TYPE']))

    def GetPlotList(self, i: int, j: int) -> tuple:
        p1 = self.Get(i)
        p2 = self.Get(j)
        return (p1['X'], p2['X']), (p1['Y'], p2['Y'])

    def BuildGraph(self, typeSelecter='A|V|P', dis=euclideanDistance) -> nx.Graph:
        ''' 构筑一个图
        从数据表中以O(N^2)的时间复杂度构筑一个全连通无向图。

        @Args: 
            typeSelecter{str} : 所要读取的类型，格式为'X'或'X|Y|...'，默认为所有类型
            dis{callable} : 用于计算图权重的闭包，默认为计算欧几里得距离 euclideanDistance(p1, p2)
        @Return: networkx.Graph
            返回一个包含所选数据的全连通无向图。
        '''
        graph = nx.Graph()
        form = self.GetType(typeSelecter).to_numpy()
        for i in form:
            for j in form:
                if i[0] != j[0]:
                    graph.add_edge(i[0], j[0], weight=dis(i, j))
        return graph

    def Draw(self):
        A, V, P = self.GetType('A'), self.GetType('V'), self.GetType('P')
        plt.scatter(A['X'], A['Y'], marker='+', c='black', s=100)
        plt.scatter(V['X'], V['Y'], marker='*', c='red', s=20)
        plt.scatter(P['X'], P['Y'], marker='.', c='blue', s=5)

    def Upgrade(self, i, target='V'):
        ''' 升级一个节点
        将水站i的类型升级为target。

        @Args: 
            i{int} : 要升级的id。
            target{str} : 升级的类型，默认为'V'。
        @Return: None
        '''
        self.df.loc[i, 'TYPE'] = target

    def WriteToFile(self, path: str):
        self.df.to_csv(path)


def graphDraw(dataform: DataForm, graph: nx.Graph):
    lines = []
    for i, j, dis in graph.edges.data('weight'):
        if dataform.CheckRoute(i, j):
            color = 'red'
            lw = 1
        else:
            color = 'green'
            lw = 0.5
        plotList = dataform.GetPlotList(i, j)
        lines.append(*plt.plot(*plotList, linewidth=lw,
                               c=color, linestyle='--'))
    return lines


def merge(lhs: nx.Graph, rhs: nx.Graph) -> nx.Graph:
    graph = nx.Graph()
    for i, j, dis in lhs.edges.data('weight'):
        graph.add_edge(i, j, weight=dis)
    for i, j, dis in rhs.edges.data('weight'):
        graph.add_edge(i, j, weight=dis)
    return graph


def weightStats(dataform: DataForm, graph: nx.Graph):
    route_1, route_2 = 0, 0
    for i, j, dis in graph.edges.data('weight'):
        if dataform.CheckRoute(i, j):
            route_1 += dis
        else:
            route_2 += dis
    # return {'total': route_1+route_2, 'route1': route_1, 'route2': route_2}
    return route_1+route_2, route_1, route_2


def disconnectCycle(dataform: DataForm, graph: nx.Graph, cycle: list, grade=False, minimum=False):
    cycleList = np.array(np.array(cycle)[:, :2], dtype=int)
    if minimum:
        weight = np.Infinity
    else:
        weight = 0
    for i, j in cycleList:
        if grade is None or dataform.CheckRoute(i, j) is grade:
            if minimum:
                if graph.edges[i, j]['weight'] < weight:
                    weight = graph.edges[i, j]['weight']
                    res = (i, j)
            else:
                if graph.edges[i, j]['weight'] > weight:
                    weight = graph.edges[i, j]['weight']
                    res = (i, j)
    graph.remove_edge(*res)
    return res


if __name__ == "__main__":
    df = DataForm(".\\code\\anotherA\\data.csv")
    df.Upgrade(150)
    df.Upgrade(160)

    G = nx.minimum_spanning_tree(df.BuildGraph('V|P'), algorithm='prim')
    graphDraw(df, G)

    df.Draw()
    plt.show()
