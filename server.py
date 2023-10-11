import asyncio
from websockets.server import serve

class Server:
    def __init__(self):
        self.address = "localhost"
        self.port = 8765

    async def read_command(self, command):
        params = command.split()
        with open(params[1], "r") as archivo:
            return archivo.read()

    async def serve_command(self, command):
        if ("read" in command) or ("write" in command):
            return await self.read_command(command)

    async def echo(self, websocket, path):
        async for command in websocket:
            response = await self.serve_command(command)
            await websocket.send(response)

    def run(self):
        async def server_loop():
            async with serve(self.echo, self.address, self.port):
                await asyncio.Future()

        asyncio.run(server_loop())

if __name__ == "__main__":
    sv = Server()
    sv.run()
