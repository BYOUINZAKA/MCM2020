'''
@Author: Hata
@Date: 2020-05-22 16:15:38
@LastEditors: Hata
@LastEditTime: 2020-05-22 17:26:06
@FilePath: \MCM2020\template\线性规划.py
@Description: 
'''

import numpy as np
from scipy import optimize


def LinearProgramming():
    '''
    @description: 例题1-2
    '''
    c = np.array([-2, -3, 5])
    A_ub = np.array([[-2, 5, -1], [1, 3, 1]])
    b_ub = np.array([-10, 12])
    A_eq = np.array([[1, 1, 1]])
    b_eq = np.array([7])
    return optimize.linprog(c, A_ub, b_ub, A_eq, b_eq,
                            bounds=((0, None), (0, None), (0, None)))


def GoodsLoad():
    '''
    @description: 习题1-4
    '''    
    A_ub = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                     [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                     [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                     [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                     [480, 0, 0, 650, 0, 0, 580, 0, 0, 390, 0, 0],
                     [0, 480, 0, 0, 650, 0, 0, 580, 0, 0, 390, 0],
                     [0, 0, 480, 0, 0, 650, 0, 0, 580, 0, 0, 390]])
    A_eq = np.array([[8, -5, 0, 8, -5, 0, 8, -5, 0, 8, -5, 0],
                     [0, 1, -2, 0, 1, -2, 0, 1, -2, 0, 1, -2]])
    return optimize.linprog(
        c=np.array([-3100, -3100, -3100, -3800, -3800, -3800, -
                    3500, -3500, -3500, -2850, -2850, -2850]),
        A_ub=A_ub,
        b_ub=np.array([18, 15, 23, 12, 10, 16, 8, 6800, 8700, 5300]),
        A_eq=A_eq,
        b_eq=np.array([0, 0])
    )


print(GoodsLoad())
