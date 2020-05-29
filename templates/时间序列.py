'''
@Author: Hata
@Date: 2020-05-27 23:56:02
@LastEditors: Hata
@LastEditTime: 2020-05-28 00:40:49
@FilePath: \MCM2020\templates\时间序列.py
@Description: 
'''
import numpy as np
import copy


def MovingAverage():
    y = np.array([533.8, 574.6, 606.9, 649.8, 705.1, 772.0,
                  816.4, 892.7, 963.9, 1015.1, 1102.7])
    minarg = (0, np.Infinity, 0)
    for N in range(4, len(y)-1):
        def func(t):
            return y[t-N:t].sum()/N
        s = np.sqrt(
            np.sum([(func(t)-y[t])**2 for t in range(N, len(y))])/(len(y)-N))
        if s < minarg[1]:
            minarg = (N, s, func(len(y)))
    return minarg  # result = (4, 150.51213020645784, 993.5999999999999)


print(MovingAverage())
