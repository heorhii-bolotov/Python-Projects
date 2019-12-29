import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True, precision=12)

I = 39
U, Ur, Ul, Uc, = 10.4, 3.1, 5.9, 12.6
f, fr, fl, fc = -49, 0, 54, -89

# Баланс потужностей для посл кола
# for u, fi in zip([U, Ur, Ul, Uc], [f, fr, fl, fc]):
#     print('I * U * cos(ƒ) = ', (I / 1000) * u * np.cos(np.radians(fi)))

# P, Pr, Pl, Pc = 0.2660975421585498, 0.12090000000000001, 0.1352493865524981, 0.00857611252328116
# print(P, '~', Pr + Pl + Pc)

U = 9.8
I, Ir, Il, Ic, = 136, 104, 54, 26
f, fr, fl, fc = 10, 0, 54, -89
# Баланс потужностей для паралел кола

# for i, fi in zip([I, Ir, Il, Ic], [f, fr, fl, fc]):
#     print('I * U * cos(ƒ) = ', (i / 1000) * U * np.cos(np.radians(fi)))
#
# P, Pr, Pl, Pc = 1.312551773214671, 1.0192, 0.31105595551317683, 0.004446873160219861
# print(P, '~', Pr + Pl + Pc)

# Баланс потужностей для різних кіл
# U, Ur, Ul, Uc = 10.4, 4, 7.9, 4.1
# I, Ir, Il, Ic = 50, 49, 50, 12
# f, fr, fl, fc = 32, 0, 54, -89

# for u, i, fi in zip([U, Ur, Ul, Uc], [I, Ir, Il, Ic], [f, fr, fl, fc]):
#     print(u * (i / 1000) * np.cos(np.radians(fi)))
# P, Pr, Pl, Pc = 0.4409850100013415, 0.196, 0.23217517465552695, 0.000858658396714353
# print(P, '~', Pr + Pl + Pc)

# U, Ur, Ul, Uc = 10.6, 2, 2, 10.9
# I, Ir, Il, Ic = 34, 24, 12, 34
# f, fr, fl, fc = -79, 0, 54, -89

# for u, i, fi in zip([U, Ur, Ul, Uc], [I, Ir, Il, Ic], [f, fr, fl, fc]):
#     print(u * (i / 1000) * np.cos(np.radians(fi)))
# P, Pr, Pl, Pc = 0.06876756193370678, 0.048, 0.014106846055019358, 0.006467861825657302
# print(P, '~', Pr + Pl + Pc)

I = (0.039, 0)
U, Ur, Ul, Uc = (3.126, 9.91), (3.1, 0), (-4.89, -3.29), (6.428, -10.836)
fig, ax = plt.subplots(figsize=(10, 8))
x, y = list(zip(Ul, Uc, Ur, U, I))
plt.plot(x, y, '--bo', linewidth=3, markersize=12)
plt.title('рис. 21.1 суміщена діаграмма струму/напруг')
for x_, y_, t in zip(x, y, ['Ul', 'Uc', 'Ur', 'U', 'I']):
    # f'{t} ~ {x_} + i * ({y_})'
    ax.annotate(t, (x_ + 0.3, y_ + 0.3))
plt.grid()
plt.show()