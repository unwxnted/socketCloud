import os
import asyncio
import json
from websockets.sync.client import connect

class Client:
    def __init__(self):
        self.websocket = None
        self.last_update = {}

    def connect_to_server(self):
        self.websocket = connect("ws://localhost:8765")

    def send_command(self, command):
        if self.websocket is not None:
            self.websocket.send(command)
            response = self.websocket.recv()
            params = command.split()
            if(params[0] != "add"): self.last_update[params[1]] = response
            return response if response else ""
        else:
            print("Error, no websocket connection")

    def write_command(self, response, command):
        if(response == "File not found"): return print("File not found") 
        params = command.split()
        self.last_update[params[1]] = response
        temp = open("temp_" + params[1], "w")
        temp.write(response)
        temp.close()
        os.system("nano " + temp.name)
    
    def commit_command(self, command):
        params = command.split()
        if(not os.path.exists("temp_" + params[1])): return "No changes maded to commit"
        file = open("temp_"+ params[1], "r")
        content = file.read()
        file.close()
        os.remove("temp_"+ params[1])
        data = {"command": "commit", "filename": params[1],"data": content}
        data_str = json.dumps(data)
        if(self.last_update[params[1]] != self.send_command("read "+ params[1])):
            return "Some changes were made during the file modification, the server file is not the same, please get the new file and try again."
        return self.send_command(data_str)

    def help_command(self, comment):
        print(comment + "\nadd - adds a new empty file to the server\n    example: add [filename]\n\nread - retrieves a given file from the server and prints it to the terminal\n    example: read [filename]\n\nwrite - retrieves a given file from the server and open nano to write changes on the file\n    example: write [filename]\n\ncommit - push the changes from the write command to the server\n    example: commit [filename]\n")

    def close_connection(self):
        if self.websocket is not None:
            self.websocket.close()

    def run(self):
        self.connect_to_server()
        while True:
            command = input("[cmd]: ")
            if "commit" in command: print(self.commit_command(command))
            elif "read" in command: print(self.send_command(command)) 
            elif "add" in command: print(self.send_command(command))
            elif "write" in command: self.write_command(self.send_command(command), command)
            elif "help" in command: self.help_command("")
            elif "exit" in command: break
            else: self.help_command("Command no found. Please check the commands below: ")
                
        self.close_connection()

if __name__ == "__main__":
    cli = Client()
    cli.run()
