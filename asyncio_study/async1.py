import asyncio

async def do_some_work(x):
    print("Waiting " + str(x))
    await asyncio.sleep(x)

def done_callback(future):
    print("Done")

loop = asyncio.get_event_loop()

#  futu = asyncio.ensure_future(do_some_work(3))
#  futu.add_done_callback(done_callback)

loop.call_later(1, do_some_work, 1)

loop.run_forever()

#  try:
    #  loop.stop()
#  finally:
    #  loop.close()

