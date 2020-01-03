import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.cluster import MeanShift
from matplotlib.colors import ListedColormap

pd.options.display.float_format = '{:.5f}'.format
DATA_FILE = '/Users/macair/Python Projects/CourseraML3/umn_foursquare_datasets/checkins.dat'
data = pd.read_csv(DATA_FILE, skipinitialspace=True, sep='|')
data.dropna(axis=0, inplace=True)
data = data

bandwidth = 0.1
min_freq = 15
n = 100000


def main():
    meanshift = MeanShift(bandwidth=bandwidth, n_jobs=2)
    X = data.iloc[:n, 3:5]
    meanshift.fit(X)
    labels = meanshift.labels_
    centers = meanshift.cluster_centers_

    clusters, counts = np.unique(labels, return_counts=True)




classes, counts = np.unique(labels, return_counts=True)
inds = np.where(counts > min_freq)
fig = plt.figure(figsize=(10, 8))
pred_c = meanshift.predict(X)
cmap = cm.get_cmap('viridis', len(list(inds)[0]))
plt.plot(X[:, 3], X[:, 4], color=pred_c, )
plt.xlabel('latitude')
plt.ylabel('longitude')
plt.grid()
plt.legend()
plt.show()