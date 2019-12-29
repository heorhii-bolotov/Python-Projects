# # # # import numpy as np
# # # # from sklearn.datasets import load_digits
# # # # from sklearn.model_selection import cross_val_score, KFold, train_test_split, RandomizedSearchCV
# # # # from sklearn.tree import DecisionTreeClassifier
# # # # from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
# # # # import matplotlib.pyplot as plt
# # # #
# # # # cv = 10
# # # # n_jobs = 2
# # # #
# # # #
# # # # digits = load_digits()
# # # # X = digits.data
# # # # Y = digits.target
# # # #
# # # #
# # # # def write(n=0, *args):
# # # #     with open(f'file{n}.txt', 'w') as file:
# # # #         file.write(' '.join(list(map(str, args))))
# # # #
# # # #
# # # # def plot_curve(x1=None, y1=None, x2=None, y2=None):
# # # #     if x1 is None and x2 is None:
# # # #         x1, x2 = np.arange(0, y1.size, 1), np.arange(0, y1.size, 1)
# # # #     plt.grid(x1, y1, 'g-', marker='o', label='first')
# # # #     plt.grid(x2, y2, 'r-', marker='o', label='second')
# # # #     plt.ylim((0, 1.02))
# # # #     plt.legend()
# # # #     plt.show()
# # # #
# # # #
# # # # def plot_curves(labels, y, x=None):
# # # #     if x is None:
# # # #         x_ = np.arange(0, 1, y[0].size)
# # # #         for y_, label_ in zip(y, labels):
# # # #             plt.plot(x_, y_, marker='o', label=label_)
# # # #     else:
# # # #         for x_, y_, label_ in zip(x, y, labels):
# # # #             plt.plot(x_, y_, marker='o', label=label_)
# # # #     plt.grid()
# # # #     plt.legend()
# # # #     plt.show()
# # # #
# # # #
# # # # def first():
# # # #     estimator = DecisionTreeClassifier(random_state=0)
# # # #     answer1 = cross_val_score(estimator, X, Y, cv=cv, n_jobs=n_jobs).mean()
# # # #     write(1, answer1)
# # # #
# # # #
# # # # def second():
# # # #     estimator = DecisionTreeClassifier()
# # # #     classifier = BaggingClassifier(base_estimator=estimator, n_estimators=100, random_state=0)
# # # #     answer2 = cross_val_score(classifier, X, Y, cv=cv, n_jobs=n_jobs).mean()
# # # #     write(2, answer2)
# # # #
# # # #
# # # # def third():
# # # #     estimator = DecisionTreeClassifier()
# # # #     classifier = BaggingClassifier(base_estimator=estimator, max_features=int(np.sqrt(X.shape[1])), n_estimators=100, random_state=0)
# # # #     answer3 = cross_val_score(classifier, X, Y, cv=cv, n_jobs=n_jobs).mean()
# # # #     write(3, answer3)
# # # #
# # # #
# # # # def fourth():
# # # #     estimator = DecisionTreeClassifier(max_features='sqrt')
# # # #     classifier = BaggingClassifier(base_estimator=estimator, n_estimators=100, random_state=0)
# # # #     answer4 = cross_val_score(classifier, X, Y, cv=cv, n_jobs=n_jobs).mean()
# # # #     write(4, answer4)
# # # #
# # # #
# # # # def fifth():
# # # #     classifier = RandomForestClassifier(n_estimators=100, max_features='sqrt', random_state=0)
# # # #     answer5 = cross_val_score(classifier, X, Y, cv=cv, n_jobs=n_jobs).mean()
# # # #     print(answer5)
# # # #
# # # #
# # # # def SearchCV():
# # # #     X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=int(np.sqrt(Y.size)))
# # # #     classifier = RandomForestClassifier()
# # # #     param_grid = {
# # # #         'n_estimators': [1, 2, 3, 5, 10, 20, 40, 50, 70, 80, 100],
# # # #         'max_depth': [2, 3, 5, 7, 10, None],
# # # #         'max_features': ['sqrt', 'log2', None, 0.25, 0.5, 0.75]
# # # #     }
# # # #     grid_cv = RandomizedSearchCV(estimator=classifier, param_distributions=param_grid, n_iter=20, cv=3, random_state=0,
# # # #                                  n_jobs=n_jobs)
# # # #     grid_cv.fit(X_train, Y_train)
# # # #
# # # #
# # # # def main():
# # # #     fifth()
# # # #
# # # #
# # # # main()
# # # from functools import reduce
# # #
# # # from sklearn.datasets import load_boston
# # # from sklearn.metrics import mean_squared_error
# # # from sklearn.model_selection import train_test_split, GridSearchCV
# # # from sklearn.tree import DecisionTreeRegressor
# # # from sklearn.linear_model import LinearRegression
# # # import numpy as np
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # import xgboost as xgb
# # # import seaborn as sns
# # # # %matplotlib inline
# # #
# # #
# # # #  prepare dataset
# # # boston = load_boston()
# # # X = boston.data
# # # Y = boston.target
# # # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25)
# # #
# # #
# # # def plotData():
# # #     sns.set(style='ticks')
# # #     data = sns.load_dataset('boston')
# # #     sns.pairplot(data, hue='species')
# # #
# # # plotData()
# # #
# # #
# # # def getStats():
# # #     learning_rate = [0.01, 0.1, 0.2, 0.3, 0.5]
# # #     max_depth = range(2, 9, 2)
# # #     n_estimators = range(100)
# # #     random_state = 42
# # #     n_jobs = 2
# # #     objective = 'reg:squarederror'
# # #
# # #
# # #     def gradBoostReg(**kwargs):
# # #         regressor = xgb.XGBRegressor(**kwargs)
# # #         regressor.fit(X_train, Y_train)
# # #         return np.sqrt(mean_squared_error(Y_test, regressor.predict(X_test)))
# # #
# # #
# # #     for eta in learning_rate:
# # #         fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# # #         fig.suptitle(f'SMSE GBRM, eta: {eta}')
# # #         i, j = 0, 0
# # #         for depth in max_depth:
# # #             axes[i, j].plot(n_estimators, list(map(
# # #                 lambda n: gradBoostReg(learning_rate=eta, max_depth=depth, n_estimators=n, n_jobs=n_jobs,
# # #                                        objective=objective, random_state=random_state), n_estimators)), )
# # #             axes[i, j].set_title(f'max_depth: {depth}')
# # #             if j == 1:
# # #                 j = 0
# # #                 i += 1
# # #             else:
# # #                 j += 1
# # #
# # #         for ax in axes.flat:
# # #             ax.set(xlabel='smse', ylabel='n-tree')
# # #             ax.label_outer()
# # #             ax.grid()
# # #         plt.show()
# # #
# # # def compareLinearTree():
# # #     regressor = LinearRegression(n_jobs=2)
# # #     regressor.fit(X_train, Y_train)
# # #     smse = np.sqrt(mean_squared_error(Y_test, regressor.predict(X_test)))
# # #     return smse
# # import numpy as np
# # import pandas as pd
# # from sklearn.datasets import load_digits, load_breast_cancer
# # from sklearn.ensemble import RandomForestClassifier
# # from sklearn.model_selection import cross_val_score, train_test_split
# # from sklearn.naive_bayes import BernoulliNB, MultinomialNB, GaussianNB
# # from sklearn.neighbors import KNeighborsClassifier
# # from scipy.spatial.distance import euclidean
# # from collections import defaultdict
# #
# # np.set_printoptions(suppress=True)
# #
# #
# # def write(num, *args):
# #     with open(f'file{num}', 'w') as file:
# #         file.write(' '.join(map(str, args)))
# #
# #
# # data_digits = load_digits()
# # X, y = data_digits.data, data_digits.target
# # train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=0.25)
# #
# #
# # def classifyKNN(train_data, test_data):
# #     n = train_data.shape[0]
# #     points = defaultdict(tuple)
# #     for i in range(test_data.shape[0]):
# #         points[i] = (np.inf, -1.)
# #
# #     for i, row in enumerate(train_data):
# #         for j, row_ in enumerate(test_data):
# #             dist = euclidean(row, row_)
# #             points[j] = (dist, i) if points[j][0] > dist else points[j]
# #     return list(map(lambda x: x[1], points.values()))
# #
# #
# # inds = classifyKNN(train_X, test_X)
# # answer1 = (train_y[inds] == test_y).mean()
# # write(1, answer1)
# # print(answer1)
# #
# # classifier = RandomForestClassifier(n_estimators=1000, n_jobs=2)
# # classifier.fit(train_X, train_y)
# # cross_val_score(classifier, test_X, test_y)
#
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import normalize, LabelEncoder
# import numpy as np
# import pandas as pd
# import torch
# from torch import nn
# import matplotlib.pyplot as plt
# from torch.nn.functional import cross_entropy, softmax
#
# np.set_printoptions(suppress=True)
#
# DATA = '_02195759eb952fcd23b60d5b07594b7b_winequality-red.csv'
#
# with open(DATA) as file:
#     file.readline() # miss header line
#     data = np.loadtxt(file, delimiter=';')
#
#
# TRAIN_SIZE = 0.7
# HIDDEN_NEURONS_NUM = 100
#
# y = data[:, -1]
# np.place(y, y < 5, 5)
# np.place(y, y > 7, 7)
# y -= y.min()
# X = data[:, :-1]
# X = normalize(X)
#
#
# def train(num_epochs):
#     losses, test_losses = [], []
#     for _ in range(num_epochs):
#         model.train(True)
#         preds = model(X_train)
#         loss = loss_fn(preds, y_train)
#
#         optim.zero_grad()
#         loss.backward()
#         optim.step()
#
#         losses.append(loss.item())
#
#         model.train(False)
#         test_losses.append(loss_fn(model(X_test), y_test).item())
#
#     return losses, test_losses
#
#
# in_features, out_features = X.shape[1], len(np.unique(y))
# loss_fn = nn.CrossEntropyLoss()
#
# lr = [0.05, 0.03, 0.01, 0.007, 0.001]
# num_epochs = range(100, 1001 - 500, 100)
# k_fold = 3
# folds_loss, folds_acc = [], []
# for i in range(k_fold):
#     print(i)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=TRAIN_SIZE)
#     X_train, y_train = torch.tensor(X_train, dtype=torch.float), torch.tensor(y_train, dtype=torch.long)
#     X_test, y_test = torch.tensor(X_test, dtype=torch.float), torch.tensor(y_test, dtype=torch.long)
#     ep_loss, ep_acc = [], []
#     for n_epochs in num_epochs:
#         print('\t', n_epochs)
#         model = torch.nn.Sequential(
#             nn.Linear(in_features=in_features, out_features=HIDDEN_NEURONS_NUM),
#             nn.ReLU(),
#             nn.Dropout(),
#             nn.BatchNorm1d(HIDDEN_NEURONS_NUM),
#             nn.Linear(in_features=HIDDEN_NEURONS_NUM, out_features=out_features),
#             nn.Softmax(dim=1)
#         )
#         lr_loss, lr_acc = [], []
#         for lr_ in lr:
#             print('\t\t', lr_)
#             optim = torch.optim.Adam(model.parameters(), lr=lr_)
#             for _ in range(n_epochs):
#                 model.train(True)
#                 preds = model(X_train)
#                 loss = loss_fn(preds, y_train)
#                 optim.zero_grad()
#                 loss.backward()
#                 optim.step()
#
#             model.train(False)
#             preds = model(X_test)
#             loss = cross_entropy(preds, y_test).item()  #
#             preds = np.argmax(preds.data.numpy(), axis=1)
#             accuracy = np.mean(preds == y_test.data.numpy())  #
#
#             lr_loss.append(loss), lr_acc.append(accuracy)
#
#         ep_loss.append(lr_loss), ep_acc.append(lr_acc)
#
#     folds_loss.append(ep_loss), folds_acc.append(ep_acc)
#
# folds_loss, folds_acc = np.array(folds_loss), np.array(folds_acc)
# mean_folds_loss, mean_folds_acc = folds_loss.mean(axis=3), folds_acc.mean(axis=3)
# n, k = np.argmin(mean_folds_loss)
# m, l = np.argmax(mean_folds_loss)
# print('min loss', num_epochs[n], lr[k])
# print('max acc', num_epochs[m], lr[l])


