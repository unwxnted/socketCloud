import asyncio
import json
import os
from websockets.server import serve

class Server:
    def __init__(self):
        self.address = "localhost"
        self.port = 8765

    async def read_command(self, command):
        try:
            params = command.split()
            if(not os.path.exists("./server_files/"+params[1]) or "../" in params[1]): return "File not found"
            with open("./server_files/"+params[1], "r") as archivo:
                return archivo.read()
        except:
            return "Error, cannot read/write to a folder"

    async def add_command(self, command):
        try:
            filename = command.split()
            filename = filename[1]
            with open("./server_files/"+filename, 'w') as file:
                file.write("")
            return "Successfully added new file"
        except:
            return "Error, cannot add a file with the same folder name"
    
    async def list_command(self, command):
        directory = ".\\server_files"
        response = ""
        stack = []

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                stack.append(item)
            else:
                response += f"File: {item}\n"

        while stack:
            item = stack.pop()
            response += f"Folder: {item}\n"
            folder_path = os.path.join(directory, item)
            for file_item in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_item)
                if os.path.isdir(file_path):
                    stack.append(os.path.join(item, file_item))
                else:
                    response += f"  File: {file_item}\n"
        return response
    
    async def mkdir_command(self, command):
        filename = command.split()
        filename = filename[1]
        os.makedirs("server_files/"+filename)
        return "Succesfully created new directory"

    async def commit_command(self, command):
        json_data = json.loads(command)
        file = open("./server_files/"+json_data["filename"], "w")
        file.write(json_data["data"])
        file.close()
        return "Successfully committed"

    async def serve_command(self, command):
        if ("read" in command) or ("write" in command):
            return await self.read_command(command)
        if("commit" in command): return await self.commit_command(command)
        if("ls" in command): return await self.list_command(command)
        if("add" in command): return await self.add_command(command)
        if("mkdir" in command): return await self.mkdir_command(command)

    async def echo(self, websocket, path):
        async for command in websocket:
            response = await self.serve_command(command)
            await websocket.send(response)

    def run(self):
        os.path.exists("./server_files") or os.mkdir("./server_files")
        async def server_loop():
            async with serve(self.echo, self.address, self.port):
                await asyncio.Future()

        asyncio.run(server_loop())

if __name__ == "__main__":
    sv = Server()
    sv.run()
