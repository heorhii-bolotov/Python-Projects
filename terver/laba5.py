import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import matplotlib.patches as mpatches

matplotlib.style.use('ggplot')
np.set_printoptions(suppress=True)


def matrix(n_state):
    np.random.seed(0)
    m = np.random.randint(0, 10, (n_state, n_state))
    np.fill_diagonal(np.nan)
    return m


def plot(markov):
    data = markov.h_exp
    cmap = cm.viridis(np.linspace(0, 1, data.shape[1]))
    handles = []
    norm = data[::10].sum(axis=1)
    for i in range(data.shape[1]):
        plt.plot(range(0, data.shape[0], 10), data[::10, i] / norm, color=cmap[i], linewidth=3)
        handles.append(mpatches.Patch(color=cmap[i], label=f'state: {i}'))
    plt.legend(handles=handles)
    plt.xlabel('step')
    plt.ylabel('probability')
    plt.title(f'Continuous Markov chain. n={data.shape[1]}')
    # plt.axis('equal')
    plt.show()


class Markov:

    def __init__(self, m):
        self.m = m

    def __str__(self):
        return f'Experimental stationary probabilities: {self.p_exp}\n' \
               f'Theoretical stationary probabilities: {self.p_theor}\n'

    def _theoretical(self):
        m = self.m
        k = m.shape[1]

        def func(i):
            c = m[:, i]
            c[i] = -np.nansum(m[i])
            return c.tolist()

        X = np.array([np.ones(k).tolist()] + [func(i) for i in range(k - 1)])
        # a = np.linalg.inv(X)
        # print(a.shape)
        # b = np.array([1, 0, 0, 0, 0]).reshape((5, 1))
        # print(b.shape)
        # print(a @ b)
        y = np.concatenate(([1, ], np.zeros(k - 1))).reshape((-1, 1))
        self.p_theor = np.linalg.solve(X, y).flatten()

    def _experimental(self, ind, r):
        m = self.m
        T = np.zeros(m.shape[1]).tolist()
        bin = [T, ]
        for ri in r:
            t = -(1 / m[ind]) * np.log(ri)
            min_ind = np.nanargmin(t)
            T[ind] += t[min_ind]
            ind = min_ind
            bin.append(T)

        T = np.array(T)
        self.p_exp = T / T.sum()
        self.h_exp = np.array(bin)

    def find_probs(self, ind, r):
        self._experimental(ind, r)
        self._theoretical()

        if sum(self.p_exp) > 1.0001 or sum(self.p_theor) > 1.0001:
            raise LookupError


def main():
    m = np.array([
        [np.nan, 1, 0, 0, 0],
        [0, np.nan, 2, 4, 0],
        [3, 0, np.nan, 0, 5],
        [0, 0, 0, np.nan, 7],
        [0, 0, 6, 0, np.nan],
    ])
    # m = np.array([
    #     [0, 0, 0, 0, 1 / 2],
    #     [1, 0, 0, 0, 0],
    #     [0, 3 / 2, 0, 0, 0],
    #     [0, 0, 2, 0, 0],
    #     [0, 0, 0, 1, 0],
    # ])
    ind = 2  # 3 state
    r = np.random.random((1000, m.shape[1]))
    markov = Markov(m)
    try:
        markov.find_probs(ind, r)
        print(markov)
    except:
        pass
    plot(markov)


def test():
    X = np.array([
        [-1 / 2, 1, 0, 0, 0],
        [0, -1, 3 / 2, 0, 0],
        [0, 0, -3 / 2, 2, 0],
        [0, 0, 0, -2, 1],
        [1 / 2, 0, 0, 0, -1],
    ])

    y = np.array([
        [12 / 31],
        [6 / 31],
        [4 / 31],
        [3 / 31],
        [6 / 31],
    ])
    print(y)


if __name__ == '__main__':
    main()
    # test()
    # print(sum([0.38709677 ,0.19354839 ,0.12903226 ,0.09677419 ,0.19354839]))
