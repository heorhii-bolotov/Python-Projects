"""
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739

for k, v in metrics.items():
    print(*list(map(lambda pair: f"{k} {pair[0]} {pair[1]}", v)), sep="\n")
"""


import asyncio
from collections import defaultdict

# DB for metrics
# Works for each client
Metrics = defaultdict(list)


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = self.process_data(data.decode())
        self.transport.write(response.encode())

    def process_data(self, data: str):
        # Check command
        if data.startswith("get"):
            return self.get(data)
        elif data.startswith("put"):
            return self.put(data)
        else:
            # No such command
            return "error\nwrong command\n\n"

    def _get_response(self, **kwargs):
        lines = []

        # If no kwargs -> get all metrics
        for metric, value in (kwargs or Metrics).items():
            for pair in sorted(value, key=lambda x: x[0]):
                lines.append(f"{metric} {pair[1]} {pair[0]}")

        # Get line with metrics
        line = "\n".join(lines)

        # Response to client
        return f"ok\n{line}\n\n"

    def get(self, data):
        # Get key-metric from data
        _, key = data.rstrip().split()

        # Empty DB-metrics
        if not len(Metrics):
            return "ok\n\n"

        # Get all metrics
        if key == "*":
            return self._get_response()

        # Get key-metric
        else:
            try:
                # Get response line
                response = self._get_response(**{key: Metrics[key]})

                return response

            except KeyError:
                # Key not found
                return "ok\n\n"

    def put(self, data):

        # Use DB metric
        global Metrics

        # Parse key/values
        metric, value, timestamp = data.rstrip().split()[1:]

        # Get by key
        values = Metrics.get(metric, None)

        # Update DB metrics
        if values is None or (timestamp, value) not in values:
            Metrics[metric].append((timestamp, value))

        return "ok\n\n"

if __name__ == '__main__':
    run_server("127.0.0.1", 8888)

