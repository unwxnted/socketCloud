import os
import asyncio
import json
from websockets.sync.client import connect

class Client:
    def __init__(self):
        self.websocket = None

    def connect_to_server(self):
        self.websocket = connect("ws://localhost:8765")

    def send_command(self, command):
        if self.websocket is not None:
            self.websocket.send(command)
            response = self.websocket.recv()
            return response if response else ""
        else:
            print("Error, no websocket connection")

    def write_command(self, response, command):
        params = command.split()
        temp = open("temp_" + params[1], "w")
        temp.write(response)
        temp.close()
        os.system("nano " + temp.name)
    
    def commit_command(self, command):
        params = command.split()
        file = open("temp_"+ params[1], "r")
        content = file.read()
        file.close()
        os.remove("temp_"+ params[1])
        data = {"command": "commit", "filename": params[1],"data": content}
        data_str = json.dumps(data)
        return self.send_command(data_str)

    def help_command(self):
        print("add - adds a new empty file to the server\n    example: add [filename]\n\nread - retrieves a given file from the server and prints it to the terminal\n    example: read [filename]\n\nwrite - retrieves a given file from the server and open nano to write changes on the file\n    example: write [filename]\n\ncommit - push the changes from the write command to the server\n    example: commit [filename]\n")

    def close_connection(self):
        if self.websocket is not None:
            self.websocket.close()

    def run(self):
        self.connect_to_server()
        while True:
            command = input("[cmd]: ")
            if "commit" in command: print(self.commit_command(command))
            if "read" in command: print(self.send_command(command)) 
            if "add" in command: print(self.send_command(command))
            if "write" in command: self.write_command(self.send_command(command), command)
            if "help" in command: self.help_command()
                
        self.close_connection()

if __name__ == "__main__":
    cli = Client()
    cli.run()
