'''
@Author: Hata
@Date: 2020-05-22 17:37:52
@LastEditors: Hata
@LastEditTime: 2020-05-22 23:35:28
@FilePath: \MCM2020\templates\非线性规划.py
@Description: 
'''
import numpy as np
from scipy import optimize


def NonlinearProgramming():
    '''
    @description: 例3-2
    '''
    cons = (
        {'type': 'ineq', 'fun': lambda x: 20 - x[0] - x[1]**2 - x[2]**3},
        {'type': 'ineq', 'fun': lambda x: x[0]**2 + x[1] + x[2]**2},
        {'type': 'eq', 'fun': lambda x: -x[0] - x[1]**2 + 2},
        {'type': 'eq', 'fun': lambda x: x[1] + 2*x[2]**2 - 3}
    )

    return optimize.minimize(
        fun=lambda x: x[0]**2 + x[1]**2 + x[2]**2 + 8,
        x0=(0, 0, 0),
        method='SLSQP',
        bounds=((0, None), (0, None), (0, None)),
        constraints=cons
    )


def NonlinearGroup():
    '''
    @description: 例3-8
    '''
    def func(arg): return [
        arg[0]**2 + arg[1] - 6,
        arg[1]**2 + arg[0] - 6
    ]
    return optimize.fsolve(func, [1, 1])


def EnginesQuantify():
    '''
    @description: 3-1
    '''
    def func(x):
        return 50*x.sum() + 0.2*(x**2).sum() + 4*(3*x[0]+2*x[1]+x[2]-320)
    cons = (
        {'type': 'ineq', 'fun': lambda x: x[0] - 40},
        {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 100},
        {'type': 'ineq', 'fun': lambda x: x[0] + x[1] + x[2] - 180}
    )
    bound = (0, 100)

    return optimize.minimize(
        fun=func,
        x0=(0, 0, 0),
        method='SLSQP',
        bounds=(bound, bound, bound),
        constraints=cons
    ).get('x')  # result = [50, 60, 70]


print(EnginesQuantify())
