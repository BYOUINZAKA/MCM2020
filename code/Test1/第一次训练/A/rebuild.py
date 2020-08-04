import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from pandas import read_csv
from scipy import interpolate

ax = Axes3D(plt.figure())
df = read_csv("code\\Test1\\第一次训练\\A\\circles.csv")
ax.plot3D(df['X'], df['Y'], df['Z'], 'gray')
ax.scatter3D(df['X'], df['Y'], df['Z'], cmap='b', s=900, marker='o')

ax.set_xlim(-256, 256)
ax.set_ylim(-256, 256)
ax.set_zlim(0, 100)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

datas = read_csv("code\\Test1\\第一次训练\\A\\circles_single.csv").to_numpy().T
y, x, z = datas[1:4]

yy = np.linspace(y[0], y[-1], 2000)

ax = Axes3D(plt.figure())
fyz = interpolate.interp1d(y, z, kind='slinear')
fyx = interpolate.interp1d(y, x, kind='slinear')
ax.scatter3D(fyx(yy), yy, fyz(yy), s=900, c='gray')

ax.set_xlim(-256, 256)
ax.set_ylim(-256, 256)
ax.set_zlim(0, 100)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

'''
datas = read_csv("code\\Test1\\第一次训练\\A\\circles.csv").to_numpy().T
y, x, z = datas[1:4]

zz = np.linspace(0, 99, 1000)

ax1 = plt.subplot(221)
fzx = interpolate.interp1d(z, x, kind='slinear')
plt.scatter(zz, fzx(zz))

ax2 = plt.subplot(222)
fzy = interpolate.interp1d(z, y, kind='slinear')
plt.scatter(zz, fzy(zz))
'''

plt.show()
