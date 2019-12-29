from random import random
import numpy as np
import sympy as sm


class Distribution:
    def __init__(self):
        pass

    @staticmethod
    def rvs(n):
        return np.random.random_sample(n), np.random.random_sample(n)


class NoNameDist(Distribution):
    def __init__(self, x: float, y: float, v=1):
        super().__init__()
        self.x, self.y = x, y
        self.h = 2 * v / (x * y)
        self.X, self.Y = np.array([]), np.array([])

    def __str__(self):
        return '2var Distribution' \
               f'\ninitial params:' \
               f'\n\tx, y, ƒ(x,y) = {self.x}, {self.y}, {self.h}' \
               f'\n\tmin&max x, y= ({self.X.min():.3f},{self.X.max():.3f}), ({self.Y.min():.3f},{self.Y.max():.3f})' \
               f'\n\tMx, My = {self.Mx:.3F}, {self.My:.3F}' \
               f'\n\tDx, Dy = {self.Dx:.3F}, {self.Dy:.3F}' \
               f'\nQx, Qy: {self.Qx:.3f}, {self.Qy:.3f}' \
               f'\nCov: {self.cov:.3F}' \
               f'\ncorr coef: {self.corr:.3F}'

    def rvs(self, n=1000):
        x, y = super().rvs(n)

        def quadratic(a, b, c, func):
            D = pow(b, 2) - 4 * a * c
            if D > 0:
                x1, x2 = (-b + pow(D, 1 / 2)) / (2 * a), (-b - pow(D, 1 / 2)) / (2 * a)
                return x1 if func(x1) else x2
            elif D == 0:
                return -b / (2 * a)

        x_ = []
        for s in x:
            i = quadratic(1, - 4 / 3, (2 / 3) * s, lambda j: 0 <= j <= 2 / 3) if s <= 2 / 3 else quadratic(1, - 4 / 3, (2 - s) / 3, lambda j: 2 / 3 <= j <= 1)
            # print(i)
            x_.append(i)
        self.X = np.array(x_)
        self.Y = y

    def findM(self):
        self.Mx, self.My = self.X.mean(), self.Y.mean()

    def findD(self):
        self.Dx, self.Dy = self.X.var(), self.Y.var()

    def findQ(self):
        self.Qx, self.Qy = np.sqrt(self.Dx), np.sqrt(self.Dy),

    def findCov(self):
        self.cov = ((self.X - self.Mx) * (self.Y - self.My)).mean()

    def findCorr(self):
        self.corr = self.cov / (self.Qx * self.Qy)


def main():
    # x, y = map(float, input('Enter x, y: ').strip().split())
    # v = float(input('Enter V: '))
    # n = int(input('Enter n: '))
    x, y = 1, 1
    n = 10000
    dist = NoNameDist(x, y)
    dist.rvs(n)
    dist.findM()
    dist.findD()
    dist.findQ()
    dist.findCov()
    dist.findCorr()
    print(dist)


if __name__ == '__main__':
    main()