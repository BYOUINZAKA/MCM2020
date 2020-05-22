'''
@Author: Hata
@Date: 2020-05-22 19:07:04
@LastEditors: Hata
@LastEditTime: 2020-05-22 23:37:48
@FilePath: \MCM2020\templates\插值与拟合.py
@Description: 
'''
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate


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


HeightMeasure()
plt.show()
