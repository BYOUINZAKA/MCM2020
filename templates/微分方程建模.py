'''
@Author: Hata
@Date: 2020-05-23 03:53:28
@LastEditors: Hata
@LastEditTime: 2020-05-23 23:24:10
@FilePath: \MCM2020\templates\微分方程建模.py
@Description: 
'''
import sympy as sy


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


# print(ODEWithInits())
ODEGroup()
