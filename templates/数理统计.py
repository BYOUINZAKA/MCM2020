'''
@Author: Hata
@Date: 2020-05-25 17:03:42
@LastEditors: Hata
@LastEditTime: 2020-05-26 16:26:33
@FilePath: \MCM2020\templates\数理统计.py
@Description: 
'''

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats, integrate


def Interval():
    '''
    @description: 例7-1
    '''
    x = np.array([506, 508, 499, 503, 504, 510, 497, 512,
                  514, 505, 493, 496, 506, 502, 509, 496])
    return stats.norm.interval(
        0.95, loc=x.mean(), scale=stats.tsem(x))  # result = (500.7110022625732, 506.7889977374268)


def CDFProgram():
    '''
    @description: 例7-5
    '''
    with open('.\\references\\司守奎 《数学建模算法与应用》\\【代码】司守奎 《数学建模算法与应用》 第二版\\07第7章 数理统计\\ex7_5.txt') as file:
        x = np.array([int(i)
                      for line in file for i in line.rstrip().split('  ')])
    pts = plt.hist(x, bins=len(x), cumulative=True, histtype='step')


def Chisquare():
    def func(t):
        if t >= 0:
            return 0.005*np.exp(-0.005*t)
        else:
            return 0
    edges = [0, 100, 200, 300, np.inf]
    obs = np.array([121, 78, 43, 58])
    exp = np.array([integrate.quad(func, edges[i-1], edges[i])[0]*300
                    for i in range(1, len(edges))])
    print(stats.chisquare(obs, exp))


# print(Interval())
Chisquare()
