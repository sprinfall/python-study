import asyncio

# HTTP client sending a GET request.
# Add class Writer to send request.


class Writer:
    def __init__(self, transport):
        self._transport = transport

    def write(self, data):
        self._transport.write(data)


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
        self._reader.feed(data)

    def eof_received(self):
        self._reader.feed_eof()

    def connection_lost(self, exc):
        print('Connection lost.')


async def open_connection(host, port, loop):
    reader = Reader(loop)
    protocol = ClientProtocol(loop, reader)
    transport, _ = await loop.create_connection(lambda: protocol, host, port)
    writer = Writer(transport)
    return reader, writer


class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    async def get(self, url, host, port):
        reader, writer = await open_connection(host, port, self._loop)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)

        # Send the request.
        writer.write(request.encode())

        # Read the response data.
        data = await reader.read()
        print(data.decode())



async def main(loop):
    session = ClientSession(loop)
    await session.get('/', 'localhost', 8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
