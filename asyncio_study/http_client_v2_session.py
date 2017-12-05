import asyncio

# HTTP client sending a GET request.
# Add ClientSession.

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        print('Connection made.')
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        print('Connection lost.')
        self.loop.stop()


class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    # Send HTTP GET request.
    async def get(self, url, host, port):
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop), host, port)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)

        # Send the request.
        transport.write(request.encode())


async def main(loop):
    session = ClientSession(loop)
    await session.get('/', 'localhost', 8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.run_forever()