from pybrain.datasets import ClassificationDataSet # Структура данных pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules.softmax import SoftmaxLayer
from pybrain.utilities import percentError
import numpy as np
import random
import matplotlib.pyplot as plt

# Определение основных констант
HIDDEN_NEURONS_NUM = 100 # Количество нейронов, содержащееся в скрытом слое сети
MAX_EPOCHS = 100 # Максимальное число итераций алгоритма оптимизации параметров сети


ds_train = ClassificationDataSet(X.shape[1], nb_classes=len(np.unique(y_train)))
ds_train.setField('input', X_train)
ds_train.setField('target', y_train[:, np.newaxis])
ds_train._convertToOneOfMany()
ds_test = ClassificationDataSet(X.shape[1], nb_classes=len(np.unique(y_train)))
ds_test.setField('input', X_test)
ds_test.setField('target', y_test[:, np.newaxis])
ds_train._convertToOneOfMany()


np.random.seed(0)
net = buildNetwork(ds_train.indim, HIDDEN_NEURONS_NUM, ds_train.outdim, outclass=SoftmaxLayer)
init_params = np.random.random(len(net.params))
net._setParameters(init_params)

trainer = BackpropTrainer(net, dataset=ds_train)
err_train, err_val = trainer.trainUntilConvergence(maxEpochs=MAX_EPOCHS)

