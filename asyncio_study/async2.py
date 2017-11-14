import asyncio
import functools

async def do_some_work(loop, x):
    print('Waiting ' + str(x))
    await asyncio.sleep(x)
    print('Done')

async def timer(x, cb):
    futu = asyncio.ensure_future(asyncio.sleep(x))
    futu.add_done_callback(cb)
    await futu

loop = asyncio.get_event_loop()

t = timer(3, lambda futu: print('Done'))
loop.run_until_complete(t)

loop.close()

#  callback = lambda: asyncio.ensure_future(coro)
#  loop.call_soon(callback)


