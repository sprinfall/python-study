# encoding: utf-8

import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()

# Each client connection will create a new protocol instance

# NOTE: loop.create_server() is a coroutine (function), it returns a coroutine
# object.
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)

# Running the coroutine object in the loop will return a server.
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()  # Close the sockets.
# NOTE: server.wait_closed() is a coroutine.
loop.run_until_complete(server.wait_closed())
loop.close()
