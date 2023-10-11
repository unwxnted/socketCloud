import os
import asyncio
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

    def write_command_to_editor(self, response):
        temp = open("temp", "w")
        temp.write(response)
        temp.close()
        os.system("nano " + temp.name)

    def close_connection(self):
        if self.websocket is not None:
            self.websocket.close()

    def run(self):
        self.connect_to_server()
        while True:
            command = input("[cmd]: ")
            response = self.send_command(command)
            if "read" in command and response:
                print(response)
            if "write" in command and response:
                self.write_command_to_editor(response)
                
        self.close_connection()

if __name__ == "__main__":
    cli = Client()
    cli.run()
