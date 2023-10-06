#!/usr/bin/python

import shared

import socket

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(shared.SERVER_ADDRESS)
        print(f"[CLIENT] Connected with server")

        while 1:
            msg = input("[CLIENT] Provide a message: ")
            msg = msg[:shared.BUFSIZE]

            print(f"[CLIENT] Sending message to the server...")
            s.sendall(msg.encode())

            print(f"[CLIENT] Waiting for response from the server...")
            data = s.recv(shared.BUFSIZE)
            if not data:
                break
            print(f"[CLIENT] Received: {data}")


if __name__ == "__main__":
    main()
