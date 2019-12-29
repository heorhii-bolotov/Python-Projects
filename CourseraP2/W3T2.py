from abc import ABC, abstractmethod


class System:

    def __init__(self):
        self.map = self.grid = self._get_grid()
        self.map[5][7] = 1  # Lights
        self.map[5][2] = -1  # Obstacles

    @staticmethod
    def _get_grid(dim=None):
        dim = dim or (30, 20)
        return [[0 for __ in range(dim[0])] for _ in range(dim[1])]

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class MappingProcessor(ABC):

    @abstractmethod
    def lighten(self, grid):
        pass


class Light:

    def __init__(self, dim):
        self.dim = dim  # (W/H)
        self.grid = self._get_grid()
        self.lights = []
        self.obstacles = []

    def _get_grid(self):
        return [[0 for __ in range(self.dim[0])] for _ in range(self.dim[1])]

    def set_dim(self, dim):
        self.dim = dim
        self.grid = self._get_grid()

    def generate_lights(self):
        return self.grid.copy()

    def _set_item(self, items, delta):
        pass

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()


class MappingAdapter(MappingProcessor):

    def __init__(self, adaptee):
        self.adaptee = adaptee  # object to be connected to adapter

    def lighten(self, grid):
        dim = len(grid[0]), len(grid)
        self.adaptee.set_dim(dim)

        lights = []
        obstacles = []

        for row, i in enumerate(grid):
            for col, j in enumerate(i):
                if j == 1:
                    lights.append((col, row))
                elif j == -1:
                    obstacles.append((col, row))

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)

        return self.adaptee.generate_lights()


system = System()
light = Light((30, 20))
adapter = MappingAdapter(light)
system.get_lightening(adapter)
