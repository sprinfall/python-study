# Python 的异步 IO：Asyncio 之 TCP Client

## 一个简单的 HTTP Server

首先，为了便于测试，我们用 Python 内建的 `http` 模块，运行一个简单的 HTTP Server。

新建一个目录，添加文件 `index.html`，内容为 `Hello, World!`（不是合法的 HTML 格式也没有关系），然后运行如下命令（Ubuntu 请用 `python3`）：
```bash
$ python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

后面不同的 Client 实现，都会连接这个 Server：Host 为 `localhost`，Port 为 `8000`。

所有的示例代码，`import` 语句一律从略。
```python
import asyncio
```

## 第一版

第一版改写自 Python 官方文档里的 [例子](https://docs.python.org/3.6/library/asyncio-protocol.html#tcp-echo-client-protocol)。
Python 的例子是 Echo Client，我们稍微复杂一点，是 HTTP Client，都是 TCP。
```python
class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        request = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'
        transport.write(request.encode())

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        self.loop.stop()

async def main(loop):
    await loop.create_connection(
        lambda: ClientProtocol(loop), 'localhost', 8000)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.run_forever()
```

TCP 连接由 `loop.create_connection()` 创建，后者需要一个 Protocol 工厂，即 `lambda: ClientProtocol(loop)`。
Protocol 提供了 `connection_made()`，`data_received()`， `connection_lost()` 等接口，这些接口就像回调函数一样，会在恰当的时候被调用。
我们在 `connection_made()` 中，通过参数 `transport` 发送一个 HTTP GET 请求，随后在 `data_received()` 里，将收到 HTTP 应答。
当 `connection_lost()` 被调用时，表示 Server 已经断开连接。

运行结果：
```http
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.6.3
Date: Mon, 04 Dec 2017 06:11:52 GMT
Content-type: text/html
Content-Length: 13
Last-Modified: Thu, 30 Nov 2017 05:37:31 GMT


Hello, World!
```
这就是一个标准的 HTTP 应答，包含 Status Line，Headers 和 Body。

值得注意的是，loop 其实运行了两遍：
```python
loop.run_until_complete(main(loop))  # 第一遍
loop.run_forever()  # 第二遍
```
如果没有 `run_forever()`，在收到数据之前，loop 可能就结束了。协程 `main()` 只是创建好连接，随后 `run_until_complete()` 自然也就无事可做而终。

加了  `run_forever()` 后，`data_received()` 等便有了被调用的机会。但是也有问题，loop 一直在跑，程序没办法结束，所以才在 `connection_lost()` 里主动停止 loop：
```python
    def connection_lost(self, exc):
        self.loop.stop()
```

## 第二版：ClientSession

第一版在 `connection_made()` 中 hard code 了一个 HTTP GET 请求，灵活性较差，以后必然还有 POST 等其他 HTTP 方法需要支持，所以有必要新增一个 `ClientSession` 类，来抽象客户端的会话。于是，HTTP 请求的发送，便从 `connection_made()` 挪到了 `ClientSession.get()`。

`ClientSession` 应该为每一个 HTTP 方法提供一个相应的方法，比如 `post`，`put` 等等，虽然我们只考虑  HTTP GET。

```python
class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        self.loop.stop()

class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    async def get(self, url, host, port):
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop), host, port)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)
        transport.write(request.encode())
```

首先，`ClientProtocol` 新增了一个属性 `transport`，是在 `connection_made()` 时保存下来的，这样在 `ClientSession` 里才能通过它来发送请求。

## 第三版：去掉 `run_forever()`

第三版的目的是：去掉 `run_forever()` 。

```python
class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self._eof = False  # 有没有收到 EOF
        self._waiter = None  # 用来等待接收数据的 future

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

    def eof_received(self):
        self._eof = True
        self._wakeup_waiter()

    def connection_lost(self, exc):
        pass  # 不再调用 self.loop.stop()

    async def wait_for_data(self):
        assert not self._eof
        assert not self._waiter

        self._waiter = self.loop.create_future()
        await self._waiter
        self._waiter = None

    def _wakeup_waiter(self):
        waiter = self._waiter
        if waiter:
            self._waiter = None
            waiter.set_result(None)

class ClientSession:
    def __init__(self, loop):
        self._loop = loop

    async def get(self, url, host, port):
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop), host, port)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)
        transport.write(request.encode())

        # 等待接收数据。
        await protocol.wait_for_data()
```

协程 `main()` 保持不变，但是 `loop.run_forever()` 已被剔除：
```python
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
# 不再需要 loop.run_forever()
```

HTTP 请求发送之后，继续异步等待（await）数据的接收，即 `protocol.wait_for_data()`。
这个等待动作，是通过往 loop 里新增一个  future 来实现的：
```python
    async def wait_for_data(self):
        # ...
        self._waiter = self.loop.create_future()
        await self._waiter
        self._waiter = None
```
`self._waiter` 就是这个导致等待的 future，它会保证 loop 一直运行，直到数据接收完毕。
`eof_received()` 被调用时，数据就接收完毕了（EOF 的意思不用多说了吧？）。
```python
    def eof_received(self):
        self._eof = True
        self._wakeup_waiter()
```
`_wakeup_waiter()` 的作用是结束那个导致等待的 future，这样 loop 也就可以结束了：
```python
    def _wakeup_waiter(self):
        waiter = self._waiter
        if waiter:
            self._waiter = None
            # 结束 waiter future，以便 loop 结束。
            waiter.set_result(None)
```

## 第四版：Reader

在 `data_received()` 里直接输出 HTTP 的应答结果，实在算不上什么完美的做法。
```python
    def data_received(self, data):
        print(data.decode())
