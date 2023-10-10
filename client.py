import asyncio
from websockets.sync.client import connect


def send_command(command):
    with connect("ws://localhost:8765") as websocket:
        websocket.send(command)
        response = websocket.recv()
        if(response): return response
        else: return False

def main():
    while(True):
        command = input("[cmd]: ")
        response = send_command(command)
        print(response)

main()