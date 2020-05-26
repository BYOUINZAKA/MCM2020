'''
@Author: Hata
@Date: 2020-05-26 16:33:47
@LastEditors: Hata
@LastEditTime: 2020-05-26 22:46:53
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
            self.__data = np.asarray(data)

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

    def Build(self, choice=0) -> callable:
        data = self.__data[choice:]+self.__c
        x_1 = np.array([np.sum(data[:i+1]) for i in range(len(data))])
        z_1 = np.array([-0.5*(x_1[i-1]+x_1[i]) for i in range(1, len(data))])
        B = np.vstack((-z_1, np.ones(len(z_1)))).T
        Y = np.array(data[1:])
        a, b = np.abs((np.linalg.inv(B.T@B) @ B.T) @ Y)

        return lambda k: (data[0]-b/a)*(1-np.exp(a))*np.exp(-a*k)-self.__c

    def Generate(self, k: int, choice=0) -> np.ndarray:
        generate = self.Build(choice=choice)
        return np.array([generate(_k) for _k in range(1, k)])

    def Verify(self, genlist) -> dict:
        maxlen = min(len(self.__data), len(genlist))
        e = [self.__data[i]-genlist[i]
             for i in range(1, maxlen)]
        delta = np.abs(e/self.__data[1:maxlen])
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
            'delta_avg': delta.sum()/(maxlen-1)
        }


if __name__ == "__main__":
    data = [33.27, 43.41, 62.06, 101.72, 131.15, 170.73,
            217.69, 296.39, 440.69, 457.12, 559.11]

    data = [71.1, 72.4, 72.4, 72.1, 71.4, 72, 71.6, 71.0, 72]
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

{
    'C': 0.5158581516842807,
    'S_1': 0.2461728395061746,
    'S_2': 0.12699026598252633,
    'deltas': array([0.00301566, 0.00478461, 0.00241688, 0.00557581, 0.00457356, 0.00078892, 0.00586681, 0.009864]),
    'delta_avg': 0.004610781318595852
}
