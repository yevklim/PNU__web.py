#!/usr/bin/python

import shared

import socket

def main():
    with socket.socket() as s:
        s.connect(shared.SERVER_ADDRESS)
        print(f"[CLIENT] Connected with server")

        msg = input("[CLIENT] Provide a message: ")

        print(f"[CLIENT] Sending message to the server...")
        s.sendall(msg.encode())

if __name__ == "__main__":
    main()