```

为了解决这一问题，我们引入一个 `Reader` 类，用来缓存收到的数据，并提供「读」的接口给用户。

首先，Protocol 被简化了，前一版引入的各种处理，都转交给了 Reader。
```python
class ClientProtocol(asyncio.Protocol):
    def __init__(self, loop, reader):
        self.loop = loop
        self.transport = None
        self._reader = reader

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self._reader.feed(data)  # 转交给 Reader

    def eof_received(self):
        self._reader.feed_eof()  # 转交给 Reader

    def connection_lost(self, exc):
        pass
```

下面是 `ClientSession.get()` 基于 `Reader` 的实现：
```python
class ClientSession:
    async def get(self, url, host, port):
        reader = Reader(self._loop)
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop, reader), host, port)
        # 发送请求，代码从略...
        data = await reader.read()
        print(data.decode())
```

`Reader` 本身是从上一版的 Protocol 抽取出来的，唯一不同的是，接收的数据被临时放在了一个 `bytearray` 缓存里。
```python
class Reader:
    def __init__(self, loop):
        self._loop = loop
        self._buffer = bytearray()  # 缓存
        self._eof = False
        self._waiter = None

    def feed(self, data):
        self._buffer.extend(data)
        self._wakeup_waiter()

    def feed_eof(self):
        self._eof = True
        self._wakeup_waiter()

    async def read(self):
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
```

稍微解释一下 `read()`，比较重要的是开始的一句判断：
```python
        # 如果缓存为空，并且 EOF 还没收到，那就（继续）等待接收数据。
        if not self._buffer and not self._eof:
            # read() 会停在这个地方，直到 feed() 或 feed_eof() 被调用，
            # 也就是说有数据可读了。
            await self._wait_for_data()
```
接下来就是把缓存倒空：
```python
        data = bytes(self._buffer)
        del self._buffer[:]
```

运行一下，不难发现，`ClientSession.get()` 里读数据的那一句是有问题的。
```python
        data = await reader.read()
```
收到的 `data` 并不是完整的 HTTP 应答，可能只包含了 HTTP 的 Headers，而没有 Body。

一个 HTTP 应答，Server 端可能分多次发送过来。比如这个测试用的 Hello World Server，Headers 和 Body 就分了两次发送，也就是说 `data_received()` 会被调用两次。

之前我们在 `eof_received()` 里才唤醒 waiter（`_wakeup_waiter()`），现在在 `data_received()` 里就唤醒了，于是第一次数据收完， waiter 就结束了，loop 也便跟着结束。

为了读到完整的 HTTP 应答，方法也很简单，把 `read()` 放在循环里：
```python
        blocks = []
        while True:
            block = await reader.read()
            if not block:
                break
            blocks.append(block)
        data = b''.join(blocks)
        print(data.decode())
```
每一次 `read()`，如果缓存为空，并且 EOF 还没收到的话，就会再次创建 waiter，放到 loop 里，继续等待接收数据。

这个循环显然应该交给 `Reader` 处理，对 `ClientSession` 需保持透明。
```python
class Reader:
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
        if not self._buffer and not self._eof:
            await self._wait_for_data()
            
        data = bytes(self._buffer)
        del self._buffer[:]
        return data
```
最后，原来的 `read()` 重命名为 `_read()`，新的 `read()` 在循环中反复调用 `_read()`，直到无数据可读。`ClientSession` 这边直接调用新的 `read()` 即可。

## 第五版：Writer

到目前为止，发送 HTTP 请求时，都是直接调用较为底层的 `transport.write()`：
```python
    async def get(self, url, host, port):
        # ...
        transport.write(request.encode())
```

可以把它封装在 `Writer` 中，与 `Reader` 的做法类似，但是 `Writer` 要简单得多：
```python
class Writer:
    def __init__(self, transport):
        self._transport = transport

    def write(self, data):
        self._transport.write(data)
```

然后在 `ClientSession.get()` 中创建 `Writer`：
```python
    async def get(self, url, host, port):
        reader = Reader(self._loop)
        transport, protocol = await self._loop.create_connection(
            lambda: ClientProtocol(loop, reader), host, port)

        writer = Writer(transport)
        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)
        writer.write(request.encode())
        # ...
```

对 `ClientSession` 来说，只需知道 `Reader` 和 `Writer` 就足够了，所以不妨提供一个函数 `open_connection()`，直接返回 `Reader` 和 `Writer`。
```python
async def open_connection(host, port, loop):
    reader = Reader(loop)
    protocol = ClientProtocol(loop, reader)
    transport, _ = await loop.create_connection(lambda: protocol, host, port)
    writer = Writer(transport)
    return reader, writer
```

然后 `ClientSession` 就可以简化成这样：
```python
class ClientSession:
    async def get(self, url, host, port):
        reader, writer = await open_connection(host, port, self._loop)
		# ...
```

## 第六版：Asyncio Streams

其实 Asyncio 已经提供了 Reader 和 Writer，详见 [官方文档](https://docs.python.org/3.6/library/asyncio-stream.html)。

下面以 Asyncio Streams 实现 `ClientSession.get()`：
```python
class ClientSession:
    async def get(self, url, host, port):
        reader, writer = await asyncio.open_connection(
            host, port, loop=self._loop)

        request = 'GET {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(url, host)
        writer.write(request.encode())

        data = await reader.read(-1)
        print(data.decode())
        writer.close()
```

`asyncio.open_connection()` 就相当于我们的 `open_connection()`。`Reader` 和 `Writer` 也都类似，只是复杂了一些。


**全文完**