
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
# from mpl_toolkits.mplot3d import Axes3D
import seaborn as sb
import pandas as pd
from scipy.optimize import linprog
# import sympy as sm

from random import randint
from math import pi, sqrt

# r = float(input("Enter R[1; h]: "))
r = 10

# generate params
fi = np.linspace(0, 2 * np.pi, 100)
R = np.linspace(0, r, 100)
fi, R = np.meshgrid(fi, R)

# generate coords
x = R * np.cos(fi)
y = R * np.sin(fi)
z = np.sqrt(x ** 2 + y ** 2)


def draw3d(r):
    """
        draw cone:
    """
    # get current axis
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')

    # plot surface
    ax.plot_surface(x, y, z, alpha=0.2, color='yellow')
    ax.plot_surface(x, np.absolute(y), z, alpha=0.1, color='red')
    surf = ax.plot_surface(x, y, np.full((100, 100), r), alpha=0.5, color='green')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    # X, Y, Z Bounds
    X, Y, Z = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()

    plt.show()

    return X, Y, Z


X, Y, Z = draw3d(r)

print(f'X bounds: {X}')
print(f'Y bounds: {Y}')
print(f'Z bounds: {Z}')


def find_min(*args):
    import time
    start = time.time()
    c, A_ub, b_ub, A_eq, b_eq = args
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
    stop = time.time()
    return stop - start, res

# 2. Find Global Extremum - global minimum
search_time, res = find_min([r, r], [[r, r], ], [r], [[r, r], ], [Z[0]])
print(f'Time: {search_time}')
extr_x, extr_y = res.x
print(f'Global min:\n\tx = {extr_x:.16f}, y = {extr_y:.16f}, z = {Z[0]}')


def draw3dZ(x, y, z):
    """
        draw cone:
    """
    # get current axis
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')

    # 1. Plot surface by z value
    surf = ax.plot_surface(x, y, z, alpha=0.5, cmap=cm.coolwarm)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.show()


draw3dZ(x, y, z)


def drawCuts(r, fi, x, y, z):
    # Additional functions
    def genCutY():
        z1 = np.linspace(0, r, 100)
        x1 = np.concatenate((z1, z1 * (-1)), axis=0)
        z1 = np.tile(z1, 2)
        y1 = np.zeros(x1.shape)
        return x1, y1, z1

    def genCutX():
        z1 = np.linspace(0, r, 100)
        y1 = np.concatenate((z1, z1 * (-1)), axis=0)
        z1 = np.tile(z1, 2)
        x1 = np.zeros(y1.shape)
        return x1, y1, z1

    # draw x y
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, z, alpha=0.2, color='yellow')
    ax.plot_surface(x, y, np.full(x.shape, r), alpha=0.3, color='yellow')

    x1, y1, z1 = genCutY()
    ax.plot(x1, y1, z1, lw=5, linestyle='--', color='blue', zorder=4)
    ax.plot(x1, y1, np.full(x1.shape, r), lw=5, linestyle='--', color='blue', zorder=4)

    x1, y1, z1 = genCutX()
    ax.plot(x1, y1, np.full(x1.shape, r), lw=5, linestyle='--', color='red', zorder=4)

    ax.plot(x[z == 10], y[z == 10], z[z == 10], lw=5, linestyle='--', color='green', zorder=4)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.show()


drawCuts(r, fi, x, y, z)


def showDistribution(x, y, z):
    # 4. Pair Distribution
    dataset = pd.DataFrame({'x': x.ravel(), 'y': y.ravel(), 'z': z.ravel()})
    sb.pairplot(dataset)
    plt.show()


showDistribution(x, y, z)