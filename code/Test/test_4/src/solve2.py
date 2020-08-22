import numpy as np
import pandas as pd

from matplotlib import pyplot as plt


def plane_wave(t, n, d):
    o = d / 8
    u = t + d / 2

    base = 1/(np.sqrt(2*np.pi)*o)
    two_o2 = 2*o**2

    def func(x):
        return base*np.exp(-(x-u)**2/two_o2)

    return n*func(X)


def get_plane_list(df: pd.DataFrame):
    global time_length, to_taxi_rate

    # d = np.arange(30, 120)
    C = np.zeros(time_length)

    for t, n in df.to_numpy()[:, 1:]:
        C += plane_wave(t, n, n/2)

    return C * to_taxi_rate


def get_taxi_list(df: pd.DataFrame):
    global time_length

    delta = 30
    D = np.zeros(time_length)
    array = df.to_numpy()[:, 1:]

    for t, v in array:
        val, begin = v / delta, int(t)
        for i in range(begin, begin+delta):
            D[i] = val
    return D


def forward_iterate(in_args, out_args, args):
    D, C = in_args
    r, k, end = args
    L, T, P = out_args

    def sigmoid(x, k):
        return 1 / (1+np.exp(-k*x))

    def exp_p(x, k):
        return 1.0 if x <= 0 else np.exp(-k*x)

    next_t = 0
    while next_t < end:
        next_t = T[-1]+r*L[-1] if L[-1] >= 0 else T[-1]+r
        if next_t > end:
            break

        # next_p = sigmoid(-L[-1], k)
        P.append(exp_p(L[-1], k))

        total_d, total_c = 0, 0
        for t in range(int(T[-1]), int(next_t)+1):
            total_d += D[t]
            total_c += C[t]

        T.append(next_t)
        L.append(L[-1] + P[-1] * total_d - total_c)

    return L, T, P


time_length = 24 * 60
X = np.arange(0, time_length)

to_taxi_rate = 0.15 / 3

if __name__ == "__main__":
    taxis = pd.read_csv("code\\Test\\test_4\\taxi.csv")
    planes = pd.read_csv("code\\Test\\test_4\\plane.csv")

    D = get_taxi_list(taxis)
    C = get_plane_list(planes)

    r, k = 1, 0.02

    L, T, P = forward_iterate((D, C), ([0], [0], [1]), (r, k, X[-1]))

    plt.figure()
    plt.plot(X, D)
    plt.plot(X, C)
    plt.legend(('D(t)', 'C(t)'), loc='upper right')  
    plt.ylabel('count')
    plt.xlabel('t')

    plt.figure()
    plt.plot(T, P)
    plt.title('P(t)')
    plt.ylabel('P')
    plt.xlabel('t')

    plt.figure()
    plt.plot(T, L, c='black')
    plt.title('L(t)')
    plt.ylabel('L')
    plt.xlabel('t')

    print(f"平均每一批间隔{ len(X)/len(T) }分钟")
    plt.show()
