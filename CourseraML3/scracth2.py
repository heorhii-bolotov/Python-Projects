import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score as cv_score
import matplotlib.pyplot as plt


def plot_scores(d_scores):
    n_components = np.arange(1, d_scores.size + 1)
    plt.plot(n_components, d_scores, 'b', label='PCA scores')
    plt.xlim(n_components[0], n_components[-1])
    plt.xlabel('n components')
    plt.ylabel('cv scores')
    plt.legend(loc='lower right')
    plt.show()


def write_answer_1(optimal_d):
    with open("pca_answer1.txt", "w") as fout:
        fout.write(str(optimal_d))


data = pd.read_csv('data_task1.csv')

# place your code here
scores = np.array([cv_score(PCA(n_components=n + 1), data, cv=3).mean() for n in range(min(data.shape))])
plot_scores(scores)
# write_answer_1(scores.argmax() + 1)

data = pd.read_csv('data_task2.csv')

model = PCA(n_components=data.shape[0])
model.fit(data)
W_pca = model.components_


plt.plot()