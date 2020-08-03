import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame, read_csv

ax = Axes3D(plt.figure())

# df = read_csv("code\\Test1\\第一次训练\\A\\circle_datas\\circles_s16.csv")
df = read_csv("code\\Test1\\第一次训练\\A\\circles.csv")

ax.plot3D(df['X'], df['Y'], df['Z'], 'gray')
ax.scatter3D(df['X'], df['Y'], df['Z'], cmap='b', s=30)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()