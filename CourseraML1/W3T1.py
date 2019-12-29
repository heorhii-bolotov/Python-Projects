from scipy.optimize import minimize, differential_evolution
import numpy as np
import matplotlib.pyplot as plt
from W2T2FD import File


x = np.linspace(1., 30., 60)


# [1, 30]
def func(x):
    return np.sin(x / 5) * np.exp(x / 10) + 5 * np.exp(-x / 2)


def int_func(x):
    return np.array(list(map(int, func(x))))


# fig, ax = plt.subplots()
# ax.plot(x, func(x))
# ax.plot(x, int_func(x))
# ax.set(xlabel="x", ylabel="f(x)", title="f(x) = sin(x / 5) * exp(x / 10) + 5 * exp(-x / 2)")
# ax.grid()
# plt.show()



# 1.
# res = [minimize(func, step, method="BFGS") for step in [2., 30.]]
# print(*list(map(lambda x: x.nit, res)))

# 2.
# res = differential_evolution(func, [(1., 30.)])
# print(f"{res.x} {func(*res.x)} iter: {res.nit}")

# 3.
res = (minimize(int_func, 30., method="BFGS"), differential_evolution(int_func, [(1., 30.)]))
print(list(map(lambda x: x.nit, res)))

# file = File("/Users/macair/Desktop/data.txt")
# file.write(" ".join(map(lambda x: str(*int_func(x.x)), res)))


