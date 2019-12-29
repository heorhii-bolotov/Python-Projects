"""
    Визначити специфікації класів, що реалізують елементи графічного інтерфейсу користувача — панелі (композит) та
    кнопки (компонент). Реалізувати децентралізований механізм обробки події переміщення курсору миші. Кількість
    компонентів інтерфейсу, які реагують на цю подію, може змінюватись динамічно.

    Pattern: Visitor

    ABC Component
        class Panel
        class Button
    ABC Visitor
        class Cursor
"""

from random import choice


class Component(object):
    """
        Component class
        prints when it is visited
    """
    def __init__(self, name, on=True):
        self.name = name
        self._on = on

    def __str__(self):
        return self.__class__.__name__ + self.name

    def off(self):
        self._on = False

    def on(self):
        self._on = True

    def targetted(self, visitor):
        visitor.visit(self)

    def activate(self, cursor):
        if self._on:
            print(f'{self} is on by {cursor}')
        else:
            print(f'{self} is off')


class Panel(Component):
    """
        class Panel
        inherits Component class
    """
    def __init__(self, name, on=True, children=None):
        super().__init__(name, on)
        self.name = name
        self.components = children or []

    def addChild(self, child):
        self.components.append(child)

    def removeChild(self, child):
        self.components.remove(child)


class Button(Component):
    """
        class Button
        inherits Component class
    """
    def __init__(self, name, on=True):
        super().__init__(name, on)
        self.name = name


class Visitor:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.__class__.__name__ + self.name


class Cursor(Visitor):
    """
        class Cursor
        Visitor object class
        activates component in method visit
    """
    def __init__(self, name):
        super().__init__(name)

    def visit(self, component):
        component.activate(self)


def generateComponents(n):
    """
        generates Components subclasses objects
    """
    components = Component.__subclasses__()
    for i in range(n):
        yield choice(components)(str(i), choice([True, False]))


def main():
    cursor1 = Cursor('1')
    cursor2 = Cursor('2')
    for component in generateComponents(5):
        component.targetted(cursor1)
        activate = choice([component.on, component.off])
        activate()
        component.targetted(cursor2)


if __name__ == '__main__':
    main()
