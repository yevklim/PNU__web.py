#!/usr/bin/python

import shared

import socket
from datetime import datetime

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(shared.SERVER_ADDRESS)
        print(f"[CLIENT] Connected with server")

        while 1:
            msg = input("[CLIENT] Provide a message: ")
            msg = msg[:shared.BUFSIZE]
            if not msg:
                continue

            print(f"[CLIENT] Sending message to the server...")
            s.sendall(msg.encode())

            print(f"[CLIENT] Waiting for response from the server...")
            data = s.recv(shared.BUFSIZE)
            if not data:
                break
            timestamp = datetime.now()
            print(f"[CLIENT] Received:\n\t{timestamp}\n\t{data}\n")


if __name__ == "__main__":
    main()
