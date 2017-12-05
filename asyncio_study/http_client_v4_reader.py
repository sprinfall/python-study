import asyncio

# HTTP client sending a GET request.
# Add class Reader using bytearray to buffer the received data.
# Based on http_client_v3_wait.py.


class Reader:
    def __init__(self, loop):
        self._loop = loop
        self._buffer = bytearray()
        self._eof = False  # EOF received or not.
        self._waiter = None  # A future used to wait for data.

    def feed(self, data):
        self._buffer.extend(data)
        self._wakeup_waiter()

    def feed_eof(self):
        self._eof = True
        self._wakeup_waiter()

    async def read(self):
        blocks = []
        while True:
            block = await self._read()
            if not block:
                break
            blocks.append(block)
        data = b''.join(blocks)
        return data

    async def _read(self):
        # Wait for more data if buffer is empty and EOF hasn't been received.
        if not self._buffer and not self._eof:
            await self._wait_for_data()

        data = bytes(self._buffer)
        del self._buffer[:]

        return data

    async def _wait_for_data(self):
        assert not self._eof
        assert not self._waiter

        self._waiter = self._loop.create_future()
        await self._waiter
        self._waiter = None

    def _wakeup_waiter(self):
        waiter = self._waiter
        if waiter:
            self._waiter = None
            waiter.set_result(None)


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop, reader):
        self.loop = loop
        self.transport = None
        self._reader = reader

    def connection_made(self, transport):
        print('Connection made.')
        self.transport = transport

    def data_received(self, data):
        # print("data received: {!r}".format(data.decode()))
        self._reader.feed(data)

    def eof_received(self):
        self._reader.feed_eof()

    def connection_lost(self, exc):
        print('Connection lost.')


class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    async def get(self, url, host, port):
        reader = Reader(self._loop)

        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop, reader), host, port)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)

        # Send the request.
        transport.write(request.encode())

        # Read the response data.
        data = await reader.read()
        print(data.decode())


async def main(loop):
    session = ClientSession(loop)
    await session.get('/', 'localhost', 8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
