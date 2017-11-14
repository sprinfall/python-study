import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        message = input('Type a message: ')
        transport.write(message.encode())
        print('Data sent: {!r}'.format(message))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    def data_received(self, data):
        print('Data received: {}'.format(data))

loop = asyncio.get_event_loop()

# loop.create_connection() is a coroutine which will try to establish the
# connection in the background.  When successful, the coroutine returns a
# (transport, protocol) pair.
coro = loop.create_connection(lambda: EchoClientProtocol(loop),
                              '127.0.0.1', 8888)

transport, protocol = loop.run_until_complete(coro)
print('transport: {}, protocol: {}'.format(transport, protocol))

loop.run_forever()
loop.close()
