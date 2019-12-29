from abc import ABC
import random


class AbstractLevel:

    @classmethod
    def get_map(cls):
        return cls.Map()

    @classmethod
    def get_objects(cls):
        return cls.Objects()

class MapLevel:

    def __init__(self, n, r):
        self._map = [[0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                if i == 0 or j == 0 or i == n - 1 or j == n - 1:
                    # граница карты
                    self._map[j][i] = -1
                else:
                    # характеристика области (-1 для непроходимой обл.)
                    self._map[j][i] = random.randint(*r)

    def get_map(self):
        return self._map


class ObjectsLevel:

    def __init__(self, step):
        # размещаем переход на след. уровень
        self.objects = [("next_lvl", step)]

    def get_objects(self, map, obj_names, r):
        # размещаем противников
        for obj_name in obj_names:
            coord = random.randint(*r), random.randint(*r)
            # ищем случайную свободную локацию
            intersect = True
            while intersect:
                intersect = False
                for obj in self.objects:
                    if coord == obj[1]:
                        intersect = True
                        coord = random.randint(*r), random.randint(*r)

            self.objects.append((obj_name, coord))

        return self.objects


class EasyLevel(AbstractLevel):

    class Map(MapLevel):

        def __init__(self):
            super().__init__(5, (0, 2))

    class Objects(ObjectsLevel):

        def __init__(self):
            super().__init__((2, 2))

        def get_objects(self, map, obj_names=None, r=(1, 3)):
            obj_names = obj_names or ["rat"]
            return super().get_objects(map, obj_names, r)


class MediumLevel(AbstractLevel):

    class Map(MapLevel):

        def __init__(self):
            super().__init__(8, (0, 2))

    class Objects(ObjectsLevel):

        def __init__(self):
            super().__init__((4, 4))

        def get_objects(self, map, obj_names=None, r=(1, 6)):
            obj_names = obj_names or ["rat", "snake"]
            return super().get_objects(map, obj_names, r)


class HardLevel(AbstractLevel):

    class Map(MapLevel):

        def __init__(self):
            super().__init__(10, (-1, 8))

    class Objects(ObjectsLevel):

        def __init__(self):
            super().__init__((5, 5))

        def get_objects(self, map, obj_names=None, r=(1, 8)):
            for obj_name in obj_names or ['rat', 'snake']:
                coord = (random.randint(*r), random.randint(*r))
                intersect = True
                while intersect:
                    intersect = False
                    if map.get_map()[coord[0]][coord[1]] == -1:
                        intersect = True
                        coord = (random.randint(*r), random.randint(*r))
                        continue
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(*r), random.randint(*r))

                self.objects.append((obj_name, coord))
            return self.objects




