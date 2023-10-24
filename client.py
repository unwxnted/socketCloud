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
            if(params[0] != "add" and params[0] != "ls"): self.last_update[params[1]] = response
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

    def readc_command(self, command):
        filename = command.split()
        filename = "temp_" + filename[1]
        with open(filename, "r") as archivo:
            return archivo.read()

    def help_command(self, comment):
        print(comment + "\nadd - adds a new empty file to the server\n    example: add [filename]\n\nread - retrieves a given file from the server and prints it to the terminal\n    example: read [filename]\n\nwrite - retrieves a given file from the server and open nano to write changes on the file\n    example: write [filename]\n\ncommit - push the changes from the write command to the server\n    example: commit [filename]\n\nls - list existing server files\n    example: ls [filename]\n\nexit - finish the client process\n    example: exit\n\nreadc - prints a given file's temporary file\n    example: readc [filename]\n")

    def checker(self, command): 
        params = command.split()
        if len(params) > 2 or (len(params)==1 and (params[0] != "help") and (params[0] != "exit") and (params[0] != "ls")): # add command check here
            self.help_command("Command syntax not valid, check the commands below: ")
            return False
        commands = ["read", "add", "commit", "write", "help", "exit", "ls", "readc"] # add the command in the list
        for cmd in commands:
            if cmd == params[0]:
                return True
        self.help_command("Command not found. Please check the commands below: ")
        return False

    def close_connection(self):
        if self.websocket is not None:
            self.websocket.close()
  
    def run(self):
        self.connect_to_server()
        while True:
            try:
                command = input("[cmd]: ")
            except KeyboardInterrupt: 
                print("\nExiting...")
                break
                
            if not self.checker(command): continue 
            # add the command below
            if "commit" in command: print(self.commit_command(command))
            if "readc" in command: print(self.readc_command(command))
            else: 
                if "read" in command: print(self.send_command(command))
            if "add" in command: print(self.send_command(command))
            if "write" in command: self.write_command(self.send_command(command), command)
            if "ls" in command: print(self.send_command(command))
            if "help" in command: self.help_command("")
            if "exit" in command: break 
                
        self.close_connection()

if __name__ == "__main__":
    cli = Client()
    cli.run()
