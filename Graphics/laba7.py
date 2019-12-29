import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from celluloid import Camera


class Pyramid:
    def __init__(self, a, h):
        self.a, self.h = a, h
        self.vertices = self.genVertices(a, h)
        self.polygons = self.genPolygons(self.vertices)

    def plot(self):
        fig = plt.figure(figsize=(10, 8))
        ax = plt.axes(projection='3d')
        ax.scatter3D(self.vertices[:, 0], self.vertices[:, 1], self.vertices[:, 2])
        ax.add_collection3d(
            Poly3DCollection(self.polygons, facecolors='gray', linewidths=2, edgecolors='grey', alpha=0.5))
        plt.show()

    @staticmethod
    def genVertices(a, h):
        down = np.array([
            [-a / 2, -a / 2, -h / 2],
            [a / 2, a / 2, -h / 2],
            [-a / 2, a / 2, -h / 2],
            [a / 2, -a / 2, -h / 2],
        ])
        upper = np.hstack([(down[:, :2] * 0.33), (down[:, 2] + h).reshape(4, 1)])
        return np.vstack([upper, down])

    @staticmethod
    def genPolygons(vertices):
        return np.array([
            vertices[[0, 2, 6, 4]],
            vertices[[0, 3, 7, 4]],
            vertices[[1, 2, 6, 5]],
            vertices[[1, 3, 7, 5]],
            vertices[[0, 1, 2, 3]],
            vertices[[4, 5, 6, 7]]
        ])


class Prism:
    def __init__(self, a, h):
        self.a, self.h = a, h
        self.vertices = self.genVertices(a, h)
        self.polygons = self.genPolygons(self.vertices)

    def plot(self):
        fig = plt.figure(figsize=(10, 8))
        ax = plt.axes(projection='3d')
        ax.scatter3D(self.vertices[:, 0], self.vertices[:, 1], self.vertices[:, 2], edgecolors='gray')
        ax.add_collection3d(Poly3DCollection(self.polygons, facecolors='pink', linewidths=2, edgecolors='grey', alpha=0.5))
        plt.show()

    @staticmethod
    def genVertices(a, h):
        R = a / np.sqrt(3)
        down = np.array([
            [0, R, -h / 2],
            [a / 2, pow(R, 2) - pow(a / 2, 2), -h / 2],
            [-a / 2, pow(R, 2) - pow(a / 2, 2), -h / 2],
        ])
        upper = np.hstack([(down[:, :2]), (down[:, 2] + h).reshape(-1, 1)])
        return np.vstack([upper, down])

    @staticmethod
    def genPolygons(vertices):
        return np.array([
            vertices[[0, 1, 2]],
            vertices[[3, 4, 5]],
            vertices[[0, 3, 4, 1]],
            vertices[[0, 3, 5, 2]],
            vertices[[1, 4, 5, 2]],
        ])


class Animation:
    def __init__(self, figure):
        self.fig = plt.figure(figsize=(12, 10))
        self.camera = Camera(self.fig)
        self.figure = figure

    def getMatrix(self, axis):
        mx = lambda i: np.array([
                    [1, 0, 0],
                    [0, np.cos(i), -np.sin(i)],
                    [0, np.sin(i), np.cos(i)],
                ])
        my = lambda i: np.array([
                    [np.cos(i), 0, np.sin(i)],
                    [0, 1, 0],
                    [-np.sin(i), 0, np.cos(i)],
                ])
        mz = lambda i: np.array([
                    [np.cos(i), -np.sin(i), 0],
                    [np.sin(i), np.cos(i), 0],
                    [0, 0, 1],
                ])

        if axis == 0:
            return mx
        if axis == 1:
            return my
        if axis == (0, 1):
            return lambda i: mx(i) @ my(i)
        if axis == (0, 1, 2):
            return lambda i: mx(i) @ my(i) @ mz(i)

    def animate(self, axis):
        verts = self.figure.vertices
        t = np.linspace(0, 8 * np.pi, 40)

        ax = plt.axes(projection='3d')
        ax.set_xlim(-self.figure.h, self.figure.h)
        ax.set_ylim(-self.figure.h, self.figure.h)
        ax.set_xlabel('X'), ax.set_ylabel('Y'), ax.set_zlabel('Z')

        matrix = self.getMatrix(axis)

        for i in t:
            v = verts @ matrix(i)
            ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
            p = self.figure.genPolygons(v)
            ax.add_collection3d(Poly3DCollection(p, facecolors='pink', linewidths=2, edgecolors='grey', alpha=0.5))
            ax.add_collection3d(Poly3DCollection(p[[int(i % 2), int(int(i % 2) * 2 + (i % 2))]], facecolors='red'))
            self.camera.snap()

    def save(self, path):
        anim = self.camera.animate(interval=100, blit=True)
        anim.save(path, writer='ffmpeg')


def main():
    # a, h = 4, 6
    # prism = Prism(a, h)
    # animation = Animation(prism)
    # axis = 0
    # animation.animate(axis=axis)
    # animation.save(f'/Users/macair/Desktop/pyramid{axis}axis.mp4')

    from time import time
    a, h = 4, 6

    for axis in [0, 1, (0, 1), (0, 1, 2)]:
        start = time()
        pyramid = Prism(a, h)
        animation = Animation(pyramid)
        animation.animate(axis)
        animation.save(f'/Users/macair/Desktop/pyramid{axis}axis.mp4')
        print(f'Time: {time() - start}')


main()