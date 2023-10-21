import socket
import asyncio
import os
import threading

HOST = "localhost"
PORT_BLOCK = 50006
PORT_NON_BLOCK = 50007
PORT_ASYNC = 50008
PORT_UNIX = 50009
UNIX_SOCKET_PATH = "unix_socket.sock"
BUFFER = 4096

testdata = b'x' * BUFFER * 4


# Original blocking socket server
def original_blocking_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT_BLOCK))
        server_sock.listen(1)
        print("Original blocking socket server is listening on", (HOST, PORT_BLOCK))
        conn, addr = server_sock.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(BUFFER)
                if not data:
                    break
                conn.sendall(data)


# Non-blocking socket server
def non_blocking_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setblocking(False)
        server_sock.bind((HOST, PORT_NON_BLOCK))
        server_sock.listen(1)
        print("Non-blocking socket server is listening on", (HOST, PORT_NON_BLOCK))
        try:
            conn, addr = server_sock.accept()
            conn.setblocking(False)
            print("Connected by", addr)
        except BlockingIOError:
            pass

        while True:
            try:
                data = conn.recv(BUFFER)
                if not data:
                    break
                conn.send(data)
            except BlockingIOError:
                pass


async def asynchronous_socket_server(reader, writer):
    print("Asynchronous socket server connected")
    while True:
        data = await reader.read(BUFFER)
        if not data:
            break
        writer.write(data)
        await writer.drain()


def unix_domain_socket_server():
    if os.path.exists(UNIX_SOCKET_PATH):
        os.remove(UNIX_SOCKET_PATH)

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(UNIX_SOCKET_PATH)
        server_sock.listen(1)
        print("Unix domain socket server is listening on", UNIX_SOCKET_PATH)
        conn, addr = server_sock.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(BUFFER)
                if not data:
                    break
                conn.sendall(data)


if __name__ == "__main__":
    original_thread = threading.Thread(target=original_blocking_socket_server)
    non_blocking_thread = threading.Thread(target=non_blocking_socket_server)
    async_server = asyncio.start_server(asynchronous_socket_server, HOST, PORT_ASYNC)
    unix_thread = threading.Thread(target=unix_domain_socket_server)

    original_thread.start()
    non_blocking_thread.start()
    asyncio.get_event_loop().run_until_complete(async_server)
    unix_thread.start()

    original_thread.join()
    non_blocking_thread.join()
    asyncio.get_event_loop().close()
    unix_thread.join()

    # Clean up the Unix domain socket file
    os.remove(UNIX_SOCKET_PATH)
