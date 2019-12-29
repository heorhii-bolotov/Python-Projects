"""
    Сгенерувати 5000 значень випадкової величини з заданим законом розподілу, обчислити математичне очікування і
    середньоквадратичне відхилення
    Рівномірний 2-ступінчатий

    Закон равномерного распределения характеризуется плотностью вероятности:
        2-ступенчатое:
"""

from random import random
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import sympy as sm

sm.init_printing(use_unicode=True)


class Distribution:
    def __init__(self):
        pass

    def rvs(self, n):
        sample = np.random.random_sample(n)
        return sample


class Plotter:
    def __init__(self):
        self.figure = plt.figure(figsize=(15, 10))

    def hist(self, rng, sample):
        plt.hist(sample, range=rng, bins=30, density=False)

    def plotM(self, M):
        ymin, ymax = plt.axis()[2:]
        plt.plot(np.repeat(M, 2), np.linspace(ymin, ymax, 2), '--', linewidth=2, color='red', label='M expectancy')
        plt.annotate(f'x = {M:.2f}', xy=(M, 0), xytext=(M + 0.5, (ymax - ymin) / 10),
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    def distribution(self, a, b, c, d1, d2):
        ymin, ymax = plt.axis()[2:]

        def func(x):
            return (x - a) / (c - a) * (ymax - ymin) * d1

        plt.plot(np.linspace(a, b, 10), func(np.linspace(a, b, 10)), '-', linewidth=2, color='yellow')

        def func(x):
            return (x - b) / (c - b) * ((ymax - ymin) * d2) + (ymax - ymin) * d1

        plt.plot(np.linspace(b, c, 10), func(np.linspace(b, c, 10)), '-', linewidth=2, color='yellow')

    def show(self):
        plt.legend()
        plt.show()


class Unifrom2n(Distribution, Plotter):
    def __init__(self, a, b, c, h1, h2):
        # initialized
        super().__init__()
        self.a, self.b, self.c = a, b, c
        self.h1, self.h2 = h1, h2
        self._find_d()
        # None
        self._rvs = np.array([])
        self._theorM, self._M = np.inf, np.inf
        self._theorD, self._D = np.inf, np.inf
        self._theorQ, self._Q = np.inf, np.inf

    def __str__(self):
        return f'Uniform2n distribution' \
               f'\ninitial params:' \
               f'\n\ta, b, c = {self.a}, {self.b}, {self.c}' \
               f'\n\th1, h2 = {self.h1:.6F}, {self.h2:.6F}' \
               f'\n\td1, d2 = {self.d1:.6F}, {self.d2:.6F}' \
               f'\nmin/max: {self._rvs.min():.6f}, {self._rvs.max():.6f}' \
               f'\ntheorM/expM: {self._theorM:.6F}, {self._M:.6F}' \
               f'\ntheorD/expD: {self._theorD:.6F}, {self._D:.6F}' \
               f'\ntheorQ/expQ: {self._theorQ:.6F}, {self._Q:.6F}'

    def hist(self, rng=None, sample=None):
        super().hist((self._rvs.min(), self._rvs.max()), self._rvs)

    def plotM(self, M=None):
        super().plotM(self._theorM)

    def distribution(self, a=None, b=None, c=None, d1=None, d2=None):
        super().distribution(self.a, self.b, self.c, self.d1, self.d2)

    def _find_d(self) -> None:
        self.d1 = abs(self.b - self.a) * self.h1
        self.d2 = abs(self.c - self.b) * self.h2# 1 - self.d1
        # if not np.isclose(self.d1 + self.d2, 1):
        #     raise LookupError(f'd1 & d2 in sum must be approximately 1, given {self.d1 + self.d2}')

    def rvs(self, n):
        nums = super().rvs(n)

        self._rvs = np.where(nums <= self.d1, self.a + nums / self.h1, self.b + (nums - self.d1) / self.h2)
        # def func():
        #     for r_i in nums:
        #         if r_i < self.d1:
        #             yield self.a + r_i / self.h1
        #         elif r_i == self.d1:
        #             yield self.b
        #         elif r_i > self.d1:
        #             yield (r_i - self.d1) / self.h2 + self.b
        #         elif r_i == self.d2:
        #             yield self.c

        # self._rvs = np.array(list(func()))

    def findM(self):
        x = sm.symbols('x')
        self._theorM = sm.integrate(x * self.h1, (x, self.a, self.b)) + sm.integrate(x * self.h2, (x, self.b, self.c))
        # self._theorM = ((self.b + self.a) * self.d1) / 2 + ((self.c + self.b) * self.d2) / 2
        # self._M = self._rvs.sum() / self._rvs.size
        self._M = self._rvs.mean()

    def findD(self):
        x = sm.symbols('x')
        self._D = ((self._rvs - self._M) ** 2).sum() / self._rvs.size
        self._theorD = sm.integrate(self.h1 * (x - self._M) ** 2, (x, self.a, self.b)) + sm.integrate(
            self.h2 * (x - self._M) ** 2, (x, self.b, self.c))

    def findQ(self):
        self._theorQ = sqrt(self._theorD)
        self._Q = sqrt(self._D)


def test():
    # a, b, c = map(float, input('Enter a, b, c: ').strip().split())
    # h1, h2 = map(float, input('Enter h1, h2: ').strip().split())
    # a, b, c = 0, 4, 6
    # h1, h2 = 0.1, 0.3
    a, b, c = 16, 18, 20
    h1 = 1 / 4
    h2 = 1 / 4
    U2n = Unifrom2n(a, b, c, h1, h2)
    U2n.rvs(10000)
    U2n.findM()
    U2n.findD()
    U2n.findQ()
    print(U2n)
    U2n.hist()
    U2n.plotM()
    # U2n.distribution()
    U2n.show()


def main():
    x = sm.symbols('x')
    D = 4
    M = 18
    b = 0
    a = - M
    c = 36
    d1, d2 = sm.integrate((x - M) ** 2, (x, a, b)), sm.integrate((x - M) ** 2, (x, b, c))
    # h1, h2 = (D / 2) / d1, (D / 2) / d2
    # s1, s2 = abs(b - a) * h1, abs(c - b) * h2
    h1 = (D / 2) / d1
    h2 = (D - (D / 2)) / d2
    s1 = h1 * abs(b - a)
    s2 = h2 * abs(c - b)
    print(s1, s2)


if __name__ == '__main__':
    # main()
    test()
    # C = 36
    # h2 = lambda c: 0.99074074 / c
    # print(h2(C))
    # print(h2(C) * ((C ** 2) / 3 - 18 * C + 324))