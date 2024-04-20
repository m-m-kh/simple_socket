import asyncio
from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol


async def echo(websocket: WebSocketServerProtocol):
    async def sender(websocket: WebSocketServerProtocol):
        while True:
            r = await asyncio.to_thread(input,'::>>')
            await websocket.send(r)
    async def reciver(websocket: WebSocketServerProtocol):
        while True:
            print('here')
            print(await websocket.recv())

    await asyncio.gather(sender(websocket))


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())