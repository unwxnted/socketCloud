import asyncio
from websockets.sync.client import connect


def send_command(command):
    with connect("ws://localhost:8765") as websocket:
        websocket.send(command)
        message = websocket.recv()
        if(message): return True
        else: return False

command = input("[cmd]: ")
send_command(command)