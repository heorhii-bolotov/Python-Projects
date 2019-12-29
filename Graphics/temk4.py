# R12, R23, R31 = 200, 800, 1000
#
# #   1.
# print()
# # Rc = R12 + R23 + R31
# # R1223 = (R12 * R23) / (R12 + R23)
# # Rp = R1223 * R31 / (R1223 + R31)
# # Rm = R23 * R31 / (R23 + R31) + R12
# print()
# # 2.
# import numpy as np
#
# E = 20.8
# R1, R2 = 50, 75
# #
# # A = np.array([
# #     [R1 + R12, -R1, -R12],
# #     [-R1, R1 + R2 + R23, -R23],
# #     [-R12, -R23, R31 + R12 + R23]
# # ])
# # y = np.array([
# #     [E],
# #     [0],
# #     [0],
# # ])
# # IK1, IK2, IK3 = np.linalg.solve(A, y).ravel().tolist()
# # I1 = IK1 - IK2
# # I2 = IK2
# # I3 = IK1
# # for i in [I1, I2, I3]:
# #     print(i * 1000)
#
# A = np.array([
#     [(1 / R12) + (1 / R23) + (1 / R1), -1 / R23],
#     [-1 / R23, (1 / R31) + (1 / R23) + (1 / R2)],
# ])
# y = np.array([
#     [E * (1 / R1)],
#     [E * (1 / R2)],
# ])
# f1 = 0
# f4 = E
# f2, f3 = np.linalg.solve(A, y).ravel().tolist()
# print(f1, f2, f3, f4)
# # I1, I2, I3 = f4 + f1 - E
# I1, I2, I3 = (f4 - f2) / R1, (f4 - f3) / R2, (f4 - f1 - f2) / ((R12 * R1) / (R12 + R1))
# print(1000 * (f2 - f1) / R12, 1000 * (f4 - f2) / R1)
# for i in [I1, I2, I3]:
#     print(i * 1000)
