"""
НОМЕР СПИСКА 5 ВАРИАНТ 11

В кармане есть 2 монеты по 50коп., 3 монеты по 25коп., 3 монеты по 5коп. .
Вероятность что все три монеты разные.
"""
from itertools import permutations
from math import factorial as fact, gcd
from random import choices, choice

# # КОМБИНАТОРИКА ФОРМУЛА РАЗМЕЩЕНИЯ - A(n, m)
n = 8
m = 3
a1, a2, a3 = 2, 3, 3

num = fact(a1) / fact(a1 - 1) * fact(1)\
    * fact(a2) / fact(a2 - 1) * fact(1)\
    * fact(a3) / fact(a3 - 1) * fact(1)

denom = fact(n) / (fact(n - m) * fact(m))
gcd_ = gcd(int(num), int(denom))
print('КОМБИНАТОРИКА ФОРМУЛА РАЗМЕЩЕНИЯ')
print(round(num / denom, 3))
print(f'{int(num / gcd_)}/{int(denom / gcd_)}\n')


# КЛАССИЧЕСКИЙ МЕТОД
p = fact(m)
denom = (n) * (n - 1) * (n - 2)
num = a1 * a2 * a3 * p
# three_cases = (a1 / n) \
#             * (a2 / (n - 1)) \
#             * (a3 / (n - 2))
# p = fact(m)
# num = (three_cases * p) * denom
#
gcd_ = gcd(int(num), int(denom))
print('КЛАССИЧЕСКИЙ МЕТОД')
print(round(num / denom, 3))
print(f'{int(num / gcd_)}/{int(denom / gcd_)}\n')


# ВЫБОРКА СТАТИСТИЧЕСКИЙ МЕТОД
# denom = 50000
sets = [1] * 2 + [2] * 3 + [3] * 3
# num = len([1 for _ in range(denom) if len({choice(sets), choice(sets), choice(sets)}) == 3])

sets = list(permutations(sets, 3))
denom = len(sets)
num = len(list(filter(lambda x: len(set(x)) == 3, sets)))

gcd_ = gcd(int(num), int(denom))
print('ВЫБОРКА СТАТИСТИЧЕСКИЙ МЕТОД')
print(round(num / denom, 3))
print(f'{int(num / gcd_)}/{int(denom / gcd_)}')

# def func():
#     pass
#
#
# a1, a2, a3 = 3, 3, 2
# c1, c2, c3 = [50], [25], [10]
# coins = c1 * a1 + c2 *  + c3
# coin1 = choice(coins)
# coins.remove(coin1)
#
# if coin1 in c1:
#     a1 -= 1
# elif coin1 in c2:
#     a2 -= 1
# else:
#     a3 -= 1
