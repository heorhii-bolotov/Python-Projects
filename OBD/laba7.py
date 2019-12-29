"""
Визначити специфікації класу, що подає мережеве з'єднання протоколу TCP.
Реалізувати зміну поведінки в залежності від стану з'єднання (LISTENING,
ESTABLISHED, CLOSED) без використання громіздких умовних операторів.

Pattern: State

class TcpConnection
class TcpState
    class TcpClosed
    class TcpEstablished
    class TcpListen
"""

from abc import ABC, abstractmethod


class TcpConnection:
    def __init__(self):
        self.__state: TcpState = TcpClosed().instance()

    def Open(self):
        self.__state.Open(self)

    def Close(self):
        self.__state.Close(self)

    def Send(self):
        self.__state.Send(self)

    def _setState(self, state):
        """
            Sets new State for self.__state field
            :param state: TcpState instance
        """
        self.__state = state


class TcpState(ABC):
    """
        Abstract class TcpState
        Defines TCP state connection
    """

    @abstractmethod
    def Open(self, context: TcpConnection):
        """
            Opens Tcp connection
        """
        pass

    @abstractmethod
    def Close(self, context: TcpConnection):
        """
            Closes Tcp connection
        """
        pass

    @abstractmethod
    def Send(self, context: TcpConnection):
        """
            Establishes Tcp connection between the user
        """
        pass


class TcpClosed(TcpState):
    """
        class TcpClosed
        Defines closed TCP-connection state
    """

    def __init__(self):
        self.__instance: TcpState = None

    def instance(self) -> TcpState:
        if not self.__instance:
            self.__instance = TcpClosed()
        return self.__instance

    def Open(self, context: TcpConnection):
        print('Opens TCP connection')
        context._setState(TcpListen().instance())

    def Close(self, context: TcpConnection):
        pass

    def Send(self, context: TcpConnection):
        pass


class TcpEstablished(TcpState):
    """
        class TcpEstablished
        Defines established TCP-connection state
    """

    def __init__(self):
        self.__instance: TcpState = None

    def instance(self) -> TcpState:
        if not self.__instance:
            self.__instance = TcpEstablished()
        return self.__instance

    def Close(self, context: TcpConnection):
        print('Closes established TCP connection')
        context._setState(TcpClosed().instance())

    def Open(self, context: TcpConnection):
        pass

    def Send(self, context: TcpConnection):
        pass


class TcpListen(TcpState):
    """
        class TcpListen
        Defines in-progress TCP-connection state
    """

    def __init__(self):
        self.__instance: TcpState = None

    def instance(self) -> TcpState:
        if not self.__instance:
            self.__instance = TcpListen()
        return self.__instance

    def Send(self, context: TcpConnection):
        print('Sends SYN, gets SYN-ACK, sends ACK')
        context._setState(TcpEstablished().instance())

    def Close(self, context: TcpConnection):
        print('Stops listening')
        context._setState(TcpClosed().instance())

    def Open(self, context: TcpConnection):
        pass


def main():
    tcp_connection = TcpConnection()

    print(f'-------test{1}-------')
    tcp_connection.Open()
    tcp_connection.Send()
    tcp_connection.Close()
    print(f'-------test{2}-------')
    tcp_connection.Open()
    tcp_connection.Close()


if __name__ == '__main__':
    main()
