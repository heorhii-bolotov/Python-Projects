import matplotlib
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from cmath import *
import matplotlib.patches as mpatches

matplotlib.style.use('ggplot')


def main():
    fig, ax = plt.subplots(figsize=(10, 8))

    cmap = ['black', 'pink', 'purple', 'yellow', 'gray', 'orange']
    labels = ['Uc', 'Ul', 'Ur', 'U', 'I']
    # labels = ['Uc', 'Ul', 'U', 'I']
    handles = [mpatches.Patch(color=c, label=f'{l}') for c, l in zip(cmap, labels)]

    # C < Co
    # ax.quiver(0, 0, 0, -2.5, color=cmap[0], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0.2, -2.5, 0, 5.5, color=cmap[1], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0.2, 3, 2, 0, color=cmap[2], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0, 0, 2, 3, color=cmap[3], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0, 0, 3.5, 0, color=cmap[4], angles='xy', scale_units='xy', scale=1)

    # C > Co
    ax.quiver(0, 0, 0, -2.5, color=cmap[0], angles='xy', scale_units='xy', scale=1)
    ax.quiver(0.2, -2.5, 0, 1, color=cmap[1], angles='xy', scale_units='xy', scale=1)
    ax.quiver(0.2, -1.5, 1.5, 0, color=cmap[2], angles='xy', scale_units='xy', scale=1)
    ax.quiver(0, 0, 1.7, -1.4, color=cmap[3], angles='xy', scale_units='xy', scale=1)
    ax.quiver(0, 0, 2.5, 0, color=cmap[4], angles='xy', scale_units='xy', scale=1)

    # C = Co
    # ax.quiver(0, 0, 0, -2.5, color=cmap[0], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0.2, -2.5, 0, 2.5, color=cmap[1], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0, 0, 3.5, 0, color=cmap[3], angles='xy', scale_units='xy', scale=1)
    # ax.quiver(0, 0, 2.5, 0, color=cmap[2], angles='xy', scale_units='xy', scale=1)


    ax.set_xlim(-1, 5)
    ax.set_ylim(-5, 5)
    ax.set_title('Векторна диаграмма кола')
    legend = plt.legend(handles=[mpatches.Patch(edgecolor='y', facecolor='y', label='C > Co')], loc=4)
    # ax.axis('equal')
    ax.legend(handles=handles)
    plt.gca().add_artist(legend)
    ax.tick_params(axis='both', labelsize=0, length=0)
    ax.grid()
    plt.show()


main()


def plot_digram(x, y, u, v, text, labels=None):
    fig, ax = plt.subplots(figsize=(10, 8))
    cmap = ['black', 'pink', 'purple', 'yellow', 'orange', 'gray']
    # cmap = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    handles = []
    for xi, yi, ui, vi, c, l in zip(x, y, u, v, cmap, labels):
        ax.quiver(xi, yi, ui, vi, color=c, angles='xy', scale_units='xy', scale=1)
        handles.append(mpatches.Patch(color=c, label=f'{l}'))
    # if labels is not None:
    #     for xi, yi, text in labels:
    #         ax.annotate(text, (xi, yi))
    ax.set_title('Суміщена діграмма напруг/струмів')
    ax.set_xlabel('+1')
    ax.set_ylabel('i')
    x, y = np.array(x), np.array(y)
    # ax.axis('equal')
    ax.set_xlim(x.min() - 5, x.max() + 8)
    ax.set_ylim(y.min() - 13, y.max() + 5)
    legend = plt.legend(handles=[mpatches.Patch(edgecolor='y', facecolor='y', label=text), ], loc=4)
    ax.legend(handles=handles)
    plt.gca().add_artist(legend)
    ax.grid()
    plt.show()


def init_params(args, zeros=1):
    cumsum = np.cumsum(args[zeros - 1: -1])
    x = np.zeros(zeros).tolist() + np.real(cumsum).tolist()
    y = np.zeros(zeros).tolist() + np.imag(cumsum).tolist()
    u, v = np.real(args), np.imag(args)
    # labels = list(zip((np.array(u) + np.array(x)) * 0.5, (np.array(v) + np.array(y)) * 0.5, text))
    return x, y, u, v


