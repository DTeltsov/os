import socket


HOST = "localhost"
PORT = 50007

connections = []  # New

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        serv_sock.setblocking(False)  # New
        print("Server started")
        while True:
            # Try accept new connections
            try:  # New
                # print("Waiting for connection...")
                sock, addr = serv_sock.accept()
                sock.setblocking(False)
                print("Connected by", addr)
                connections.append((sock, addr))
            except BlockingIOError:
                # print("No connections are waiting to be accepted")
                pass
            # Try receive from current
            for sock, addr in connections.copy():  # New
                print("Try", sock, addr)
                # Receive
                try:
                    data = sock.recv(1024)
                except ConnectionError:
                    print(f"Client suddenly closed while receiving from {addr}")
                    connections.remove((sock, addr))  # New
                    sock.close()
                    continue
                except BlockingIOError:  # New
                    # No data received
                    continue
                print(f"Received: {data} from: {addr}")
                if not data:
                    connections.remove((sock, addr))  # New
                    sock.close()
                    print("Disconnected by", addr)
                    continue
                # Process
                if data == b"close":
                    break
                data = data.upper()
                # Send
                print(f"Send: {data} to: {addr}")
                try:
                    sock.sendall(data)
                except ConnectionError:
                    print(f"Client suddenly closed, cannot send to {addr}")
                    connections.remove((sock, addr))  # New
                    sock.close()
                    continue
