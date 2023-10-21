import socket
from utils import speed_test
from server_blocking import BlockingSocket


class NotBlockingSocket(BlockingSocket):
    def create_socket(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.bind((self.HOST, self.PORT))
        serv_sock.listen(1)
        serv_sock.setblocking(False)
        print("Server started")
        return serv_sock

    @speed_test
    def read(self, sock):
        count = 0
        with sock:
            print("Connected by", addr)
            while True:
                try:
                    data = sock.recv(self.BUFFER)
                except BlockingIOError:
                    continue
                if data:
                    count += len(data)
                    del data
                    continue
                break
        return count


if __name__ == "__main__":
    blocking_server = NotBlockingSocket()
    serv_sock = blocking_server.create_socket()
    with serv_sock:
        print("Waiting for connection...")
        while True:
            try:
                sock, addr = serv_sock.accept()
                break
            except BlockingIOError:
                continue
        sock.setblocking(False)
        blocking_server.read(sock)
