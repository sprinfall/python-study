import time
import asyncio
from threading import Thread

# Run a loop in a different thread.

async def do_some_work(x):
    print("Waiting %s" % x)
    # Wait on the results of external workload (simulated through
    # asyncio.sleep.
    await asyncio.sleep(x)
    print("Finished work %s" % x)

def more_work(x):
    print("More work %s" % x)
    time.sleep(x)
    print("Finished more work %s" % x)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

new_loop = asyncio.new_event_loop()

# Spawn a new thread, pass it the new loop.
t = Thread(target=start_loop, args=(new_loop,))
t.start()

# The call to more_work blocks for 3 seconds.
new_loop.call_soon_threadsafe(more_work, 3)

# The calls to do_some_work execute in parallel immediately after more_work
# finishes.
asyncio.run_coroutine_threadsafe(do_some_work(3), new_loop)
asyncio.run_coroutine_threadsafe(do_some_work(5), new_loop)

