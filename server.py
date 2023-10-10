import asyncio
from websockets.server import serve

async def read_command(command):
    params = command.split()
    with open(params[1], "r") as archivo:
        return archivo.read()

async def serve_command(command):
    if "read" in command: return await read_command(command)

async def echo(websocket):
    async for command in websocket:
        response = await serve_command(command)
        await websocket.send(response)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())