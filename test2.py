def print_maze(maze, x, y):
    for i in range(len(maze)):
        s = ''
        for j in range(len(maze)):
            if i == x and j == y:
                s += 'X'
            elif maze[i][j] == 1:
                s += '1'
            else:
                s += '.'
        print(s)
    print(' ')


class MazeRunner(object):

    def __init__(self, maze, start, finish):
        self.__maze = maze
        self.__rotation = (1, 0)
        self.__x = start[0]
        self.__y = start[1]
        self.__finish = finish

    def __getitem__(self, item):
        if item == 0:
            return self.__x, self.__y

    def go(self):
        x = self.__x + self.__rotation[0]
        y = self.__y + self.__rotation[1]
        if x > len(self.__maze) - 1 or y > len(self.__maze) - 1 or x < 0 or y < 0 or self.__maze[x][y] == 1:
            return False
        self.__x = x
        self.__y = y
        # print_maze(self.__maze, self.__x, self.__y)
        return True

    def turn_left(self):
        left_rotation = {
            (0, 1): (1, 0),
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
            (-1, 0): (0, 1),
        }
        self.__rotation = left_rotation[self.__rotation]
        return self

    def turn_right(self):
        right_rotation = {
            (1, 0): (0, 1),
            (0, -1): (1, 0),
            (-1, 0): (0, -1),
            (0, 1): (-1, 0),
        }
        self.__rotation = right_rotation[self.__rotation]
        return self

    def found(self):
        return self.__x == self.__finish[0] and self.__y == self.__finish[1]


def maze_controller(mr):
    from copy import deepcopy
    from collections import deque

    def cycle(mr, pos, path):
        def down_():
            down = mr.go()
            pos['down'] = down
            if down:
                mr.turn_right(), mr.turn_right()
                mr.go()
                mr.turn_right(), mr.turn_right()

        def right_():
            mr.turn_left()
            right = mr.go()
            pos['right'] = right
            if right:
                mr.turn_left(), mr.turn_left()
                mr.go()
                mr.turn_left()
            else:
                mr.turn_right()

        def up_():
            mr.turn_right(), mr.turn_right()
            up = mr.go()
            pos['up'] = up
            if up:
                mr.turn_left(), mr.turn_left()
                mr.go()
            else:
                mr.turn_left(), mr.turn_left()

        def left_():
            mr.turn_right()
            left = mr.go()
            pos['left'] = left
            if left:
                mr.turn_left(), mr.turn_left()
                mr.go()
                mr.turn_right(),
            else:
                mr.turn_left()

        for k, v in pos.items():
            if v is not None:
                if k == 'down':
                    down_()
                elif k == 'right':
                    right_()
                elif k == 'up':
                    up_()
                elif k == 'left':
                    left_()

        vertices = []
        for k, v in pos.items():
            if v:
                tmp_pos = dict(zip(['left', 'up', 'right', 'down'], [False] * 4))
                if k == 'down':
                    tmp_pos['up'] = None
                    mr.go()
                    vertices.append((deepcopy(mr), tmp_pos, path + [k]))
                    mr.turn_left(), mr.turn_left(), mr.go(), mr.turn_right(), mr.turn_right()
                elif k == 'right':
                    tmp_pos['left'] = None
                    mr.turn_left(), mr.go(), mr.turn_right()
                    vertices.append((deepcopy(mr), tmp_pos, path + [k]))
                    mr.turn_right(), mr.go(), mr.turn_left()
                elif k == 'up':
                    tmp_pos['down'] = None
                    mr.turn_left(), mr.turn_left(), mr.go(), mr.turn_right(), mr.turn_right()
                    vertices.append((deepcopy(mr), tmp_pos, path + [k]))
                    mr.go()
                elif k == 'left':
                    tmp_pos['right'] = None
                    mr.turn_right(), mr.go(), mr.turn_left()
                    vertices.append((deepcopy(mr), tmp_pos, path + [k]))
                    mr.turn_left(), mr.go(), mr.turn_right()
        if not vertices:
            if mr.found():
                vertices.append((deepcopy(mr), pos, path))

        return vertices

    def bfs(mr, pos):
        pos = dict(zip(['left', 'up', 'right', 'down'], [False] * 4))
        queue = deque([(mr, pos, [])])

        while queue:
            tmp_mr, tmp_pos, tmp_path = queue.popleft()
            for mr_, pos_, path_ in cycle(tmp_mr, tmp_pos, tmp_path):
                if tmp_mr.found():
                    return tmp_path
                else:
                    queue.append((mr_, pos_, path_))

    pos = dict(zip(['left', 'up', 'right', 'down'], [False] * 4))
    path = bfs(mr, pos)
    for step in path:
        if step == 'down':
            mr.go()
        elif step == 'right':
            mr.turn_left(), mr.go(), mr.turn_right()
        elif step == 'up':
            mr.turn_left(), mr.turn_left(), mr.go(), mr.turn_right(), mr.turn_right()
        else:
            mr.turn_right(), mr.go(), mr.turn_left()



