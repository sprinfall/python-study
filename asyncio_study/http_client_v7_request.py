import asyncio


class ClientRequest:
    def __init__(self, method, url, host):
        self.method = method.upper()
        self.url = url
        self.host = host

    def send(self, protocol):
        crlf = '\r\n'

        # Start line
        request = '{} {} HTTP/1.1'.format(self.method, self.url)
        request += crlf

        # Header fields
        request += 'Host: {}'.format(self.host)
        request += crlf

        request += crlf  # End of Headers

        protocol.transport.write(request.encode())


class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    async def request(self, url, host):
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop), host, 80)

        req = ClientRequest('GET', url, host)
        req.send(protocol)


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
        print('Stop the event loop.')
        self.loop.stop()


async def main(loop):
    session = ClientSession(loop)
    await session.request('/w/', 'en.cppreference.com')


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.run_forever()
