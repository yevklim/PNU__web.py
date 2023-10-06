#!/usr/bin/python

import shared

import socket
import datetime
import time

def main():
    with socket.socket() as s:
        print("[SERVER] Socket created")
        s.bind(shared.SERVER_ADDRESS)
        s.listen(10)
        print("[SERVER] Socket starts listening")

        while 1:
            connection, client_address = s.accept()
            with connection:
                print(f"[SERVER] Connected with client {client_address}")
                while 1:
                    data = connection.recv(shared.BUFSIZE)
                    if not data or data == shared.MSG_CLOSE_CON:
                        break
                    timestamp = datetime.datetime.now()
                    print(f"[SERVER] Received message from the client {client_address}:\n\t{timestamp}\n\t{data}\n")

                    time.sleep(5)

                    # Змініть код так, щоб сервер відповідав ... із ... перевіркою (використати розмір даних),
                    # що всі дані успішно відправлено. І далі закривав з’єднання з клієнтом.
                    data_len = len(data)
                    sent = 0
                    while sent < data_len:
                        sent += connection.send(data[sent:sent+shared.BUFSIZE])
                connection.shutdown(socket.SHUT_RD)
                print(f"[SERVER] Disconnected from client {client_address}")

if __name__ == "__main__":
    main()
