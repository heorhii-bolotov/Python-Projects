import sys


def check_err(func):
    def wrapper(self):
        try:
            return func(self)
        except IOError:
            return ""
    return wrapper


class FileReader:
    def __init__(self, path):
        self.path = path

    @check_err
    def read(self):
        with open(self.path, "r") as f:
            return f.read()


reader = FileReader(sys.argv[1])
print(reader.read())