#!/usr/bin/python

import shared

import socket
import threading

from types import SimpleNamespace

CLI_STOP = "STOP"

class Server:
    _alive = False
    _socket = None
    _thread = None
    _clients = dict()

    def __init__(self):
        s = self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(shared.SERVER_ADDRESS)
        s.listen(10)

    def start(self):
        self._alive = True
        self._thread = threading.Thread(target=self._accept_connections, args=())
        self._thread.start()
        self._cli_start()

    def _accept_connections(self):
        while 1:
            if not self._alive:
                return

            try:
                connection, address = self._socket.accept()
            except:
                continue

            client = SimpleNamespace(connection=connection, address=address, nickname="")

            self._log(f"Connected with {address}")

            thread = threading.Thread(target=self._authorize_connection, args=(client,))
            thread.start()

    def _authorize_connection(self, client):
        if not self._alive:
            return

        client.connection.sendall("NICK".encode())
        while 1:
            if not self._alive:
                return

            data = client.connection.recv(shared.BUFSIZE)
            if not data:
                self._disconnect_client(client)
                self._log(f"Disconnected from {client.address}")
                return
            client.nickname = data.decode()
            break

        self._clients[client.connection] = client

        self._log(f"{client.address} is {client.nickname}")
        client.connection.sendall(shared.B_SIGNAL_WELCOME)
        self.broadcast(f"{client.nickname} joined the chat".encode())

        self._service_connection(client)

    def _service_connection(self, client):
        while 1:
            try:
                data = client.connection.recv(shared.BUFSIZE)
                if not data:
                    break

                if data == shared.B_SIGNAL_NICKNAME:
                    continue

                if data == shared.B_SIGNAL_STOP:
                    break

                self.broadcast(f"{client.nickname}: ".encode() + data)
            except:
                break

        self._disconnect_client(client)
        self._log(f"Disconnected from {client.address}")
        if self._alive:
            self._clients.pop(client.connection, None)
        self.broadcast(f"{client.nickname} left the chat".encode())

    def broadcast(self, message):
        if not self._alive:
            return

        for connection in self._clients:
            try:
                connection.send(message)
            except:
                pass

    def stop(self):
        if not self._alive:
            return

        self._alive = False
        self._close_connections()
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self._socket.close()

    def _close_connections(self):
        for client in self._clients.values():
            self._disconnect_client(client)
        self._clients.clear()

    def _disconnect_client(self, client):
        try:
            client.connection.sendall(shared.B_SIGNAL_STOP)
            client.connection.shutdown(socket.SHUT_RDWR)
        except:
            pass
        client.connection.close()

    def _cli_start(self):
        while 1:
            cmd = input("")
            if cmd == CLI_STOP:
                self.stop()
                break

    def _log(self, message):
        print("[SERVER]", message)


if __name__ == "__main__":
    server = Server()
    server.start()
