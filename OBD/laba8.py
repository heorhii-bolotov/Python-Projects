"""
Визначити специфікації класів для подання файлової системи у вигляді дерева об’єктів. Реалізувати механізм
клонування таких об’єктів з параметром глибини.

Pattern: Prototype

class Prototype
class Path
    class Directory
    class File
"""

import os
from copy import deepcopy
from random import randint


class Prototype:
    """
        Prototype class
        Make Copies of other objects, in our case Dirs and files
    """

    def __init__(self):
        self._obj = None

    def clone(self):
        obj = deepcopy(self._obj)
        if issubclass(type(obj), (File, Path, Directory)):
            obj._name = f'{obj._name}{randint(1, 100)}'
        return obj

    obj = property()

    @obj.getter
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):
        self._obj = value

    @obj.deleter
    def obj(self):
        self._obj = None


class Path(object):
    """
        Class Path
        Parent for Directory and File classes
    """

    def __init__(self, path):
        self.__path = path

    def pwd(self):
        print(self.__path)

    def _path(self):
        return self.__path


class Directory(Path):
    """
        Class Directory
        Composite class for Leaf objects(Files) and other Composites
    """

    def __init__(self, name=None, path=os.getcwd(), delim=''):
        path = os.path.join(path, name) if name else path
        super().__init__(path)
        self._name = os.path.basename(path)
        self.__dchildren = set()
        self.__fchildren = set()
        self.delim = delim

    def getDirs(self):
        return self.__dchildren

    def getFiles(self):
        return self.__fchildren

    def ls(self):
        print(f'{self.delim}Current {self._name}')
        delim = self.delim + "- "
        for i in self.__dchildren:
            print(f'{delim}{i._name}')
        for i in self.__fchildren:
            print(f'{delim}{i._name}')

    def touch(self, name):
        for f in self.__fchildren:
            if name == f._name:
                print(f'file {name} already exists')
                return
        self.__fchildren.add(File(name, self._path()))

    def rm(self, name):
        for f in list(self.__fchildren):
            if name == f._name:
                self.__fchildren.remove(f)
                return
        print(f'file {name} not found')

    def mkdir(self, name):
        for d in self.__dchildren:
            if name == d._name:
                print(f'dir {name} already exists')
                return
        self.__dchildren.add(Directory(name, self._path(), delim=self.delim + "- "))

    def rmdir(self, name):
        for d in list(self.__fchildren):
            if name == d._name:
                self.__fchildren.remove(d)
                return
        print(f'dir {name} not found')


class File(Path):
    """
        Class File
        Leaf object
    """

    def __init__(self, name, path=os.getcwd()):
        super().__init__(os.path.join(path, name))
        self._name = name

    def ls(self):
        print(f'{self._name}')


def main():
    dir = Directory()
    dir.pwd()
    dir.ls()

    for i in range(2):
        dir.touch(name=f'f{i + 1}.txt')
        dir.mkdir(name=f'd{i + 1}')
    dir.ls()
    for enum, d in enumerate(dir.getDirs()):
        d.pwd()
        d.touch(name=f'{enum + 1}.txt')
        d.mkdir(name=f'{enum + 1}')
        d.ls()

    prototype = Prototype()
    prototype.obj = dir
    cloned_dir = prototype.clone()
    cloned_dir.pwd()
    cloned_dir.ls()


if __name__ == '__main__':
    main()
