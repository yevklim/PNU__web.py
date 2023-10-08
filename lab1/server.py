#!/usr/bin/python

import shared

import socket
import selectors

from time import time
from collections import deque
from datetime import datetime
from types import SimpleNamespace

def main():
    selector = selectors.DefaultSelector()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(shared.SERVER_ADDRESS)
    s.listen(10)
    print("[SERVER] Socket created")

    s.setblocking(False)

    selector.register(s, selectors.EVENT_READ)

    try:
        while 1:
            events = selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_connection(_socket=key.fileobj, selector=selector)
                else:
                    serve_connection(connection=key.fileobj, data=key.data, bitmask=mask, selector=selector)
    except KeyboardInterrupt:
        pass
    finally:
        selector.close()
        s.close()
        print("[SERVER] Socket closed")

def accept_connection(_socket, selector):
    connection, client_address = _socket.accept()
    print(f"[SERVER] Connected with client {client_address}")
    connection.setblocking(False)

    data = SimpleNamespace(client_address=client_address, inb=b"", out=deque())
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(connection, events, data=data)

def serve_connection(connection, data, bitmask, selector):
    if bitmask & selectors.EVENT_READ:
        recv_data = connection.recv(shared.BUFSIZE)
        timestamp = datetime.now()

        if not recv_data or recv_data == shared.MSG_CLOSE_CON:
            print(f"[SERVER] Disconnected from client {data.client_address}")
            selector.unregister(connection)
            connection.close()
            return

        print(f"[SERVER] Received message from {data.client_address}:\n\t{timestamp}\n\t{recv_data}\n")

        if recv_data:
            send_time = time() + 5
            data.out.append((recv_data, send_time))
    if bitmask & selectors.EVENT_WRITE:
        if len(data.out):
            send_data, send_time = data.out[0]
            send_len = -1
            sent_bytes = 0
            if send_time <= time():
                send_len = len(send_data)
                print(f"[SERVER] Sending {send_data} to {data.client_address}")
                sent_bytes = connection.send(send_data)
            if sent_bytes:
                if sent_bytes < send_len:
                    send_data = send_data[sent_bytes:]
                else:
                    data.out.popleft()


if __name__ == "__main__":
    main()
