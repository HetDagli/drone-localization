import asyncio
import websockets
import time
async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        greeting = await websocket.recv()
        print(greeting)
tm=time.time()
for i in range(1000):
    asyncio.get_event_loop().run_until_complete(hello())
print(time.time()-tm)
