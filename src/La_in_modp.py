import sympy as sp
import numpy as np
from config import p, x_values, y_values, set_ga_ma

# 定义符号变量
x = sp.symbols('x')

# 计算拉格朗日基函数
def lagrange_basis(i, x_values, mod):
    numerator = 1
    denominator = 1
    xi = x_values[i]
    for j, xj in enumerate(x_values):
        if i != j:
            numerator *= (x - xj)
            denominator *= (xi - xj)
    # 计算分母的模 p 逆元
    denominator_inv = sp.mod_inverse(denominator, mod)
    return (numerator * denominator_inv) % mod

# 计算拉格朗日插值多项式
def lagrange_interpolation(x_values, y_values, mod):
    poly = 0
    for i, yi in enumerate(y_values):
        basis = lagrange_basis(i, x_values, mod)
        poly += yi * basis
        poly %= mod
    return poly

# 接受单个 x 值并返回多项式的计算结果
def test_lagrange_at_x(single_x_value):
    global p, x_values, y_values

    # 计算拉格朗日插值多项式并展开
    poly_mod_p = lagrange_interpolation(x_values, y_values, p)
    poly_expanded = sp.expand(poly_mod_p)

    # 计算单个 x 对应的多项式值（模 p）
    poly_at_x = poly_expanded.subs(x, single_x_value) % p
    #print(f"多项式在 x = {single_x_value} 时的值 (模 p): {poly_at_x}")
    return poly_at_x


