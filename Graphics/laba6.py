import numpy as np
import matplotlib.pyplot as plt
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
        ax.add_collection3d(Poly3DCollection(self.polygons, facecolors='gray', linewidths=2, edgecolors='grey', alpha=0.5))
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


class Animation:
    def __init__(self, pyramid):
        self.fig = plt.figure(figsize=(12, 10))
        self.camera = Camera(self.fig)
        self.pyramid = pyramid

    def animate(self, axis):
        verts = self.pyramid.vertices
        t = np.linspace(0, 8 * np.pi, 40)

        ax = plt.axes(projection='3d')
        ax.set_xlim(-self.pyramid.h, self.pyramid.h)
        ax.set_ylim(-self.pyramid.h, self.pyramid.h)
        ax.set_xlabel('X'), ax.set_ylabel('Y'), ax.set_zlabel('Z')

        if axis == 0:
            for i in t:
                x = verts[:, 0]
                y = verts[:, 1] * np.cos(i) + verts[:, 2] * np.sin(i)
                z = -verts[:, 1] * np.sin(i) + verts[:, 2] * np.cos(i)
                ax.scatter3D(x, y, z)
                ax.add_collection3d(Poly3DCollection(self.pyramid.genPolygons(np.column_stack((x, y, z))), facecolors='gray', linewidths=2, edgecolors='grey', alpha=0.5))
                self.camera.snap()

        elif axis == 1:
            for i in t:
                x = verts[:, 0] * np.cos(i) + verts[:, 2] * np.sin(i)
                y = verts[:, 1]
                z = -verts[:, 0] * np.sin(i) + verts[:, 2] * np.cos(i)
                ax.scatter3D(x, y, z)
                ax.add_collection3d(Poly3DCollection(self.pyramid.genPolygons(np.column_stack((x, y, z))), facecolors='gray', linewidths=2, edgecolors='grey', alpha=0.5))
                self.camera.snap()

        elif axis == 2:
            pass

        elif axis == (0, 1):
            for i in t:
                mx = np.array([
                    [1, 0, 0],
                    [0, np.cos(i), -np.sin(i)],
                    [0, np.sin(i), np.cos(i)],
                ])
                my = np.array([
                    [np.cos(i), 0, np.sin(i)],
                    [0, 1, 0],
                    [-np.sin(i), 0, np.cos(i)],
                ])
                v = verts @ (mx @ my)
                ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
                ax.add_collection3d(Poly3DCollection(self.pyramid.genPolygons(v), facecolors='gray', linewidths=2, edgecolors='grey', alpha=0.5))
                self.camera.snap()

        elif axis == (0, 1, 2):
            for i in t:
                mx = np.array([
                    [1, 0, 0],
                    [0, np.cos(i), -np.sin(i)],
                    [0, np.sin(i), np.cos(i)],
                ])
                my = np.array([
                    [np.cos(i), 0, np.sin(i)],
                    [0, 1, 0],
                    [-np.sin(i), 0, np.cos(i)],
                ])
                mz = np.array([
                    [np.cos(i), -np.sin(i), 0],
                    [np.sin(i), np.cos(i), 0],
                    [0, 0, 1],
                ])

                v = verts @ (mx @ my @ mz)
                ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
                ax.add_collection3d(Poly3DCollection(self.pyramid.genPolygons(v), facecolors='gray', linewidths=2, edgecolors='grey', alpha=0.5))
                self.camera.snap()

    def save(self, path):
        anim = self.camera.animate(interval=100, blit=True)
        anim.save(path, writer='ffmpeg')


def main():
    from time import time
    # a = int(input('Enter a: '))
    # h = int(input('Enter a: '))
    a, h = 4, 10

    for axis in [0, 1, (0, 1), (0, 1, 2)]:
        start = time()
        pyramid = Pyramid(a, h)
        animation = Animation(pyramid)
        animation.animate(axis)
        animation.save(f'/Users/macair/Desktop/pyramid{axis}axis.mp4')
        print(f'Time: {time() - start}')

main()