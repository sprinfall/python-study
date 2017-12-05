import asyncio

# Mark an empty future done in another coroutine.

async def mark_future_done(futu):
    await asyncio.sleep(3)
    # Mark the future done and set its result.
    futu.set_result(None)

loop = asyncio.get_event_loop()

futu = loop.create_future()
loop.run_until_complete(asyncio.gather(futu, mark_future_done(futu)))
