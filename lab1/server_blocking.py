import socket
from utils import speed_test, SocketWithTests


class BlockingSocket(SocketWithTests):
    def create_socket(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.bind((self.HOST, self.PORT))
        serv_sock.listen(1)
        print("Server started")
        return serv_sock

    @speed_test
    def read(self, sock):
        count = 0
        with sock:
            while True:
                data = sock.recv(self.BUFFER)
                if data:
                    count += len(data)
                    del data
                    continue
                break
        return count


if __name__ == "__main__":
    blocking_server = BlockingSocket()
    serv_sock = blocking_server.create_socket()
    with serv_sock:
        print("Waiting for connection...")
        sock, addr = serv_sock.accept()
        blocking_server.read(sock)
