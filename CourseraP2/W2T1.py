from abc import ABC, abstractmethod
import math


""" My realisation of class Base"""
# class Base(ABC):
#
#     def __init__(self, data, result):
#         self.data = data
#         self.result = result
#
#     def get_answer(self):
#         return [int(x >= 0.5) for x in self.data]
#
#     def get_score(self):
#         ans = self.get_answer()
#         return sum([int(x == y) for (x, y) in zip(ans, self.result)]) \
#                / len(ans)
#
#     def get_loss(self, func=None, sign=1):
#         return sign * sum([func(x, y) for (x, y) in zip(self.data, self.result)])
#
#
# class A(Base):
#
#     def __init__(self, data, result):
#         super().__init__(data, result)
#
#     def get_loss(self, func=None, sign=1):
#         func = func or (lambda x, y: (x - y) * (x - y))
#         super().get_loss(func, sign)
#
#
# class B(Base):
#
#     def __init__(self, data, result):
#         super().__init__(data, result)
#
#     def _get(self, denom=0):
#         ans = self.get_answer()
#         res = [int(x == 1 and y == 1) for (x, y) in zip(ans,
#                                                         self.result)]
#         return sum(res) / sum(self.result if not denom else ans)
#
#     def get_score(self):
#         pre, rec = self._get(1), self._get()
#         return 2 * pre * rec / (pre + rec)
#
#     def get_loss(self, func=None, sign=-1):
#         func = func or (lambda x, y: y * math.log(x) + (1 - y) * math.log(1 - x))
#         super().get_loss(func, sign)
#
#
# class C(Base):
#
#     def __init__(self, data, result):
#         super().__init__(data, result)
#
#     def get_loss(self, func=None, sign=1):
#         func = func or (lambda x, y: abs(x - y))
#         super().get_loss(func, sign)


class Base(ABC):
    def __init__(self, data, result):
        self.data = data
        self.result = result

    def get_answer(self):
        return [int(x >= 0.5) for x in self.data]

    def get_score(self):
        ans = self.get_answer()
        return sum([int(x == y) for x, y in zip(ans, self.result)]) / len(ans)

    @abstractmethod
    def get_loss(self):
        pass


class A(Base):
    def __init__(self, data, result):
        super().__init__(data, result)

    def get_loss(self):
        return sum([(x - y) * (x - y) for x, y in zip(self.data, self.result)])


class B(Base):
    def __init__(self, data, result):
        super().__init__(data, result)

    def get_loss(self):
        return -sum([y * math.log(x) + (1 - y) * math.log(1 - x)
                     for x, y in zip(self.data, self.result)])

    def get_pre(self):
        ans = self.get_answer()
        res = [int(x == 1 and y == 1) for x, y in zip(ans, self.result)]
        return sum(res) / sum(ans)

    def get_rec(self):
        ans = self.get_answer()
        res = [int(x == 1 and y == 1) for x, y in zip(ans, self.result)]
        return sum(res) / sum(self.result)

    def get_score(self):
        pre = self.get_pre()
        rec = self.get_rec()
        return 2 * pre * rec / (pre + rec)


class C(Base):
    def __init__(self, data, result):
        super().__init__(data, result)

    def get_loss(self):
        return sum([abs(x - y) for x, y in zip(self.data, self.result)])