# def main():
#     # 21.1
#     I = rect(*(3.9 * 2, np.radians(0)))
#     U = rect(*(10.4, np.radians(-49)))
#     UR = rect(*(3.1, np.radians(0)))
#     UL = rect(*(5.9, np.radians(54)))
#     UC = rect(*(12.6, np.radians(-89)))
#
#     args = [I, U, UR, UC, UL]
#     text = ["I", "U", "UR", "UC", "UL"]
#     x, y, u, v = init_params(args, 3)
#     # plot_digram(x, y, u, v, '5мА 1В', text)
#
#
#     # 21.2
#     I = rect(*(13.6, np.radians(-10 + 2)))
#     U = rect(*(9.8, np.radians(0)))
#     IR = rect(*(10.4, np.radians(-0)))
#     IL = rect(*(5.4, np.radians(-54)))
#     IC = rect(*(2.6, np.radians(-(-89))))
#
#     args = [U, I, IR, IC, IL]
#     text = ["U", "I", "IR", "IC", "IL"]
#     x, y, u, v = init_params(args, 3)
#     # plot_digram(x, y, u, v, '10мА 1В', text)
#
#     # 21.3
#     I = rect(*(5.0 * 2, np.radians(11)))
#     # IL = rect(*(5.0 * 2, np.radians(54)))
#     IR = rect(*(4.9 * 2, np.radians(0)))
#     IC = rect(*(1.2 * 2, np.radians(-(-89))))
#
#     U = rect(*(10.4 - 0.4, np.radians(54)))
#     UR = rect(*(4, np.radians(0)))
#     UC = rect(*(4.1, np.radians(0)))
#     UL = rect(*(7.9, np.radians(90 - 11)))
#
#     args = [I, U, IR, IC, UC, UR, UL]
#     text = ["I = IL", "U", "IR", "IC", "UC", "UR", 'UL']
#     x, y, u, v = init_params(args, 6)
#     # plot_digram(x, y, u, v, '5мА 1В', text)
#
#     # 21.4
#     I = rect(*(5.0 * 2, np.radians(11)))
#     IL = rect(*(1.2 * 2 + 0.15, np.radians(-54-7)))
#     IR = rect(*(2.4 * 2, np.radians(0)))
#     IC = rect(*(3.4 * 2, np.radians(-18)))
#
#     U = rect(*(10.6, np.radians(-97)))
#     UR = rect(*(2, np.radians(0)))
#     UC = rect(*(10.9, np.radians(-18-89)))
#     UL = rect(*(7.9, np.radians(90 - 11)))
#
#     args = [IR, IL, IC, UC, UR, U]
#     text = ['IR', 'IL', 'IC = I', 'UC', 'UR', 'U']
#     # text = ["I = IL", "U", "IR", "IC", "UC", "UR", 'UL']
#     x, y, u, v = init_params(args, 6)
#     plot_digram(x, y, u, v, '5мА 1В', text)
'''
'''

# main()
# print((79.48 + 1 / 0.0106 + 81.63 + 83.33) / 4)
# R = (88.92 + 1 / 0.00323 + 92.87 + 97.36) / 4
# X = (122.389 + 1 / 0.0044 + 127.8246 + 134.83) / 4
# Z = rect(R, X)
# print(polar(Z))
# print(np.degrees(2.2826344458717585))
# print((5.638 + 1 / 0.463 + 5.96 + 5.59) / 4)
# print(-1 / 0.002652)
# print((-323.026 + -1 / 0.002652 + -341.607 + -320.5311) / 4)

# Z = complex(84.69 + 147.18 + 4.89, 153.079 - 340.559)
# Z = complex(4.83, -340.559) + (complex(84.69, 0) * complex(147.18, 153.079)) / (complex(84.69, 0) + complex(147.18, 153.079))
# U = rect(10.6, 54 - 79)
# I = U / Z
# print(Z)
# print(abs(Z), np.degrees(phase(Z)))
# print(abs(I), np.degrees(phase(I)))
# I = rect(0.03954079832960554, np.radians(180 - 176.49935023507248))
# print(abs(I), np.degrees(phase(I)))