# maze_example1 = {
#     'm': [
#         [0, 1, 0, 0, 0],
#         [0, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 0],
#         [0, 0, 0, 1, 0],
#     ],
#     's': (0, 0),
#     'f': (4, 4)
# }
#
# maze_runner = MazeRunner(maze_example1['m'], maze_example1['s'], maze_example1['f'])  # ініціалізація робота
# maze_controller(maze_runner)  # виклик вашої функції
# print(maze_runner.found())  # перевірка того, що артефакт знайдено, повинно бути True
#
# maze_example2 = {
#     'm': [
#         [0, 0, 0, 0, 0, 0, 0, 1],
#         [0, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 0, 1, 0, 1],
#         [0, 0, 0, 0, 0, 1, 0, 1],
#         [0, 1, 0, 1, 1, 1, 1, 1],
#         [1, 1, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 1, 1, 1, 1, 0],
#     ],
#     's': (7, 7),
#     'f': (0, 0)
# }
#
# maze_runner = MazeRunner(maze_example2['m'], maze_example2['s'], maze_example2['f'])  # ініціалізація робота
# maze_controller(maze_runner)  # виклик вашої функції
# print(maze_runner.found())  # перевірка того, що артефакт знайдено, повинно бути True
#
# maze_example3 = {
#     'm': [
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
#         [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
#         [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
#     ],
#     's': (0, 5),
#     'f': (10, 5)
# }
#
# maze_runner = MazeRunner(maze_example3['m'], maze_example3['s'], maze_example3['f'])  # ініціалізація робота
# maze_controller(maze_runner)  # виклик вашої функції
# print(maze_runner.found())  # перевірка того, що артефакт знайдено, повинно бути True
#
#
# maze_example4 = {
#     'm': [
#         [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
#         [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
#         [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1],
#         [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
#         [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
#         [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
#         [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#         [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     ],
#     's': (0, 5),
#     'f': (4, 5)
# }
#
# maze_runner = MazeRunner(maze_example4['m'], maze_example4['s'], maze_example4['f'])  # ініціалізація робота
# maze_controller(maze_runner)  # виклик вашої функції
# print(maze_runner.found())  # перевірка того, що артефакт знайдено, повинно бути True
#
#
# maze_example5 = {
#     'm': [
#         [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#         [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
#         [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
#         [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
#         [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
#         [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
#         [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
#     ],
#     's': (0, 5),
#     'f': (4, 5)
# }
#
# maze_runner = MazeRunner(maze_example5['m'], maze_example5['s'], maze_example5['f'])  # ініціалізація робота
# print_maze(maze_example5['m'], *maze_example5['s'])
# maze_controller(maze_runner)  # виклик вашої функції
# print(maze_runner.found())  # перевірка того, що артефакт знайдено, повинно бути True
