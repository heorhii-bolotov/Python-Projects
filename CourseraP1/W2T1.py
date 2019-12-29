import argparse
import json
import os
import tempfile


# writing and reading from file json data
# add: --key new_key --val new_val
# print values: --key old_key

def file_loader(args, storage_path):
    if args.key is None:
        raise KeyError

    def flag():
        if args.val is None:
            return "r"
        else:
            return "w+"

    data = dict()
    if os.path.exists(storage_path) and os.path.getsize(storage_path) > 0:
        with open(storage_path, "r") as file:
            data = json.loads(file.read())
    try:
        with open(storage_path, flag()) as file:
            item = data.get(args.key, None)
            if args.val is None:
                if item is not None and os.path.getsize(storage_path) > 0:
                    print(", ".join(item))
                else:
                    print("None")
            else:
                data[args.key] = [args.val, ] if item is None else data[args.key] + [args.val, ]
                json.dump(data, file, ensure_ascii=False)
    except FileNotFoundError:
        print("None")


class Parser:
    def __init__(self, parser):
        self.parser = parser

    def add_args(self, key, val):
        self.parser.add_argument(key, type=str, default=None)
        self.parser.add_argument(val, type=str, default=None)

    def input_args(self):
        # Сюда передаем значения в args = self.parser.parse_args(["--key", "key", "--val", "first"])
        args = self.parser.parse_args()
        storage_path = os.path.join(tempfile.gettempdir(), "storage.data")
        file_loader(args, storage_path)


def run():
    new_parser = Parser(argparse.ArgumentParser())
    new_parser.add_args("--key", "--val")
    new_parser.input_args()


run()