'''
@Author: Hata
@Date: 2020-05-22 17:28:25
@LastEditors: Hata
@LastEditTime: 2020-05-26 22:38:26
@FilePath: \MCM2020\templates\整数规划.py
@Description: 
'''
import numpy as np
from scipy import optimize


def Assignment():
    '''
    @description: 例2-7
    '''    
    assignmentMatrix = np.array([
        [3, 8, 2, 10, 3],
        [8, 7, 2, 9, 7],
        [6, 4, 2, 7, 5],
        [8, 4, 2, 3, 5],
        [9, 10, 6, 9, 10]
    ])
    r, c = optimize.linear_sum_assignment(assignmentMatrix, maximize=False)
    return assignmentMatrix[r, c].sum()  # result = 21


print(Assignment())
