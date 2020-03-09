import torch
import numpy as np

import matplotlib.pyplot as plt
from math import ceil


# ------------       Plot Images from batch       ------------

def plot_img(img, title='', ax=plt):
    if isinstance(img, torch.Tensor):
        img = img.detach().cpu().numpy().transpose((1, 2, 0))

    img = (img - img.min()) / (img.max() - img.min())
    img = np.clip(img, 0, 1)

    ax.imshow(img, cmap=plt.cm.gray, vmin=-1, vmax=1, interpolation='nearest')
    ax.set_title(title)
    ax.grid(False)


def plot_batch(x, y, nrow=3, ncol=3, title=''):
    plt.figure(figsize=(2.1 * ncol, 1.9 * nrow))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(nrow * ncol):
        if i == len(x): break
        ax = plt.subplot(nrow, ncol, i + 1)
        plot_img(x[i], y[i], ax)

    plt.suptitle(title)
    plt.show()


def plot_rnd(x, y, n=10):
    inds = np.arange(0, len(x)).astype(int)
    np.random.shuffle(inds)
    nrow, ncol = ceil(len(inds) / 5), 5
    plot_batch(x[inds[:n].tolist()], y[inds[:n].tolist()], nrow=nrow, ncol=ncol)
# ---------------------------------------------------------------