'''
@Author: Hata
@Date: 2020-06-04 21:39:29
@LastEditors: Hata
@LastEditTime: 2020-06-04 22:01:44
@FilePath: \MCM2020\code\A\gratest.py
@Description: 
'''

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from data import Data


def distance(p1, p2):
    if p1[0] == p2[0]:
        return 0
    x1, y1 = p1[-2:]
    x2, y2 = p2[-2:]
    return np.sqrt((x1-x2)**2+(y1-y2)**2)

def add(G, p1, p2):
    G.add_edge(p1, p2, weight=distance(p1, p2))

data = Data('.\\code\\A\\data.csv')
G = nx.Graph()
add(G, ("A1", 5, 7), ("V1", 7, 2))
add(G, ("V1", 7, 2), ("V2", 17, 32))
add(G, ("V1", 7, 2), ("V3", 8, 20))
nx.draw(G, with_labels=True, font_weight='bold')
print(G.edges().data('weight'))
plt.show()
