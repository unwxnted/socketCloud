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
            return response if response else False
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
        data = {"command": "commit", "filename": params[1],"data": content}
        data_str = json.dumps(data)
        return self.send_command(data_str)

    def close_connection(self):
        if self.websocket is not None:
            self.websocket.close()

    def run(self):
        self.connect_to_server()
        while True:
            command = input("[cmd]: ")
            if "commit" in command:
                response = self.commit_command(command)
                print(response)
            if "read" in command:
                response = self.send_command(command)
                print(response)
            if "write" in command:
                response = self.send_command(command)
                self.write_command(response, command)
                
        self.close_connection()

if __name__ == "__main__":
    cli = Client()
    cli.run()
