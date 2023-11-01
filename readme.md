# SocketCloud
## Description
SocketCloud is a server-client program where the server provides the clients with files and folders, and where the client can store/modify its own files

We use WebSockets tech:
It is a bidirectional client-server communication protocol, the transmitted data needs to be protected with SSL/TLS encryption.

## How to Use

- add - adds a new empty file to the server                                   
example: add [file name]

- mkdir - adds a new empty folder into the server
example: mkdir [folder name]

- read - retrieves a given file from the server and prints it to the terminal 
example: read [file name]

- readc - retrieves a given file from the client and prints it to the terminal 

- write - it executes the nano command once the file is opened in the terminal
example: write [file name]

- commit - stores local temp file in the server                               
example: commit [file name]

- ls - list all the files and folders in the server
example: ls

- help - show all the commands descriptions
example: help

- exit - finish the client execution
example: exit
## Technologies used (Modules)

### Asyncio 

It is a library for writing concurrent code using async/await syntax, provides high-performance networking and web servers, database connection libraries, distributed task queues, etc. 

### Websockets

It is a library for creating WebSocket servers and clients in Python, focusing on correctness, simplicity, robustness and performance. 

## How to install
First of all intall python 3.12.0 forward, then clone the repository and run the following command to install all the dependencies:
```
# pip install -r dependencies
```
## How to run

### Server
```
# python server.py
```

### Client
```
# python client.py
```

## Credits
- Sanchez Pastor Bautista - @unwxnted
- Mendez Pricila - @mendezprisci
- Marcozzi Lucio - @Gvmbler
- Oteiza Santiago - @l0l0C1337
- Buera Jazmin