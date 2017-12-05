import asyncio

# HTTP client sending a GET request.

class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print('Connection made.')
        request = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'
        transport.write(request.encode())

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        print('Connection lost.')
        print('Stop the event loop.')
        self.loop.stop()


async def main(loop):
    await loop.create_connection(
        lambda: ClientProtocol(loop), 'localhost', 8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
# Without run_forever() the loop will end before receive any data.
# The loop will be stopped when connection is lost.
loop.run_forever()


# Another HTTP (Non-SSL) server for testing:
# Request: 'GET /w/ HTTP/1.1\r\nHost: en.cppreference.com\r\n\r\n'
# URL:  /w/
# Host: en.cppreference.com
# Port: 80

