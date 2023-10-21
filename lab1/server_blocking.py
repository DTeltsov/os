import socket
import datetime

HOST = "localhost"
PORT = 50007
BUFFER = 4096


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        print("Server started")
        print("Waiting for connection...")
        sock, addr = serv_sock.accept()
        starttime = datetime.datetime.now()
        with sock:
            print("Connected by", addr)
            count = 0
            while True:
                data = sock.recv(BUFFER)
                if data:
                    count += len(data)
                    del data
                    continue
                break
        endtime = datetime.datetime.now()
        print(endtime)
        print('%s:%s disconnected\n\r' % addr)

        print('bytes transferred: %d' % count)
        delta = endtime - starttime
        delta = delta.seconds + delta.microseconds / 1000000.0
        print('time used (seconds): %f' % delta)
        print('averaged speed (MB/s): %f\n\r' % (count / 1024 / 1024 / delta))