# Ir = I * complex(147.18, 153.079) / ((complex(147.18, 153.079) + complex(84.69, 0)))
# Ic = I
# Il = I - Ir
# print()
# Ur = Ir * complex(84.69, 0)
# Uc = Ic * complex(4.83, -340.559)
# Ul = Il * complex(147.18, 153.079)
# print()
# print(abs(Ir), np.degrees(phase(Ir)))
# print(abs(Il), np.degrees(phase(Il)))
# print(abs(Ic), np.degrees(phase(Ic)))
# print()
# print(abs(Ur), np.degrees(phase(Ur)))
# print(abs(Ul), np.degrees(phase(Ul)))
# print(abs(Uc), np.degrees(phase(Uc)))
# print()
# P = abs(U) * abs(I) * np.cos(U.imag - I.imag)
# Pr = abs(Ur) * abs(Ir) * np.cos(Ur.imag - Ir.imag)
# Pl = abs(Uc) * abs(Il) * np.cos(Uc.imag - Il.imag)
# Pc = abs(Ul) * abs(Ic) * np.cos(Ul.imag - Ic.imag)
# for p in [P, Pr, Pl, Pc]:
#     print(p)
# print(abs(Z), np.degrees(1 / np.tan(Z.imag / Z.real)))
# R = 0.0269
# X = 0.0213
# I = complex(R, X)
# U = I * complex(4.89, - 340.559)
# print(U)
# print(abs(U), np.degrees(1 / np.tan(U.imag / U.real)))
# P = 10.4 * abs(rect(0.034, 56)) * np.cos(49 - 56)
# print(P)
# Pr = abs(rect(3.1, 0)) * abs(rect(0.034, 56)) * np.cos(- 56)
# print(Pr)
# Pl = abs(rect(5.9, 54)) * abs(rect(0.034, 56)) * np.cos(54 - 56)
# print(Pl)
# Pc = abs(rect(12.6, -89)) * abs(rect(0.034, 56)) * np.cos(89 - 56)
# print(Pc)
# print(0.1295 + 0.1188 + 0.018)
# print(abs(I), np.degrees(1 / np.tan(I.imag / I.real)))
# print(np.degrees(-10.232342193352626))
'''
'''

# import pandas as pd
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# from cmath import *


# PATH = '/Users/macair/Desktop/temk24.csv'


# data = pd.read_csv(PATH, delimiter=';', decimal=',', skipinitialspace=True)

# plot
# matplotlib.style.use('ggplot')
#
# def make_patch_spines_invisible(ax):
#     ax.set_frame_on(True)
#     ax.patch.set_visible(False)
#     for sp in ax.spines.values():
#         sp.set_visible(False)
#
# fig, ax = plt.subplots(figsize=(10, 8))
# fig.subplots_adjust(right=0.75)
# par1, par2 = ax.twinx(), ax.twinx()
# par2.spines['right'].set_position(('axes', 1.06))
# make_patch_spines_invisible(par2)
# # par2.spines['right'].set_visible(True)
#
# cmap = ['black', 'pink', 'purple', 'yellow', 'm', 'y', 'k', 'w']
#
# ax.plot(data['f'][10:15], data['UL'][10:15], '-bo', color=cmap[0])
# ax.plot(data['f'][10:15], data['UC'][10:15], '-bo', color=cmap[1])
# ax.plot([402, 402], [2, 14.2], '--', color='grey')
# par1.plot(data['f'][10:15], data['I'][10:15], '-bo', color=cmap[2])
# par2.plot(data['f'][10:15], data['a'][10:15], '-bo', color=cmap[3])
#
# ax.set_xlim(data['f'].min() - data['f'].std(), data['f'].max() + data['f'].std())
# ax.set_ylim(data[10:15][['UC', 'UL']].values.min() - data[10:15][['UC', 'UL']].values.std(),
#             data[10:15][['UC', 'UL']].values.max() + data[10:15][['UC', 'UL']].values.std())
# par1.set_ylim(data[10:15]['I'].min() - data[10:15]['I'].std(), data[10:15]['I'].max() + data[10:15]['I'].std())
# par2.set_ylim(data[10:15]['a'].min() - data[10:15]['a'].std(), data[10:15]['a'].max() + data[10:15]['a'].std())
#
# ax.set_xlabel('f')
# ax.set_ylabel('U')
# par1.set_ylabel('I')
# par2.set_ylabel('ƒ')
#
# tkw = dict(size=4, width=1.5)
# ax.tick_params(axis='x', **tkw), ax.tick_params(axis='y', **tkw)
# par1.tick_params(axis='x', **tkw)
# par2.tick_params(axis='x', **tkw)
#
# handles = [mpatches.Patch(color=c, label=f'{l}') for c, l in zip(cmap, ['Ul', 'Uc', 'I', 'φ'])]
# ax.legend(handles=handles)
# ax.set_title('Резонансні криві')
# plt.show()