'''
'''
random.seed(0)
np.random.seed(0)

def plot_classification_error(hidden_neurons_num, res_train_vec, res_test_vec):
    fig = plt.figure(figsize=(10, 8))
    plt.plot(hidden_neurons_num, res_train_vec)
    plt.plot(hidden_neurons_num, res_test_vec, '-r')

def write_answer_nn(optimal_neurons_num):
    with open("nnets_answer1.txt", "w") as fout:
        fout.write(str(optimal_neurons_num))

hidden_neurons_num = [50, 100, 200, 500, 700, 1000]
res_train_vec = []
res_test_vec = []

for nnum in hidden_neurons_num:
    net = buildNetwork(ds_train, nnum, ds_train.outdim, outclass=SoftmaxLayer)
    init_params = np.random.random(len(net.params))
    net._setParameters(init_params)

    trainer = BackpropTrainer(net, dataset=ds_train)
    trainer.trainUntilConvergence(maxEpochs=MAX_EPOCHS)
    res_train = net.activateOnDataset(ds_train).argmax(axis=1)
    res_test = net.activateOnDataset(ds_test).argmax(axis=1)
    res_train_vec.append(percentError(res_train, ds_train['target'].argmax(axis=1))), res_test_vec.append(percentError(res_test, ds_test['target'].argmax(axis=1)))


from torch import