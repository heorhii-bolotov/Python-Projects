from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize, LabelEncoder
import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt
from torch.nn.functional import cross_entropy, softmax

np.set_printoptions(suppress=True)


DATA = '_02195759eb952fcd23b60d5b07594b7b_winequality-red.csv'


with open(DATA) as file:
    file.readline() # miss header line
    data = np.loadtxt(file, delimiter=';')


TRAIN_SIZE = 0.7
MAX_EPOCHS = 200

y = data[:, -1]
np.place(y, y < 5, 5)
np.place(y, y > 7, 7)
y -= y.min()
X = data[:, :-1]
X = normalize(X)

# y_encoded = LabelEncoder().fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=TRAIN_SIZE, random_state=0)


in_features, out_features = X.shape[1], len(np.unique(y))
HIDDEN_NEURONS_NUM = 100
lr = 0.05

# По наблюдением без софт софтмакса работает на ~ 87 %
# без софт софтмакса, Dropout and BatchNorm работает на ~ 77 %
model = torch.nn.Sequential(
    nn.Linear(in_features=in_features, out_features=HIDDEN_NEURONS_NUM),
    nn.ReLU(),
    nn.Dropout(),
    nn.BatchNorm1d(HIDDEN_NEURONS_NUM),
    nn.Linear(in_features=HIDDEN_NEURONS_NUM, out_features=out_features),
    nn.Softmax(dim=1)
)
loss_fn = nn.CrossEntropyLoss()
optim = torch.optim.Adam(model.parameters(), lr=lr)


X_train, y_train = torch.tensor(X_train, dtype=torch.float), torch.tensor(y_train, dtype=torch.long)
X_test, y_test = torch.tensor(X_test, dtype=torch.float), torch.tensor(y_test, dtype=torch.long)


def train(num_epochs):
    losses, test_losses = [], []
    for _ in range(num_epochs):
        model.train(True)
        preds = model(X_train)
        loss = loss_fn(preds, y_train)

        optim.zero_grad()
        loss.backward()
        optim.step()

        losses.append(loss.item())

        model.train(False)
        test_losses.append(loss_fn(model(X_test), y_test).item())

    return losses, test_losses


def plot(losses, test_losses):
    fig = plt.figure(figsize=(10, 8))
    # plt.scatter(range(len(losses)), losses, linewidths=3)
    # plt.scatter(range(len(test_losses)), test_losses, linewidths=3)
    plt.plot(range(len(losses)), losses, linewidth=3, label='train loss')
    plt.plot(range(len(test_losses)), test_losses, linewidth=3, label='test loss')
    plt.grid()
    plt.xlabel('num_epochs')
    plt.ylabel('CrossEntropyLoss')
    plt.legend()
    plt.show()


# def plot_boundary():
#     np.random.shuffle(data)
#     test_size = int(data.shape[0] * 0.3)
#     x, y = data[:test_size, :-1], data[:test_size, -1]
#     x = normalize(x)
#     model.train(False)
#     preds = model(torch.tensor(x, dtype=torch.float))
#     x = np.mean(x, axis=1)
#     preds = preds.data.numpy()
#     preds = np.argmax(preds, axis=1)
#     plt.scatter(x, y, preds, cmap=plt.cm.rainbow, alpha=0.3)
#
#     # x_min, x_max = x.min() - 1, x.max() + 1
#     # y_min, y_max = y.min() - 1, y.max() + 1
#     # plt.xlim()
#     # plt.ylim()
#     plt.show()


losses, test_losses = train(MAX_EPOCHS)
plot(losses, test_losses)

model.train(False)
preds = model(X_test)
loss = cross_entropy(preds, y_test)
print(loss.item())

preds = preds.data.numpy()
preds = np.argmax(preds, axis=1)
y_test = y_test.data.numpy()
print(np.mean(preds == y_test))




