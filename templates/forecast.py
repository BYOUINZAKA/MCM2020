'''
@Author: Hata
@Date: 2020-05-26 16:33:47
@LastEditors: Hata
@LastEditTime: 2020-05-27 15:07:32
@FilePath: \MCM2020\templates\forecast.py
@Description:
'''

import matplotlib.pyplot as plt
import numpy as np

__all__ = ["GrayForecast"]


class GrayForecast:
    def __init__(self, data):
        self.__c = 0
        if type(data) is np.ndarray:
            self.__data = data
        else:
            self.__data = np.array(data)

    def Check(self, c=0) -> bool:
        data = self.__data+c
        n = len(data)
        lamda = [data[i-1]/data[i] for i in range(1, n)]
        x = (np.exp(-2/(n+1)), np.exp(2/(n+1)))
        for l in lamda:
            if l > x[1] or l < x[0]:
                return False
        self.__c = c
        return True

    def Build(self, choice: int) -> callable:
        data = self.__data[choice:]+self.__c
        x_1 = np.array([np.sum(data[:i+1]) for i in range(len(data))])
        z_1 = np.array([0.5*(x_1[i-1]+x_1[i]) for i in range(1, len(data))])
        B = np.vstack((z_1, np.ones(len(z_1)))).T
        Y = np.array(data[1:])
        a, b = np.abs((np.linalg.inv(B.T@B) @ B.T) @ Y)

        return lambda k: (data[0]-b/a)*(1-np.exp(a))*np.exp(-a*k)-self.__c

    def Generate(self, k: int, choice=0, generator=None) -> np.ndarray:
        if generator is None:
            generator = self.Build(choice=choice)
        return np.array([generator(_k) for _k in range(1, k)])

    def Verify(self, genList) -> dict:
        genlist = np.hstack((0, genList))   
        minlen = min(len(self.__data), len(genlist))
        e = [self.__data[i]-genlist[i]
             for i in range(1, minlen)]
        delta = np.abs(e/self.__data[1:minlen])
        xavg = self.__data.sum()/len(self.__data)
        eavg = np.sum(e)/len(e)
        s_1 = np.array([(xk - xavg)**2 for xk in self.__data]
                       ).sum()/len(self.__data)
        s_2 = np.array([(ek - eavg)**2 for ek in e]).sum()/len(e)
        return {
            'C': s_2/s_1,
            'S_1': s_1,
            'S_2': s_2,
            'deltas': delta,
            'delta_avg': delta.sum()/(minlen-1)
        }


if __name__ == "__main__":
    data = [71.1, 72.4, 72.4, 72.1, 71.4, 72, 71.6, 71.0, 70]
    plt.subplot(211)
    plt.title('X_0')
    plt.scatter(np.arange(len(data)), data)

    gray = GrayForecast(data)
    if gray.Check(2):
        lst = gray.Generate(20)
        print(lst)
        print(gray.Verify(lst))
        plt.plot(np.arange(len(lst)), lst, marker='*', color='g')

    plt.subplot(212)
    plt.title('X_1')

    x_1 = np.array([np.sum(data[:i+1]) for i in range(len(data))])
    g_1 = np.array([np.sum(lst[:i+1]) for i in range(len(lst))])
    plt.scatter(np.arange(len(x_1)), x_1)
    plt.plot(np.arange(len(g_1)), g_1, marker='*', color='g')

    plt.tight_layout()

    plt.show()
