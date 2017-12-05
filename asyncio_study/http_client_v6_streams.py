import asyncio

# HTTP client sending a GET request.
# Use streams to send and receive data.

class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    # Send HTTP GET request.
    async def get(self, url, host, port):
        # asyncio.open_connection() is a wrapper of loop.create_connection().
        reader, writer = await asyncio.open_connection(
            host, port, loop=self._loop)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)

        # Send the request.
        writer.write(request.encode())

        # Receive the data.
        # -1 means read until EOF.
        data = await reader.read(-1)
        print(data.decode())

        # Close the socket.
        writer.close()


async def main(loop):
    session = ClientSession(loop)
    await session.get('/', 'localhost', 8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
