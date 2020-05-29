'''
@Author: Hata
@Date: 2020-05-23 03:53:28
@LastEditors: Hata
@LastEditTime: 2020-05-25 16:45:38
@FilePath: \MCM2020\templates\微分方程建模.py
@Description: 
'''
import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
from mpl_toolkits.mplot3d import Axes3D
from scipy import integrate


def ODEWithInits():
    '''
    @description: 例6-2
    '''
    x = sy.Symbol('x')
    y = sy.Function('y')
    eq = sy.Eq(y(x).diff(x, 3)-y(x).diff(x, 2), x)
    ics = {
        y(x).subs(x, 1): 8,
        y(x).diff(x).subs(x, 1): 7,
        y(x).diff(x, 2).subs(x, 2): 4
    }
    return sy.latex(sy.simplify(sy.dsolve(eq, ics=ics)))


def ODEGroup():
    x = sy.Symbol('x')
    y, z = sy.symbols('y, z', cls=sy.Function)
    eq = (
        sy.simplify(sy.Eq(y(x).diff(x, 2)+3*z(x), sy.sin(x))),
        sy.simplify(sy.Eq(y(x).diff(x)+z(x).diff(x), sy.cos(x)))
    )
    print(sy.latex(eq))


def LorenzEquations():
    '''
    @description: 例6-10
    '''
    ax = Axes3D(plt.figure())

    def lorenz(d_list, t):
        x, y, z = d_list
        rho = 10
        beta = 28
        lamda = 8/3
        return np.array([rho*(y-x), beta*x-y-x*z, -lamda*z+x*y])

    result = integrate.odeint(func=lorenz,
                              y0=(5.0, 13.0, 17.0),
                              t=np.arange(0, 30, 0.01))
    X, Y, Z = result[:, 0], result[:, 1], result[:, 2]
    ax.plot(X, Y, Z, label='lorenz')
    ax.legend()


def BoundaryODE():
    def func(x, y):
        return np.vstack((y[1], -5*y[0]))

    def bc(ya, yb):
        return np.array([ya[0], ya[1]-1, yb[0]+yb[1]])

    x = np.linspace(0, 1, 10)
    y_a = np.zeros((2, x.size))
    y_b = np.zeros((2, x.size))
    y_b[0] = 3

    res_a = integrate.solve_bvp(func, bc, x, y_a)
    res_b = integrate.solve_bvp(func, bc, x, y_b)

    x_plot = np.linspace(0, 1, 100)
    y_plot_a = res_a.sol(x_plot)[0]
    y_plot_b = res_b.sol(x_plot)[0]
    plt.plot(x_plot, y_plot_a, label='y1')
    plt.plot(x_plot, y_plot_b, label='y2')


# print(ODEWithInits())
plt.show()
