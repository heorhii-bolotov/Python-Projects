"""
    Нарисовать гипоциклоиду:
        x = r * (k - 1) * (cos(t) + cos((k - 1) * t) / (k -1))
        y = r * (k - 1) * (sin(t) + sin((k - 1) * t) / (k -1))
    Базовая гипоциклоида: R = 19
                          r = 5
                          t = [0, Pi * n], n = 100
                          k = R / r = 19 / 5
    Второй слой:  R = 4
                  r = 2.5
                  t = [0, Pi * n], n = 50
                  k = R / r = 8 / 5
    Третий слой: R = 11
                 r = 3
                 t = [0, Pi * n / 2], n = 20
    Эффект: рассеивание

"""

import numpy as np
import matplotlib.pyplot as plt


def get_hypocycloid(r, k, t):
    return r * (k - 1) * (np.cos(t) + np.cos((k - 1) * t) / (k - 1)), \
           r * (k - 1) * (np.sin(t) - np.sin((k - 1) * t) / (k - 1))


def plot_base(R, r, s='-'):
    t = np.linspace(0, 100 * np.pi, 100)
    k = R / r
    plt.plot(*get_hypocycloid(r, k, t), s)


def plot_second_layer(R, r, s='-'):
    k = R / r
    t = np.linspace(0, 50 * np.pi, 50)
    plt.plot(*get_hypocycloid(r, k, t), s)


def plot_last_layer(R, r, s='-'):
    k = R / r
    t = np.linspace(0, 20 * np.pi, 40)
    plt.plot(*get_hypocycloid(r, k, t), s)


def main():
    plt.figure()

    R, r, R1, r1, R2, r2 = [0] * 6

    flag = input("You want enter your params? ")
    if flag == 'yes':
        R = float(input("R for base: "))
        r = float(input("r for base: "))
        R1 = float(input("R1 for second layer: "))
        r1 = float(input("r1 for second layer: "))
        R2 = float(input("R2 for the last layer: "))
        r2 = float(input("r2 for the last layer: "))

    # Base hypocycloid
    plt.subplot(221)
    plot_base(R=R or 19, r=r or 5)
    plt.title('Base hypocycloid')
    plt.grid(True)

    # Second layer(orange)
    plt.subplot(222)
    plot_base(R=R or 19, r=r or 5)
    plot_second_layer(R=R1 or 4, r=r1 or 2.5)
    plt.title('layer(orange)')
    plt.grid(True)

    # Third layer(effect)
    plt.subplot(223)
    plot_base(R=R or 19, r=r or 5)
    plot_second_layer(R=R1 or 4, r=r1 or 2.5)
    plot_last_layer(R=R2 or 11, r=r2 or 3)
    plt.title('layer(effect)')
    plt.grid(True)

    # Square-effect
    plt.subplot(224)
    plot_base(R=R or 19, r=r or 5, s='s')
    plot_second_layer(R=R1 or 4, r=r1 or 2.5, s='s')
    plot_last_layer(R=R2 or 11, r=r2 or 3, s='s')
    plt.title('Square-effect')
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()
