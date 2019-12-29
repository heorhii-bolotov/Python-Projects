import tempfile
import os


class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current = 0

        # проверим ли есть файл, если нету - создадим новый
        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').close()

    def __str__(self):
        return "{}".format(self.file_path)

    def __add__(self, other):
        # текущая директория
        tempdir = tempfile.gettempdir()

        # содержимое первого, второго файла
        first, second = self.read(), other.read()

        # создаем новый файл
        new_file = File(os.path.join(tempdir, "file.txt"))

        # записываем все в файл
        new_file.write(first + second)

        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path, "r") as file:
            # устанавливаем позицию в файле
            file.seek(self.current)

            # считываем строку
            line = file.readline()

            # проверяем на конец файла
            if not file:
                self.current = 0
                raise StopIteration

            # меняем позицию
            self.current = file.tell()

            return line

    def write(self, text, flag=None):
        with open(self.file_path, flag or "a") as file:
            file.write(text)

    def read(self):
        with open(self.file_path, "r") as file:
            return file.read()
