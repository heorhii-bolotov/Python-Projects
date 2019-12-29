"""
Визначити специфікації класів для елементу ігрового поля (комірки) та самого простору.
Забезпечити слабку зв'язаність елементів. Реалізувати централізований механізм сумісної зміни стану елементів.

Pattern: Observer

Structure:
    class Playground(игорове поле), Observable object

    class Element(игрок)
    class Game(игра)
"""

from random import randint
from abc import ABC, abstractmethod


class ObservableEngine(ABC):
    @abstractmethod
    def up(self, object):
        pass

    @abstractmethod
    def down(self, object):
        pass

    @abstractmethod
    def right(self, object):
        pass

    @abstractmethod
    def left(self, object):
        pass


class Playground(ObservableEngine):
    """
        Class Playground
        Inherits Observable Abstract class
        Handles Observers(players) and creates play field
    """
    def __init__(self):
        self.objects = set()
        self.generateGrid()
        self.createObject()

    def generateGrid(self):
        """
            Generates 2d array 10x10 size
        """
        self.field = [[0 for __ in range(10)] for _ in range(10)]
        for i in range(randint(1, 10)):
            self.field[randint(0, 9)][randint(0, 9)] = 1
        for i in self.field:
            print(i)

    def createObject(self, object=None):
        """
            Creates new object
            :param object: Observer object(Element) to add in grid
        """
        name = str(len(self.objects))
        for i in range(len(self.field)):
            for j in range(len(self.field)):
                if self.field[i][j] == 0:
                    pos = i, j
                    object = object or Element(name, pos)
                    self.objects.add(object)
                    self.field[i][j] = object
                    for i in self.field:
                        print(i)
                    return

    def up(self, object):
        x, y = object.getPos()
        if y == 0 or self.field[x][y - 1] != 0:
            return
        else:
            self.field[x][y] = 0
            x, y = x, y - 1
            self.field[x][y] = object
            object.changePos((x, y))

            object.notify(f'{object.name} up, coords: {object.getPos()}')

    def down(self, object):
        x, y = object.getPos()
        if y == 9 or self.field[x][y + 1] != 0:
            return
        else:
            self.field[x][y] = 0
            x, y = x, y + 1
            self.field[x][y] = object
            object.changePos((x, y))

            object.notify(f'{object.name} down, coords: {object.getPos()}')

    def right(self, object):
        x, y = object.getPos()
        if x == 9 or self.field[x + 1][y] != 0:
            return
        else:
            self.field[x][y] = 0
            x, y = x + 1, y
            self.field[x][y] = object
            object.changePos((x, y))

            object.notify(f'{object.name} right, coords: {object.getPos()}')

    def left(self, object):
        x, y = object.getPos()
        if x == 0 or self.field[x - 1][y] != 0:
            return
        else:
            self.field[x][y] = 0
            x, y = x - 1, y
            self.field[x][y] = object
            object.changePos((x, y))

            object.notify(f'{object.name} left, coords: {object.getPos()}')


class AbstractObserver(ABC):
    @abstractmethod
    def notify(self, message, *params):
        pass


class Element(AbstractObserver):
    """
        Observer class object
    """
    def __init__(self, name, pos, **params):
        self.name = name
        self.params = params
        self.pos = pos

    def changePos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def notify(self, message, *params):
        """
            Sends message after action
            :param message: message to print(position of the object in grid and its name)
            :param params: other
        """
        print(message)


class Game:
    """
        class Game
        initializes Playground class object and start game with method start
    """
    def __init__(self):
        self.playground = Playground()
        self.on = False

    def start(self):
        self.on = True

    def end(self):
        self.on = False

    def getObjects(self):
        """
        :return: all Observer objects(Element) in the field <Playground.objects>
        """
        return self.playground.objects


def main():
    """
        main function
        Runs new Game(), updates actions for each Object in Playground
    """
    game = Game()
    game.start()
    while game.on:
        for object in game.getObjects():
            command = input('? ')
            while command:
                if command == 'create':
                    pass
                elif command == 'delete':
                    pass
                elif command == 'up':
                    game.playground.up(object)
                elif command == 'down':
                    game.playground.down(object)
                elif command == 'right':
                    game.playground.right(object)
                elif command == 'left':
                    game.playground.left(object)
                command = input('? ')

        next_ = input('Next? ')
        if not next_:
            game.end()


if __name__ == '__main__':
    main()