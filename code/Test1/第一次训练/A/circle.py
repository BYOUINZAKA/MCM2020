"""
@Author: Hata
@Date: 2020-08-02 17:26:38
@LastEditors: Hata
@LastEditTime: 2020-08-02 17:59:53
@FilePath: \MCM2020\code\Test1\第一次训练\A题 血管的三维重建\circle.py
@Description: 
"""

import random

import numpy as np

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes

from pandas import DataFrame


class InsideCircle:
    def __init__(self, pic_path: str, sample=16, precision=0.5) -> None:
        self.bitmap = mpimg.imread(pic_path)
        self.prec = precision
        self.sample_angles = np.linspace(0, 2 * np.pi, sample)

    def isInside(self, x, y) -> bool:
        try:
            return self.bitmap[int(y), int(x), 0] == 0
        except:
            return False

    def sampling(self, x: int, y: int, r: float) -> bool:
        ''' 
        取样判断越界

        @param {type} 
        @return: bool
        @todo: 可以尝试一下非均匀的随机取样
        '''

        # 在0到2π间分层取样
        # sample_angles = np.linspace(0, 2 * np.pi, self.sample)
        for a in self.sample_angles:
            target = (x + r * np.cos(a), y + r * np.sin(a))

            # 只要有一个点出界这个圆一定不在图形内
            # 只有所有点都处于图形内这个圆才在图形内
            if not self.isInside(*target):
                return False

        return True

    def findInsideCircle(self, x: float, y: float):
        ''' 
        计算以一点为圆心的内接圆

        @param {type} 
        @return: int
        '''
        if not self.isInside(x, y):
            return -1

        # 初始上下界，上界为图的最大像素数
        min_r, max_r = 0.0, float(np.min([x - 0, 512 - x, y - 0, 512 - y]))

        # 规定一个临界值，如果最大半径和最小半径的差小于这个临界值时，我们视为两个值相等，不再循环。
        while max_r - min_r >= self.prec:

            # 每次取上下界的中间值进行检测
            mid_r = (min_r + max_r) / 2

            # 开始取样，查看以mid_r为半径的圆是否被包含在图形中
            # 如果包含，说明内切圆的半径一定大于等于mid_r，mid_r以下的半径我们就不用检查了，于是把下界提升到mid_r
            if self.sampling(x, y, mid_r):
                min_r = mid_r
            # 如果不包含，说明内切圆的半径一定小于等于mid_r，于是我们把上界降低到mid_r
            else:
                max_r = mid_r

        # min_r 和 max_r 已经在某种意义上相等了，这就是内切圆半径
        return min_r

    def findMaxInsideCircle(self):
        res = (-1, -1, -1)
        y = 0
        for i in self.bitmap:
            x = 0
            for j in i:
                if self.isInside(x, y):
                    r = self.findInsideCircle(x, y)
                    if r > res[2]:
                        res = (x, y, r)
                x = x + 1
            y = y + 1
        return res

    def imageShow(self):
        plt.imshow(self.bitmap)


def posTranslate(pos: tuple):
    x, y = pos
    return (x - 256, y - 256)
    pass


if __name__ != "__main__":
    main_dir = {
        'Y': [],
        'X': [],
        'Z': [],
        'R': [],
    }
    sample = 32

    path = "code\\Test1\\第一次训练\\A\\A01bmp\\%d.bmp"
    for z in range(100):
        pic = path % z
        pixelMap = InsideCircle(pic, sample)
        x, y, r = pixelMap.findMaxInsideCircle()
        x, y = posTranslate((x, y))
        print("z = %d\nCircle center: (%d, %d)\nRadius = %f\n" % (z, x, y, r))
        main_dir['Y'].append(y)
        main_dir['X'].append(x)
        main_dir['Z'].append(z)
        main_dir['R'].append(r)

    df = DataFrame(main_dir)
    print(df)
    df.to_csv("code\\Test1\\第一次训练\\A\\circle_datas\\circles_s%d.csv" % sample)
else:
    sample = 32
    fig, ax = plt.subplots()
    pixelMap = InsideCircle("code\\Test1\\第一次训练\\A\\A01bmp\\76.bmp", sample)
    pixelMap.imageShow()
    x, y, r = pixelMap.findMaxInsideCircle()
    print("Circle center: (%d, %d)\nRadius = %f\n" % (x, y, r))
    ax.add_patch(mpathes.Circle(
        (x, y), r, color='yellow', fill=False, linewidth=1))

    plt.show()