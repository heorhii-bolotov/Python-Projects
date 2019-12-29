import sys
from os.path import splitext
import csv


class CarBase:
    """ Базовый класс """

    # колонки:
    c_car_type = 0
    c_brand = 1
    c_passenger_seats_count = 2
    c_photo_file_name = 3
    c_body_whl = 4
    c_carrying = 5
    c_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        return splitext(self.photo_file_name)[1]


class Car(CarBase):
    """ Класс легковой автомобиль """

    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    @classmethod
    def from_tuple(cls, row):
        """ Метод для создания экземпляра легкового автомобиля
            из строки csv-файла"""

        return cls(
            row[cls.c_brand],
            row[cls.c_photo_file_name],
            row[cls.c_carrying],
            row[cls.c_passenger_seats_count],
        )


class Truck(CarBase):
    """ Класс грузовой автомобиль """

    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        # поле body_whl
        try:
            self.body_width, self.body_height, self.body_length = (float(i) for i in body_whl.split('x', 2))
        except ValueError:
            self.body_width, self.body_height, self.body_length = [.0] * 3

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length

    @classmethod
    def from_tuple(cls, row):
        return cls(
            row[cls.c_brand],
            row[cls.c_photo_file_name],
            row[cls.c_carrying],
            row[cls.c_body_whl],
        )


class SpecMachine(CarBase):
    """ Класс спецтехника """

    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @classmethod
    def from_tuple(cls, row):
        return cls(
            row[cls.c_brand],
            row[cls.c_photo_file_name],
            row[cls.c_carrying],
            row[cls.c_extra],
        )


def get_car_list(csv_filename):
    with open(csv_filename) as csv_file:

        # создаем обьект csv.reader для чтения из csv-файла
        reader = csv.reader(csv_file, delimiter=';')

        # пропускаем заголовок
        next(reader)

        # список экземпляров техники
        car_list = []

        # создаем словарь тип техники: класс техники
        get_type = {car_class.car_type: car_class for car_class in (Car, Truck, SpecMachine)}

        for row in reader:
            try:
                # узнаем тип автомобиля
                car_type = row[CarBase.c_car_type]
            except IndexError:
                # если нет колонки,  пропускаем
                continue

            try:
                # узнаем класс автомобиля, обьект которого нужно создать
                # добавим в car_list
                car_class = get_type[car_type]
            except KeyError:
                # если тип неизвестен
                continue

            try:
                # создаем и добавляем обьект в car_list
                car_list.append(car_class.from_tuple(row))
            except (ValueError, IndexError):
                # игнорируем если данные некорректны
                pass

    return car_list


if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))



# первый вариант
"""from os.path import splitext
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying: str):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying: float = float(carrying)

    def get_photo_file_ext(self) -> str:
        return splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying: str, passenger_seats_count: str):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count: int = int(passenger_seats_count)
        self.car_type = "car"


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying: str, body_whl: str): # body_whl can be empty
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"
        self.body_width, self.body_height, self.body_length = [0.0] * 3 if not len(body_whl) else list(map(lambda i: float(i), body_whl.split("x")))

    def get_body_volume(self) -> float:
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying: str, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = "spec_machine"
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as f:
        reader = csv.reader(f, delimiter=";")
        params = {i: j for i, j in zip(("car", "truck", "spec_machine"), ((1, 2, 3, 5), (1, 3, 4, 5), (1, 3, 5, 6)))}
        next(reader)
        for row in reader:
            attr = []
            if not len(row) or not len(row[0]): continue
            for i in params[row[0]]:
                if not len(row[i]):
                    if row[0] != "truck" and i != 4: continue
                attr.append(row[i])
            if row[0] == "car":
                car_list.append(Car(attr[0], attr[2], attr[3], attr[1]))
            elif row[0] == "truck":
                car_list.append(Truck(attr[0], attr[1], attr[3], attr[2]))
            elif row[0] == "spec_machine":
                car_list.append(SpecMachine(attr[0], attr[1], attr[2], attr[3]))
            else:
                raise NameError

    return car_list

# obj = get_car_list("/Users/macair/Downloads/_af3947bf3a1ba3333b0c891e7a8536fc_coursera_week3_cars.csv")
"""