'''
@Author: Hata
@Date: 2020-05-22 19:07:04
@LastEditors: Hata
@LastEditTime: 2020-05-23 03:24:16
@FilePath: \MCM2020\templates\插值与拟合.py
@Description: 
'''
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import constants, interpolate, optimize


def MachineProcessing():
    '''
    @description: 例5-1
    '''
    x = np.array([0, 3, 5, 7, 9, 11, 12, 13, 14, 15])
    y = np.array([0.0, 1.2, 1.7, 2.0, 2.1, 2.0, 1.8, 1.2, 1.0, 1.6])
    plt.grid()
    plt.scatter(x, y)

    ix = np.linspace(x[0], x[-1], 100)
    iy = interpolate.interp1d(x, y, kind='slinear')

    plt.plot(ix, iy(ix), c='g')
    plt.plot(ix, interpolate.splev(ix, interpolate.splrep(x, y, k=3)), c='y')
    plt.legend(['Linear', 'Interpolate_3'])


def HeightMeasure():
    '''
    @description: 例5-3
    '''
    ax = Axes3D(plt.figure())
    x = np.arange(100, 600, 100)
    y = np.arange(100, 500, 100)
    z = np.array([
        [636, 697, 624, 478, 450],
        [698, 712, 630, 478, 420],
        [680, 674, 598, 412, 400],
        [662, 626, 552, 334, 310]
    ])
    xs, ys = np.meshgrid(x, y)
    ax.scatter(np.ravel(xs), np.ravel(ys), np.ravel(z), c='b')

    ix = np.linspace(100, 500, 1000)
    iy = np.linspace(100, 400, 1000)
    iz = interpolate.interp2d(x, y, z, kind='cubic')(ix, iy)
    ix, iy = np.meshgrid(ix, iy)
    ax.plot_surface(ix, iy, iz)
    return iz.max()  # result = 719.7


def EnterpriseProfit():
    '''
    @description: 例5-6
    '''
    def dis(p, x, y):
        k, b = p
        return k*x + b - y
    plt.grid()
    x = np.arange(1990, 1997)
    y = np.array([70, 122, 144, 152, 174, 196, 202])
    plt.scatter(x, y)
    k, b = optimize.leastsq(
        dis,
        [1, 0],
        args=(x, y)
    )[0]
    x1 = np.linspace(x[0], x[-1]+2, 100)
    y1 = k*x1 + b
    plt.plot(x1, y1, c='y')
    return (k*1997+b, k*1998+b)  # result = (233.4, 253.9)


def LeastSqaure():
    '''
    @description: 习题5-3
    '''
    def dis(p, x, y):
        a, k = p
        return a*np.exp(k*x) - y
    x = np.arange(1, 9)
    y = np.array([15.3, 20.5, 27.4, 36.6, 49.1, 65.6, 87.87, 117.6])
    plt.grid()
    plt.scatter(x, y)
    a, k = optimize.leastsq(dis, (1, 1), args=(x, y))[0]
    x1 = np.linspace(x[0], x[-1], 100)
    y1 = a*np.exp(k*x1)
    plt.plot(x1, y1, c='y')
    return (a, k)  # result = (11.42, 0.29)


def TankFlow():
    times = np.array([0, 3316, 6635, 10619, 13937, 17921, 21240, 25223, 28543, 32284, 35932, 39332, 39435,
                      43318, 46636, 49953, 53936, 57254, 60574, 64554, 68535, 71854, 75021, 79254, 82649, 85968, 89953, 93270])
    level = np.array([3175, 3110, 3054, 2994, 2947, 2892, 2850, 2795, 2752, 2697, -1, -1, 3550,
                      3445, 3350, 3260, 3167, 3087, 3012, 2927, 2842, 2767, 2697, -1, -1, 3475, 3397, 3340])
    times = times / 3600
    level = constants.pi*level*0.01*28.5**2*7.481
    plt.grid()

    x = []
    y = []
    for i in range(1, len(times)):
        if level[i-1] > 0 and level[i] > 0:
            x.append((times[i]+times[i-1])/2)
            y.append(np.abs(level[i-1]-level[i])/(times[i]-times[i-1]))
    x = np.array(x)
    y = np.array(y)

    plt.scatter(x, y)

    z1 = np.polyfit(x, y, 8)
    func = np.poly1d(z1)
    xn = np.linspace(x[0], x[-1], 200)
    yn = func(xn)
    plt.plot(xn, yn)

    return func
    # result = -5.175e-06x10 + 0.0006366x9 - 0.03302x8 + 0.9382x7 - 15.89x6 + 163.8x5 - 1010x4 + 3522x3 - 6067x2 + 2632x + 1.324e+04


print(TankFlow())
plt.show()
