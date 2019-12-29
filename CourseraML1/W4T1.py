import numpy as np
from scipy.stats import f, norm
from scipy.special import beta
import matplotlib.pyplot as plt


"""
         Fisher's distribution Wiki - https://en.wikipedia.org/wiki/F-distribution
           
"""


#   First p.


def pdf(x, d1, d2):
    return np.sqrt(np.float64((pow(d1 * x, d1) * pow(d2, d2)) / (pow(d1 * x + d2, d1 + d2)))) / (x * beta(d1 / 2, d2 / 2))


d1, d2 = 29., 18.


fig, ax = plt.subplots(figsize=(20, 10))

# generate random variates. F-distribution
rv = f(d1, d2)
sample = rv.rvs(size=1000)
x = np.linspace(0, sample.max(), 1000)

# plotting F-distribution's pdf
ax.plot(x, pdf(x, d1, d2), color="blue", linewidth=7.0, label="pdf")
ax.hist(sample, int(len(sample) / 10), density=True, alpha=0.5, label="rvs")

# styling
ax.set_xlabel("x", {'fontname': 'Arial', 'size': 24})
ax.set_ylabel("f(x)", {'fontname': 'Arial', 'size': 24})
ax.set_title("Fisher–Snedecor distribution (n=1000)", {'fontname': 'Arial', 'size': 24})
plt.legend(fontsize=20, frameon=True)
ax.grid()
plt.show()


#   Second p.


# degrees of freedom  d1, d2 > 0
d1, d2 = 29., 18.
# If dfd > 2
mean = d2 / (d2 - 2)
# If dfd > 4
variance = (2 * pow(d2, 2) * (d1 + d2 - 2)) / (d1 * pow((d2 - 2), 2) * (d2 - 4))
# len of each sample
n = [5, 10, 20, 40]


fig = plt.figure(figsize=(20, 10))


# print(np.average(np.array(samples[0]).reshape((10, 5)), axis=1, weights=[1, ] * 5))


def _plot(ax, sample, i):
    # average of each sample -> for hist
    average = np.average(np.array(sample).reshape((1000, i)), axis=1, weights=[1, ] * i)

    # normal probability density -> plot
    norm_rv = norm(loc=mean, scale=np.sqrt(variance / i))
    x = np.linspace(0, average.max(), 1000)

    # plot normal pdf
    ax.plot(x, norm_rv.pdf(x), color="blue", linewidth=7.0, label="norm pdf")
    ax.hist(average, int(len(sample) / 10), density=True, alpha=0.5, label="rvs")

    # styling
    ax.set_xlabel("x", {'fontname': 'Arial', 'size': 24})
    ax.set_ylabel("f(x)", {'fontname': 'Arial', 'size': 24})
    ax.set_title(f"F-distribution (n={i})", {'fontname': 'Arial', 'size': 24})
    plt.legend(fontsize=20, frameon=True)
    ax.grid()


# generate random variates. F-distribution
samples = ([f.rvs(d1, d2, size=i) for _ in range(1000)] for i in n)
samp = iter(samples)
for enum, i in enumerate(n):
    # new subplot (enum + 1 for title number)
    ax = fig.add_subplot(2, 2, enum + 1)
    # plot each sample
    _plot(ax, next(samp), i)

plt.show()









