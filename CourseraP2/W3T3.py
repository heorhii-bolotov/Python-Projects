from abc import ABC, abstractmethod


class Engine(ABC):

    @abstractmethod
    def subscribe(self, subscriber):
        pass

    @abstractmethod
    def unsubscribe(self, subscriber):
        pass

    @abstractmethod
    def notify(self, message):
        pass


class ObservableEngine(Engine):

    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        try:
            self.__subscribers.remove(subscriber)
        except ValueError:
            pass

    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message["title"])


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if message not in self.achievements:
            self.achievements.append(message)


# obs = ObservableEngine()
#
# short = ShortNotificationPrinter()
# full = FullNotificationPrinter()
#
# obs.subscribe(short)
# obs.subscribe(full)
#
# obs.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
# obs.notify({"title": "Покоритель1", "text": "Дается при выполнении всех заданий в игре1"})
# obs.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
# obs.notify({"title": "Покоритель2", "text": "Дается при выполнении всех заданий в игре2"})
# obs.notify({"title": "Покоритель1", "text": "Дается при выполнении всех заданий в игре1"})
# print(short.achievements, full.achievements,  sep="\n")