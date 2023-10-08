#!/usr/bin/python

import shared

import socket
import threading

CLI_LEAVE = "$leave"

class Client:
    _alive = False
    _socket = None
    _nickname = ""
    _recv_thread = None
    _send_thread = None

    def __init__(self):
        s = self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(shared.SERVER_ADDRESS)

        self._recv_thread = threading.Thread(target=self._recv, args=())
        self._send_thread = threading.Thread(target=self._send, args=())

    def start(self):
        self._alive = True
        self._recv_thread.start()
        self._send_thread.start()

    def _recv(self):
        while 1:
            try:
                data = self._socket.recv(shared.BUFSIZE)
                if not self._alive:
                    break

                if not data:
                    continue

                message = data.decode()
                if message == shared.SIGNAL_NICKNAME:
                    if not self._nickname:
                        self._nickname = input("Choose your nickname: ")
                    self._socket.sendall(self._nickname.encode())
                elif message == shared.SIGNAL_WELCOME:
                    print("Welcome to the chat!")
                elif message == shared.SIGNAL_STOP:
                    self.stop()
                    break
                else:
                    print(message)
            except:
                if not self._alive:
                    return

                self._log(f"Error")
                self.stop()
                break

    def _send(self):
        while 1:
            if not self._nickname or not self._alive:
                continue

            try:
                message = input('')
                if not self._alive:
                    return

                if message == CLI_LEAVE:
                    self.stop()
                    break

                self._socket.sendall(message.encode())
            except:
                if not self._alive:
                    return

                self._log(f"Error")
                self.stop()
                break

    def stop(self):
        if not self._alive:
            return

        self._alive = False
        try:
            self._socket.sendall(shared.B_SIGNAL_STOP)
            self._socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self._socket.close()
        self._log(f"Disconnected from server")

    def _log(self, message):
        print("[CLIENT]", message)


if __name__ == "__main__":
    client = Client()
    client.start()
