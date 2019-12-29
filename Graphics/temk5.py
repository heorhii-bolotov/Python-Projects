# import numpy as np
#
# E = 20.5
# R1, R2, R3, R4 = 50, 75, 100, 150
#
# A = np.array([
#     [R1 + R2, -R2],
#     [-R2, R3 + R2 + R4]
# ])
# y = np.array([
#     [E],
#     [0]
# ])
#
# Ik1, Ik2 = np.linalg.solve(A, y).ravel().tolist()
# I1 = Ik1
# I4, I3 = [Ik2] * 2
# I2 = Ik1 - Ik2
# Unx = I1 * R1 + I3 * R3
#
# R24 = R2 * R4 / (R2 + R4 + R3)
# R34 = R3 * R4 / (R2 + R4 + R3)
# R32 = R3 * R2 / (R2 + R4 + R3)
# R123 = R32 + R1
# Req = R123 * R24 / (R123 + R24) + R34
# Ikz = Unx / Req
# print(Ikz * 1000)

Unx = 14
Req = 78.65

# for Rn in [0, 20, 30, 40, 60, 80, 100, 130, 160, 180, 200]:
#     print(pow(Unx / (Rn + Req), 2) * Rn)
#
# In = [0, 50, 54, 58, 68, 78, 88, 102, 118, 128, 142][::-1]
# Un = [3.2, 4.4, 5, 6.3, 7.3, 8.1, 9, 9.6, 9.9, 10.3]


import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

# fig = plt.figure(figsize=(20, 15))
# d = {'Un': pd.Series(Un), 'In': pd.Series(In)}
# d = pd.DataFrame(d)
# d.plot('In', 'Un', label='Навантажувальна характеристика')
# d.plot('In', 'Un', marker='o')
# plt.grid()
# plt.legend()
# plt.show()

fig = plt.figure(figsize=(15, 12))
Pn = [0.45, 0.538, 0.59, 0.6426, 0.6324, 0.618, 0.612, 0.5568, 0.5346, 0.515]
Rn = [0, 20, 30, 40, 60, 80, 100, 130, 160, 180, 200]

data = pd.DataFrame({'Pn': pd.Series(Pn), 'Rn': pd.Series(Rn)})
data.plot('Rn', 'Pn', label='Навантажувальна характеристика')
data.plot('Rn', 'Pn', marker='o')
plt.grid()
plt.legend()
plt.show()