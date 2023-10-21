import socket


HOST = "localhost"
PORT = 50007
IS_RECONNECT_ENABLED = False

BUFFER = 4096

testdata = b'x' * BUFFER * 4


if __name__ == "__main__":
    is_started = False
    while IS_RECONNECT_ENABLED or not is_started:
        is_started = True
        print()
        print("Create client")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print("Client connected")
            for i in range(1, 1000000):
                sock.send(testdata)
            # while True:
            #     # Input
            #     data = input("Type the message to send:")
            #     if data == "exit":
            #         print("Close by client")
            #         break
            #     # Send
            #     data_bytes = data.encode()
            #     sock.sendall(data_bytes)
            #     # Receive
            #     data_bytes = sock.recv(1024)
            #     data = data_bytes.decode()
            #     print("Received:", repr(data))
            #     if not data:
            #         print("Closed by server")
            #         break
            print("Client disconnected")
