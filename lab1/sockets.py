import asyncio
import os
import socket
import time

HOST = "localhost"
PORT = 50007
UNIX_SOCKET_PATH = "unix_socket.sock"
BUFFER = 4096
testdata = b'x' * BUFFER * 4


def original_blocking_socket_speed():
    start_time = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        for _ in range(1000):
            sock.sendall(testdata)
            received_data = b''
            while True:
                data = sock.recv(BUFFER)
                if not data:
                    break
                received_data += data
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def non_blocking_socket_speed():
    start_time = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setblocking(False)
        try:
            sock.connect((HOST, PORT))
        except BlockingIOError:
            pass
        for _ in range(1000):
            sock.send(testdata)
            received_data = b''
            while True:
                try:
                    data = sock.recv(BUFFER)
                    if not data:
                        break
                    received_data += data
                except BlockingIOError:
                    pass
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


async def asynchronous_socket_speed():
    start_time = time.time()
    reader, writer = await asyncio.open_connection(HOST, PORT)
    for _ in range(1000):
        writer.write(testdata)
        await writer.drain()
        received_data = b''
        while True:
            data = await reader.read(BUFFER)
            if not data:
                break
            received_data += data
    writer.close()
    await writer.wait_closed()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def unix_domain_socket_speed():
    start_time = time.time()
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(UNIX_SOCKET_PATH)
        for _ in range(1000):
            sock.sendall(testdata)
            received_data = b''
            while True:
                data = sock.recv(BUFFER)
                if not data:
                    break
                received_data += data
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


if __name__ == "__main__":
    # Create a Unix domain socket server
    if os.path.exists(UNIX_SOCKET_PATH):
        os.remove(UNIX_SOCKET_PATH)

    # Start the server
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(UNIX_SOCKET_PATH)
    server.listen(1)

    original_time = original_blocking_socket_speed()
    print(f"Original blocking socket speed: {original_time:.2f} seconds")

    non_blocking_time = non_blocking_socket_speed()
    print(f"Non-blocking socket speed: {non_blocking_time:.2f} seconds")

    loop = asyncio.get_event_loop()
    async_time = loop.run_until_complete(asynchronous_socket_speed())
    print(f"Asynchronous socket speed: {async_time:.2f} seconds")

    unix_time = unix_domain_socket_speed()
    print(f"Unix domain socket speed: {unix_time:.2f} seconds")

    # Clean up the Unix domain socket file
    server.close()
    os.remove(UNIX_SOCKET_PATH)
