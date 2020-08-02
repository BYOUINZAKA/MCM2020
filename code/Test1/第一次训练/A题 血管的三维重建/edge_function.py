import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from scipy import optimize

image = mpimg.imread("code\\Test1\\第一次训练\\A题 血管的三维重建\\A01bmp\\99.bmp")
COUNT = 256
STEP = image.shape[1] // COUNT

plt.imshow(image)

high_x, low_x = [], []
high_y, low_y = [], []


def forward(xx):
    for i in range(image.shape[0] - 1):
        if image[i, xx, 0] == 255:
            if image[i + 1, xx, 0] == 0:
                high_x.append(xx)
                high_y.append(512 - i)
        elif image[i + 1, xx, 0] == 255:
            low_x.append(xx)
            low_y.append(512 - i - 1)
            break


for i in range(COUNT):
    forward(i*STEP)

high_x = np.asarray(high_x)
high_y = np.asarray(high_y)

low_x = np.asarray(low_x)
low_y = np.asarray(low_y)


def func(x, p):
    res = 0
    j = 0
    for i in p:
        res = res + i*x**j
        j = j + 1
    return res


def dis(p, x, y):
    return func(x, p) - y

num = 4
low_p = optimize.leastsq(dis, np.ones(num), args=(low_x, low_y))[0]
high_p = optimize.leastsq(dis, np.ones(num), args=(high_x, high_y))[0]

print(high_p)
print(low_p)

x = np.arange(0, 512)
plt.plot(x, 512-func(x, low_p))
plt.plot(x, 512-func(x, high_p))

plt.show()
