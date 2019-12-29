import pygame
import random
import math

SCREEN_DIM = (800, 600)

'''
    Вам необходимо провести рефакторинг кода:

        Реализовать класс 2-мерных векторов Vec2d — определить основные математические операции: сумма Vec2d.__add__, разность Vec2d.__sub__, умножение на скаляр и скалярное умножение (Vec2d.__mul__); добавить возможность вычислять длину вектора a через len(a);добавить метод int_pair для получение пары (tuple) целых чисел.
        Реализовать класс замкнутых ломаных Polyline, с возможностями: добавление в ломаную точки (Vec2d) c её скоростью; пересчёт координат точек (set_points); отрисовка ломаной (draw_points),
        Реализовать класс Knot — потомок класса Polyline — в котором добавление и пересчёт координат инициируют вызов функции get_knot для расчёта точек кривой по добавляемым опорным.
        Все классы должны быть самостоятельными и не использовать внешние функции.

    Дополнительные задачи (для получения "положительной" оценки не обязательны):

        Реализовать возможность удаления точки из кривой.
        Реализовать возможность удаления/добавления точек сразу для нескольких кривых.
        Реализовать возможность ускорения/замедления движения кривых.

        Manual:

            ["H", "Show Help"],
            ["Esc", "Close Game"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["Z", "Delete Last Points"],
            ["↑", "Speed up"],
            ["↓", "Speed down"],
            ["→", "Increase knots"],
            ["←", "Decrease knots"],
            ["MOUSEBUTTONDOWN", "Del all points in radius=3/add point"],

'''

""" Class of methods for vectors """


class Vec2d:

    def __init__(self, *args):
        try:
            self.x, self.y = int(args[0]), int(args[1])
        except (TypeError, ValueError):
            self.x, self.y = 1., 1.

    def __sub__(self, other):
        flag = self.check_instance(other)
        return Vec2d(self.x - other, self.y - other) if flag else Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        flag = self.check_instance(other)
        return Vec2d(self.x + other, self.y + other) if flag else Vec2d(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        flag = self.check_instance(other)
        return Vec2d(self.x * other, self.y * other) if flag else Vec2d(self.x * other.x, self.y * other.y)

    __rmul__ = __mul__

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    @staticmethod
    def check_instance(other):
        if isinstance(other, int) or isinstance(other, float):
            return True
        elif isinstance(other, Vec2d):
            return False
        else:
            raise TypeError(f"Unsupported object type({type(other)})")

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:

    def __init__(self, points=None, speeds=None, knots=None):
        self._points = points or []
        self._speeds = speeds or []
        self._knots = knots or []

    def add_point(self, point, speed=None):
        self._points.append(Vec2d(*point))
        self._speeds.append(speed or Vec2d(random.random() * 2, random.random() * 2))

    # Персчитывание координат опорных точек
    def set_points(self):
        for p in range(len(self._points)):
            self._points[p] = self._points[p] + self._speeds[p]
            if self._points[p].x > SCREEN_DIM[0] or self._points[p].x < 0:
                self._speeds[p].x = -self._speeds[p].x
            if self._points[p].y > SCREEN_DIM[1] or self._points[p].y < 0:
                self._speeds[p].y = -self._speeds[p].y

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line" and len(self._points) >= 3:
            for p_n in range(-1, len(self._knots) - 1):
                pygame.draw.line(gameDisplay, color, self._knots[p_n].int_pair(),
                                 self._knots[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in self._points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)

    def remove_point(self, points=None, speeds=None):
        if points and speeds:
            for i in range(len(points)):
                self._points.remove(points[i])
                self._speeds.remove(speeds[i])
        else:
            self._points.pop() if self._points else None
            self._speeds.pop() if self._speeds else None

    def clear(self):
        self._points = []
        self._speeds = []
        self._knots = []


class Knot(Polyline):

    def __init__(self, points=None, speeds=None, knots=None, knot_count=1):
        super().__init__(points, speeds, knots)
        self.knot_count = knot_count

    def get_points_near(self, point, radius=3):
        return [enum for enum, p in enumerate(self._points) if
                abs(p.x - point.x) <= radius and abs(p.y - point.y) <= radius]

    def handle_points(self, point):
        points_near = self.get_points_near(Vec2d(*point))
        if len(points_near) > 0:
            points_to_remove = list(map(lambda x: self._points[x], points_near))
            speeds_to_remove = list(map(lambda x: self._speeds[x], points_near))
            self.remove_point(points_to_remove, speeds_to_remove)
        else:
            self.add_point(point)

    @staticmethod
    def get_point(points, alpha):
        return alpha * points[2] + (1 - alpha) * (alpha * points[1] + (1 - alpha) * points[0])

    def get_points(self, base_points):
        alpha = 1 / self.knot_count
        res = []
        for i in range(self.knot_count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self._points) >= 3:
            res = []
            for i in range(-2, len(self._points) - 2):
                ptn = [
                    (self._points[i] + self._points[i + 1]) * 0.5,
                    self._points[i + 1],
                    (self._points[i + 1] + self._points[i + 2]) * 0.5
                ]
                res.extend(self.get_points(ptn))

            return res
        return []

    def increase_knots(self):
        self.knot_count += 10 if self.knot_count < 101 else 0

    def decrease_knots(self):
        self.knot_count -= 10 if self.knot_count > 1 else 0

    def update_knot(self):
        self._knots = self.get_knot()

    def set_points(self):
        super().set_points()
        self.update_knot()

    def add_point(self, point, speed=None):
        super().add_point(point, speed)
        self.update_knot()

    def draw_knots(self, style="line", width=3, color=(50, 50, 50)):
        self.update_knot()
        super().draw_points(style, width, color)


# Отрисовка справки
def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [
        ["H", "Show Help"],
        ["Esc", "Close Game"],
        ["R", "Restart"],
        ["P", "Pause/Play"],
        ["Z", "Delete Last Points"],
        ["↑", "Speed up"],
        ["↓", "Speed down"],
        ["→", "Increase knots"],
        ["←", "Decrease knots"],
        ["MOUSEBUTTONDOWN", "Del all points in radius=3/add point"],
    ]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [(0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == '__main__':
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreen")

    handler = Knot()
    working = True
    show_help = False
    pause = True

    fps = 60
    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    handler.clear()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_UP:
                    fps += 20 if fps < 200 else 0
                    pygame.display.set_caption(f"Fps - {fps} knots count - {handler.knot_count}")
                if event.key == pygame.K_DOWN:
                    fps -= 20 if fps > 20 else 0
                    pygame.display.set_caption(f"Fps - {fps} knots count - {handler.knot_count}")
                if event.key == pygame.K_RIGHT:
                    handler.increase_knots()
                    pygame.display.set_caption(f"Fps - {fps} knots count - {handler.knot_count}")
                if event.key == pygame.K_LEFT:
                    handler.decrease_knots()
                    pygame.display.set_caption(f"Fps - {fps} knots count - {handler.knot_count}")
                if event.key == pygame.K_z:
                    handler.remove_point()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handler.handle_points(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        handler.draw_points()
        handler.draw_knots(color=color)
        if not pause:
            handler.set_points()
        if show_help:
            draw_help()
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

    pygame.display.quit()
    pygame.quit()
    exit(0)

