import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from pandas import read_csv
from scipy import interpolate

def setAx(ax):
    ax.set_xlim(-256, 256)
    ax.set_ylim(-256, 256)
    ax.set_zlim(0, 100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

ax = Axes3D(plt.figure())
df = read_csv("code\\Test1\\第一次训练\\A\\circles.csv")

ax.plot3D(df['X'], df['Y'], df['Z'], 'gray')
ax.scatter3D(df['X'], df['Y'], df['Z'], cmap='b', s=900, marker='o')

setAx(ax)

datas = read_csv("code\\Test1\\第一次训练\\A\\circles.csv").to_numpy().T
y, x, z = datas[1:4]

yy = np.linspace(y[0], y[-1], 2000)

ax = Axes3D(plt.figure())
fyz = interpolate.interp1d(y, z, kind='slinear')
fyx = interpolate.interp1d(y, x, kind='slinear')
ax.scatter3D(fyx(yy), yy, fyz(yy), s=900, c='gray')

setAx(ax)

plt.show()
