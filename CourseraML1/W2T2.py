"""
    Линейная алгебра: аппроксимация функций

    Рассмотрим сложную математическую функцию на отрезке [1, 15]:

    f(x) = sin(x / 5) * exp(x / 10) + 5 * exp(-x / 2)

    files: data.txt
           graph.png
           W2T2FD.py (class: file descriptor)
"""


import os
from tempfile import gettempdir
from functools import wraps
import numpy as np
from W2T2FD import File
import matplotlib.pyplot as plt


FILE_DIR = "/Users/macair/Desktop/"
FILE_NAME = "data.txt"
PHOTO_NAME = "graph.png"


class Func:
    def __init__(self, func, num, min_, max_, x_points=None):
        self.x = np.array(x_points or self.generate_x(min_, max_, num))
        self.y = self.generate_y(func, self.x)
        self.plot = Plot(func, min_, max_, min(self.y), max(self.y))

    @staticmethod
    def generate_x(min_, max_, num=None):
        return np.linspace(min_, max_, num or (max_ - min_) * 10)

    @staticmethod
    def generate_y(func, args):
        return func(args)

    @staticmethod
    def _to_pow(x, num):
        pows = [1, ]
        temp = x
        for i in range(1, num):
            pows.append(temp)
            temp *= x

        return pows

    def generate_matrix(self):
        x_len = len(self.x)
        return list(map(lambda i: self._to_pow(i, x_len), self.x)), self.y

    def generate_graph(self):
        self.plot.plot(self.x, self.y)
        self.plot.preshow()
        self.plot.show()


class Plot:
    def __init__(self, func, *args):
        self.figure, self.ax = plt.subplots(figsize=(10, 5))
        axis = list(map(lambda i: round(i, 2), args))
        self.ax.axis(axis)
        self.ax.grid()
        x = Func.generate_x(axis[0], axis[1])
        self.ax.plot(x, Func.generate_y(func, x), label='Exponential func')

    def plot(self, x, y):
        self.ax.plot(x, y, label='Approximation func')

    def preshow(self):
        self.ax.set_xlabel('x', {'fontname': 'Arial', 'size': 24})
        self.ax.set_ylabel('f(x)', {'fontname': 'Arial', 'size': 24})
        self.ax.legend(bbox_to_anchor=(1.6, 1.))

    def show(self):
        plt.savefig(os.path.join(FILE_DIR, PHOTO_NAME))
        plt.show()


def logger(*file_args):
    try:
        dir, name = file_args
    except ValueError:
        dir, name = gettempdir(), FILE_NAME

    file_path = os.path.join(dir, name)

    def wrapper(func):
        @wraps(func)
        def inner(*args):

            self, *_ = args

            if file_path.endswith(".txt"):
                try:
                    file = self.file(file_path)
                except AttributeError as err:
                    print(f"{type(self).__name__} has no attribute 'file'\n{err}")

                data = func(*args)
                file.write(" ".join(map(lambda x: str(round(x, 2)), data)), "w")

                return data

            elif file_path.endswith(".png"):
                func(*args)

            else:
                print(f"Format {file_path[-4:]} is not supported\n{ValueError}")

        return inner

    return wrapper


class Executer:

    file = File

    def __init__(self, func, *args):
        self.func = Func(func, *args)

    @logger(FILE_DIR, FILE_NAME)
    def get_factors(self):
        return np.linalg.solve(*self.func.generate_matrix()).tolist()

    @logger(FILE_DIR, PHOTO_NAME)
    def get_graph(self):
        self.func.generate_graph()


def run():

    def func(x):
        return np.sin(x / 5) * np.exp(x / 10) + 5 * np.exp(-x / 2)

    num = 4
    min_, max_ = 1, 15
    x_points = [1., 4., 10., 15.]

    executer = Executer(func, num, min_, max_, x_points)
    factors = executer.get_factors()

    print("{}".format(" ".join(map(lambda x: str(round(x, 2)), factors))))

    executer.get_graph()


if __name__ == "__main__":
    run()