

"""
    CLIENT SERVER 5WEEK
"""


import time
import socket
from collections import defaultdict

"""
    cmd + R - cool tool

import socket
# to create TCP-socket use socket.AF_INET for family and socket.SOCK_STREAM for type
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(host, port)

"""

class ClientError(Exception):
    """
        Socket errors
    """
    def __call__(self, *args):
        return self.__class__(*(self.args + args))

    def __init__(self, *args):
        super(ClientError, self).__init__(*args)

        # Create TCP/IP socket
        # self.socket = socket.socket()

        # Bind socket to the port
        # server_addr = (host, port)
        # self.socket.connect(server_addr)

        # Set timeout
        # self.socket.settimeout(timeout)

class Client:
    def __init__(self, host, port, timeout=None):
        # Create TCP/IP client socket
        # Bind to port
        # Set timeout
        try:
            self.socket = socket.create_connection((host, port), timeout=timeout)
        except socket.error as err:
            raise ClientSocketError("connection ", err)

    def get(self, metric):
        # Create command line
        line = " ".join(["get", metric + "\n"])

        # Send metric
        self.socket.sendall(line.encode("utf-8"))

        while True:
            try:
                # Get answer
                data = self.socket.recv(1024).decode("utf-8")

            # Check time on blocking operations
            except socket.timeout as err:
                print(err.args)
                self.close()
                break

            # Check other error
            except socket.error as err:
                self.close()
                raise ClientError(*err.args)

            # Check answer
            if not data.startswith("ok"):
                raise ClientError

            # Get and then return metrics
            return self.from_dict(data)

    def put(self, metric, value, timestamp=int(time.time())):
        # Create command line
        line = " ".join(["put", metric, str(value), str(timestamp) + "\n"])

        # Send metric
        self.socket.sendall(line.encode("utf-8"))

        try:
            # Get answer
            data = self.socket.recv(1024).decode("utf-8")

            # Check answer
            if data.startswith("error"):
                raise ClientError

        # Check time on blocking operations
        except socket.timeout as err:
            print(err.args)
            self.close()

    @staticmethod
    def from_dict(data):
        # Key
        x_metric = 0
        # Values
        x_timestamp = 2
        x_value = 1

        # Strip ("ok\n", "\n\n")
        data = data[3:-2]

        # Check empty answer
        if not len(data):
            return {}

        #       neardrum.cpu 15.3 1501864259\npalm.cpu 10.5 1501864247
        #  [ [neardrum.cpu, 15.3, 1501864259], [palm.cpu, 10.5, 1501864247] ]
        lines = list(map(lambda i: i.split(" "), data.split("\n")))

        # Create metrics
        metrics = defaultdict(list)
        for line in lines:
            metrics[line[x_metric]].append((int(line[x_timestamp]), float(line[x_value])))

        return metrics

    def close(self):
        self.socket.close()

    def __del__(self):
        self.socket.close()