# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from numpy.linalg import LinAlgError
#
# np.set_printoptions(suppress=True, precision=3)
# matplotlib.style.use('ggplot')
#
#
# class LinearRegression:
#     """
#         Linear Regression with n-3 weights
#     """
#
#     def __init__(self):
#         pass
#
#     def init_params(self, X, y):
#         self.X, self.y = X, y
#         self.Mx, self.My = self._M(X), self._M(y)
#         self.stdX, self.stdY = self._std(X, self.Mx), self._std(y, self.My)
#
#     def __str__(self):
#         return f'Mx: {self.Mx} & My: {self.My.item()}\n' \
#                f'stdX: {self.stdX} & stdY: {self.stdY.item()}\n' \
#                f'weights: {self.weights}\n'
#
#     @staticmethod
#     def _M(C):
#         return C.mean() if len(C.shape) == 1 else C.mean(axis=0)
#
#     @staticmethod
#     def _std(C, mean):
#         return np.sqrt(((C - mean) ** 2).mean(axis=0))
#
#     @staticmethod
#     def covariance(C1, mean1, C2, mean2):
#         return ((C1 - mean1) * (C2 - mean2)).mean()
#
#     def fit(self, X, y):
#         self.init_params(X, y)
#         n, k = X.shape
#
#         L = np.array([[self.covariance(X[:, i], self.Mx[i], X[:, j], self.Mx[j]).item() for j in range(k)] for i in range(k)])
#         Ly = np.array([self.covariance(X[:, i], self.Mx[i], y.ravel(), self.My) for i in range(k)])
#         Ln = []
#         for i in range(k):
#             Li = np.copy(L)
#             Li[:, i] = Ly
#             Ln.append(Li)
#
#         weights = np.array([np.linalg.det(l) for l in Ln]) / np.linalg.det(L)
#         init_weight = (y - (X @ weights).reshape((-1, 1))).mean()
#         self.weights = np.concatenate(([init_weight, ], weights))
#
#         print(self)
#
#     def optimized_fit(self, X, y):
#         self.init_params(X, y)
#         n, k = X.shape
#         L = np.array([[self.covariance(X[:, i], self.Mx[i], X[:, j], self.Mx[j]).item() for j in range(k)] for i in range(k)])
#         Ly = np.array([self.covariance(X[:, i], self.Mx[i], y.ravel(), self.My) for i in range(k)])
#
#         if np.isclose(np.linalg.det(L), 0):
#             x = self.X
#             x[::5, 1] += np.random.random(x[::5].shape[0])
#             self.init_params(x, y)
#             L = np.array([[self.covariance(X[:, i], self.Mx[i], X[:, j], self.Mx[j]).item() for j in range(k)] for i in range(k)])
#             Ly = np.array([self.covariance(X[:, i], self.Mx[i], y.ravel(), self.My) for i in range(k)])
#
#         weights = np.linalg.solve(L, Ly)
#
#         init_weight = (y - (X @ weights).reshape((-1, 1))).mean()
#         self.weights = np.concatenate(([init_weight, ], weights))
#
#         print(self)
#
#     def predict(self, X):
#         k = self.weights.shape[0]
#         if X.shape[1] != k:
#             X = np.column_stack((np.ones((X.shape[0], 1)), X))
#
#         return X @ self.weights
#
#
# def plot(X, y, model):
#     fig = plt.figure(figsize=(10, 8))
#     ax = fig.add_subplot(111, projection='3d')
#     ax.scatter(X[:, 0], X[:, 1], y, color='r', label='Original Y')
#     ax.scatter(X[:, 0], X[:, 1], model.predict(X), color='g', label='Predicted Y')
#     xx, yy, zz = np.meshgrid(np.ones(X.shape[0]), X[:, 0], X[:, 1])
#     combinedArr = np.vstack((xx.flatten(), yy.flatten(), zz.flatten())).T
#     ax.plot_trisurf(combinedArr[:, 1], combinedArr[:, 2], model.predict(combinedArr), alpha=0.4, color='pink')
#     ax.set_xlabel('x1')
#     ax.set_ylabel('x2')
#     ax.set_zlabel('y')
#     ax.legend()
#     plt.show()
#
#
# def test():
#     w = np.array([-5, 1, -2.2]).reshape((-1, 1))
#     n = 10
#     X = np.column_stack((np.ones((n, 1)), np.random.random((n, 2))))
#     print(X)
#     y = X @ w
#     print(y.flatten())
#
#     regressor = LinearRegression()
#     regressor.optimized_fit(X[:, 1:], y)
#     # plot(X, y, regressor)
#     print(regressor.weights)
#
#
# def test1():
#     x1 = [7, 6, 7, 8, 7, 6, 5, 4, 0]
#     x2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     y = [9, 8, 7, 6, 5, 6, 7, 8, 7]
#     X, y = np.column_stack((x1, x2)), np.array(y).reshape((-1, 1))
#     regressor = LinearRegression()
#     regressor.optimized_fit(X, y)
#
#     print(y.flatten())
#     print(regressor.weights)
#     print(np.column_stack((np.ones((X.shape[0])), X)) @ regressor.weights)
#
#
# def main():
#     np.random.seed(42)
#     size = 10
#     # x1, x2, y = np.random.randint(0, 101, size), np.random.randint(0, 10, size), np.random.randint(0, 101, size)
#     x1, x2, y = np.arange(1, 11, 1), np.array([12, 14, 15, 11, 16, 18, 17, 28, 11, 21]), np.array([17, 22, 27, 31, 44, 49, 50, 59, 61, 73])
#     X, y = np.column_stack((x1, x2)), y.reshape((size, -1))
#     regressor = LinearRegression()
#     regressor.optimized_fit(X, y)
#     print(y.flatten())
#     print(np.column_stack((np.ones((X.shape[0])), X)) @ regressor.weights)
#     # plot(X, y, regressor)
#
# def marik():
#     weights = np.array([-5, 2, 3])
#     x1 = np.arange(-5, 6, 1)
#     x2 = np.arange(-10, 11, 2)
#
#     X = np.column_stack((np.ones(x1.size), x1, x2))
#     y = X @ weights
#     print(X)
#     print(weights)
#     print(y)
#
#     regressor = LinearRegression()
#     regressor.optimized_fit(X[:, 1:], y.reshape((-1, 1)))
#     print(regressor.weights)
#     # print(X.shape)
#     # print(y.shape)
#     # w = np.linalg.solve(X, y.reshape((-1, 1)))
#
# if __name__ == '__main__':
#     marik()
#     # main()
#     # test()
#     # test1()
#
import numpy as np


