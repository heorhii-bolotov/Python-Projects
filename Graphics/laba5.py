import numpy as np
from matplotlib import pyplot as plt
from celluloid import Camera
import time

class Hypo:
    def __init__(self, R, r):
        self.R = R
        self.r = r
        self.t = np.arange(0, 10 * np.pi + .001, np.pi / 16)
        self.X, self.Y = self.get_hypocycloid(self.r, self.R / self.r, self.t)

    @staticmethod
    def get_hypocycloid(r, k, t):
        return r * (k - 1) * (np.cos(t) + np.cos((k - 1) * t) / (k - 1)), \
               r * (k - 1) * (np.sin(t) - np.sin((k - 1) * t) / (k - 1))

    def size(self):
        return self.t.size


class Animation:

    def __init__(self, hypos=None):
        self.hypos = hypos or []
        self.fig = plt.figure()
        self.camera = Camera(self.fig)

    def add_hypo(self, hypo):
        self.hypos.append(hypo)

    def circle_effect(self, x, y):
        t = np.linspace(0, 2 * np.pi, 100)
        x, y = 5 * np.cos(t) + x, 5 * np.sin(t) + y
        plt.plot(x, y, 'green')
        self.camera.snap()

    def salute_effect(self, x, y):
        x = np.random.randint(x - 10, x + 10, 50)
        y = np.random.randint(y - 10, y + 10, 50)
        plt.scatter(np.random.choice(x, 10), np.random.choice(y, 10), color='red', s=3)

    def animate(self, speed=1, forward=1):
        if len(self.hypos) == 1:
            hypos = self.hypos[0]
            for i in range(hypos.size()):
                plt.plot(hypos.X[: i], hypos.Y[: i], color='blue')
                self.camera.snap()
        elif len(self.hypos) == 2:
            hypos1, hypos2 = self.hypos[0], self.hypos[1]
            hypos1X, hypos1Y = hypos1.X[::], hypos1.Y[::]
            hypos2X, hypos2Y = hypos2.X[::forward], hypos2.Y[::forward]

            for i in range(0, hypos1.size(), speed):
                if np.isclose(hypos1X[i], hypos2X[i], atol=1e-08, equal_nan=False) and np.isclose(hypos1Y[i], hypos2Y[i], atol=1e-08, equal_nan=False):
                    self.circle_effect(hypos1X[i], hypos1Y[i])
                    time.sleep(2)
                    for j in range(30):
                        plt.plot(hypos1X[: i], hypos1Y[: i], '--', color='pink')
                        plt.plot(hypos2X[: i], hypos2Y[: i], '--', color='gray')
                        self.salute_effect(hypos1X[i - 2 * j], hypos1Y[i - 2 * j])
                        self.camera.snap()

                plt.plot(hypos1X[: i], hypos1Y[: i], '--', color='pink')
                plt.plot(hypos2X[: i], hypos2Y[: i], '--', color='gray')
                self.camera.snap()

    def save(self):
        anim = self.camera.animate(interval=40, blit=True)
        anim.save('/Users/macair/Desktop/hypocycloid.mp4', writer='ffmpeg')


def main():
    Ra, ra = map(int, input('a object\nEnter R, r: ').strip().split())
    Rb, rb = map(int, input('a object\nEnter R, r: ').strip().split())
    A, B = Hypo(R=Ra, r=ra), Hypo(R=Rb, r=rb)
    anim = Animation([A, B])
    speed = int(input('Enter speed from 1 to 2: '))
    forward = int(input('Enter 1 or -1 for 2object position: '))
    anim.animate(speed, forward)
    anim.save()
    """
    примеры ввода:
    первая строка радиусы для 1 обьекта  
    вторая строка радиусы для 2 обьекта  
    третья строка скорость 1/2
    четвертая где позиция движение второго обьекта (против часовой стрелки/за часовой) 1/-1
    
    19 4 
    19 4
    1
    -1
    
    19 4
    19 4
    1
    1
    
    16 3
    19 5
    2
    1
    
    """


if __name__ == '__main__':
    main()
