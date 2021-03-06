#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: Quasi-Newton_BFGS.py
@time: 2021/4/25 13:44
"""
from numpy.linalg import linalg

'''拟牛顿法：BFGS'''
# coding:UTF-8

from numpy import *
from numpy.ma import shape
import matplotlib.pyplot as plt

# fun
def fun(x):
    # return 100 * (x[0, 0] ** 2 - x[1, 0]) ** 2 + (x[0, 0] - 1) ** 2
    x1 = x[0,0]
    x2 = x[1,0]
    return x1 ** 2 + 4 * x2 ** 2 - 4 * x1 - 8 * x2

# gfun
def gfun(x):
    result = zeros((2, 1))
    x1 = x[0, 0]
    x2 = x[1, 0]
    result[0, 0] = 2 * x1 - 4
    result[1, 0] = 8 * x2 - 8
    return result

def bfgs(fun, gfun, x0, precision=0.01):
    result = []
    maxk = 500
    rho = 0.55
    sigma = 0.4
    m = shape(x0)[0]
    Bk = eye(m)
    k = 0
    while (k < maxk):
        gk = mat(gfun(x0))  # 计算梯度
        print(gk)
        if gk[1][0] ** 2 + gk[0][0] ** 2 < precision ** 2: break
        dk = mat(-linalg.solve(Bk, gk))
        m = 0
        mk = 0
        while (m < 20):
            newf = fun(x0 + rho ** m * dk)
            oldf = fun(x0)
            if (newf < oldf + sigma * (rho ** m) * (gk.T * dk)[0, 0]):
                mk = m
                break
            m = m + 1

        # BFGS校正
        x = x0 + rho ** mk * dk
        sk = x - x0
        yk = gfun(x) - gk
        if (yk.T * sk > 0):
            Bk = Bk - (Bk * sk * sk.T * Bk) / (sk.T * Bk * sk) + (yk * yk.T) / (yk.T * sk)

        k = k + 1
        x0 = x
        result.append(fun(x0))

    return result


if __name__ == '__main__':

    x0 = mat([[0], [0]]) # 矩阵
    result = bfgs(fun, gfun, x0, precision=0.01)

    n = len(result)
    x = arange(0, n, 1)
    y = result
    print(y)
    # for i,j in x,y:
    #     plt.plot(i,j,"r*")
    plt.plot(x,y)
    plt.title("BFGS")
    plt.show()


