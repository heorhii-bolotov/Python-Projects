# from random import randint
#
# l = [3] + [4] * 2 + [5, 6, 7] + [8] * 3
# print(l)
# # a = list(str(randint(10000, 99999)))
# a = [4, 3, 8, 8, 8]
# print([3, 4] in l)

from itertools import permutations
_set = [3, 4, 4, 5, 6, 7, 8, 8, 8]
res = permutations(_set, r=5)
print(len(list(res)) / (9 * (10 ** 4)))
