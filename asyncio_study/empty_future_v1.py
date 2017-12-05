import asyncio

# Run an empty future in the loop.
# The loop will never end.

loop = asyncio.get_event_loop()

empty_future = loop.create_future()
loop.run_until_complete(empty_future)