def dispersion(X):
    if 4 <= len(X) <= 10:
        an = [2.059, 2.32, 2.55, 2.7, 2.8, 2.95, 3.1]
        return ((max(X)-min(X))/an[len(X)-4])**2
    elif len(X) > 10:
        average_x = sum(X)/len(X)
        return sum(map(lambda x: (x-average_x)**2, X))/(len(X)-1)


def covariance(X: list, Y: list):
    average_x = sum(X)/len(X)
    average_y = sum(Y)/len(Y)
    return sum(map(lambda x, y: (x - average_x)*(y - average_y), X, Y))/len(X)


def create_L(a: list, b: list, y: list):
    L = [[covariance(a, a), covariance(a, b)],
         [covariance(b, a), covariance(b, b)]]

    L1 = [[covariance(a, y), covariance(a, b)],
          [covariance(b, y), covariance(b, b)]]

    L2 = [[covariance(a, a), covariance(a, y)],
          [covariance(b, a), covariance(b, y)]]
    return L, L1, L2


def det_matrix_2x2(m: list):
    return m[0][0]*m[1][1] - m[0][1]*m[1][0]


def count_coefs(L: list, L1: list, L2: list, X1:list, X2:list, Y:list):
    b1 = det_matrix_2x2(L1) / det_matrix_2x2(L)
    b2 = det_matrix_2x2(L2) / det_matrix_2x2(L)
    a = sum(Y)/len(Y) - b1*sum(X1)/len(X1) - b2*sum(X2)/len(X2)
    return a, b1, b2


def main():
    x1 = [-7, -5, -3, -2, -1, 0, 1, 3, 4, 6]
    x2 = [-6, -4, -2, -1, 0, 1, 2, 5, 6, 6]
    y = [-3, -9, -15, -18, -21, -24, -27, -37, -40, -38]
    L, L1, L2 = create_L(x1, x2, y)
    a, b1, b2 = count_coefs(L, L1, L2, x1, x2, y)
    print(L[0], L[1], sep='\n')
    print()
    print(f'Y ={a:.3f} + {b1:.3f}*X1 + {b2:.3f}*X2')

main()

