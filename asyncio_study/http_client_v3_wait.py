import asyncio

# HTTP client sending a GET request.
# Add an extra future to the loop to wait for the data.


class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

        self._eof = False  # EOF received or not.
        self._waiter = None  # A future used to wait for data.

    def connection_made(self, transport):
        print('Connection made.')
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

    def eof_received(self):
        self._eof = True
        self._wakeup_waiter()

    def connection_lost(self, exc):
        print('Connection lost.')
        # No more self.loop.stop()

    async def wait_for_data(self):
        assert not self._eof

        # Or
        #   if self._waiter:
        #       raise RuntimeError(
        #           'Another coroutine is already waiting for data.')
        assert not self._waiter

        self._waiter = self.loop.create_future()
        await self._waiter
        self._waiter = None

    def _wakeup_waiter(self):
        waiter = self._waiter
        if waiter:
            self._waiter = None
            # The data has been received, mark the waiter future done
            # so that the loop could end.
            # Or,
            #   if not waiter.cancelled()
            #       waiter.set_result(None)
            waiter.set_result(None)


class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    async def get(self, url, host, port):
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop), host, port)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)

        # Send the request.
        transport.write(request.encode())

        # Wait for the data to be received.
        await protocol.wait_for_data()


async def main(loop):
    session = ClientSession(loop)
    await session.get('/', 'localhost', 8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
# No more loop.run_forever()
