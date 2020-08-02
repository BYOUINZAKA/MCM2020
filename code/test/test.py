'''
@Author: Hata
@Date: 2020-08-01 09:46:17
@LastEditors: Hata
@LastEditTime: 2020-08-01 10:20:46
@FilePath: \MCM2020\code\test\test.py
@Description: 
'''

import numpy as np
from scipy.optimize import minimize_scalar
from matplotlib import pyplot as plt

def f(x):
    return 0.22*np.log(1.42*x)*np.exp(-0.19*x)-2.34*np.exp(-1.07*x)-1.21*x*np.exp(-0.27*x)

res = minimize_scalar(f, bounds=(3, 4), method='bounded')
print(res)


x = np.linspace(-10, 10, 1000)

plt.plot(x, f(x))
plt.show()
