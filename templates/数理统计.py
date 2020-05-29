'''
@Author: Hata
@Date: 2020-05-25 17:03:42
@LastEditors: Hata
@LastEditTime: 2020-05-27 19:28:37
@FilePath: \MCM2020\templates\数理统计.py
@Description: 
'''

from sklearn import linear_model
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
    '''
    @description: 例7-8
    '''
    def func(t):
        if t >= 0:
            return 0.005*np.exp(-0.005*t)
        else:
            return 0
    edges = [0, 100, 200, 300, np.inf]
    obs = np.array([121, 78, 43, 58])
    exp = np.array([integrate.quad(func, edges[i-1], edges[i])[0]*300
                    for i in range(1, len(edges))])
    return stats.chisquare(obs, exp)


def Regression():
    '''
    @description: 例7-19
    '''
    y = np.zeros((25, 1))
    x = np.zeros((25, 3))
    with open('.\\references\\司守奎 《数学建模算法与应用》\\【代码】司守奎 《数学建模算法与应用》 第二版\\07第7章 数理统计\\ex7_19.txt') as file:
        for line in file:
            array = line.rstrip().split('  ')[0].split('\t')
            i = 0
            while i < len(array):
                if i == 0 or i == 5:
                    index = int(array[i])-1
                    i = i+1
                    continue
                y[index, 0] = float(array[i])
                x[index, ] = [float(array[i+1]),
                              float(array[i+2]), float(array[i+3])]
                i = i + 4
    plt.grid()
    model = linear_model.LinearRegression()
    model.fit(x, y)
    pltx = np.arange(1, 26)
    plt.scatter(pltx, y.T[0], marker='*')
    plt.scatter(pltx, model.predict(x).T[0], marker='.')
    return model.intercept_, model.coef_
    # result = (array([0.8538775]), array([[0.0177632 , 2.07820655, 1.93958733]]))


def Regression2():
    '''
    @description: 7-5
    '''    
    x = np.array([1, 2, 4, 5, 7, 8, 9, 10])
    y = np.array([1.3, 1, 0.9, 0.81, 0.7, 0.6, 0.55, 0.4])
    x_t = np.vstack((1/x, x, x**2))
    y.shape = (len(y), 1)
    plt.grid()
    model = linear_model.LinearRegression()
    model.fit(x_t.T, y)

    def func(x):
        a1, a3, a4 = model.coef_[0]
        a2 = model.intercept_[0]
        return a1/x + a2 + a3*x + a4*x**2

    plt.scatter(x, y.T[0], marker='*', c='black')
    px = np.linspace(x[0]-0.5, x[-1]+0.5, 100)
    py = func(px)
    plt.plot(px, py)

    return "y={0:.2f}/x+{1:.2f}+{2:.2f}*x+{3:.2f}*x**2".format(model.coef_[0][0], model.intercept_[0], model.coef_[0][1], model.coef_[0][2])
    # result = "y=0.65/x+0.59+0.07*x+-0.01*x**2"


# print(Interval())
# Chisquare()
print(Regression2())
plt.show()
