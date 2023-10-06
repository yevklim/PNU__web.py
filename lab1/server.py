#!/usr/bin/python

import shared

import socket
import datetime

def main():
    with socket.socket() as s:
        print("[SERVER] Socket created")
        s.bind(shared.SERVER_ADDRESS)
        s.listen()
        print("[SERVER] Socket starts listening")

        while 1:
            connection, client_address = s.accept()
            with connection:
                print(f"[SERVER] Connected with client {client_address}")
                while 1:
                    data = connection.recv(1024)
                    if not data:
                        break
                    timestamp = datetime.datetime.now()
                    print(f"[SERVER] Received message from the client:\n\t{timestamp}\n\t{data}\n")

if __name__ == "__main__":
    main()
