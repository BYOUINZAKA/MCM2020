import os
import re
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D


def sample(): return random.randint(0, 100) > 99


path = os.path.dirname(__file__) + "/A01bmp/"
bit_size, bit_color = 1, 'black'
pos_range = (-256, 256)

ax = Axes3D(plt.figure())

X, Y, Z = [], [], []

for pic in os.listdir(path):
    if not os.path.isdir(pic):
        print(pic)

        z = int(re.findall(r'\d+', pic)[0])
        y = pos_range[0]

        for i in mpimg.imread(path+pic):
            x = pos_range[0]
            for j in i:
                if j[0] == 0 and sample():
                    X.append(x)
                    Y.append(y)
                    Z.append(z)
                x = x + 1
            y = y + 1

print("Points count: %d" % len(X))

ax.scatter3D(X, Y, Z, s=bit_size, c=bit_color)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
