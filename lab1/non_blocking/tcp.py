import socket
import time
from test_socket import SocketTest


class NonBlockingTcp(SocketTest):
    port = 54323

    def __str__(self):
        return 'Non-Blocking TCP'

    def client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.url, self.port))
        client_socket.setblocking(False)

        start_time = time.time()

        for _ in range(self.num_pack):
            while True:
                try:
                    client_socket.sendall(self.get_data_to_send())
                    break
                except socket.error:
                    pass

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Time taken: {elapsed_time} seconds")

        client_socket.close()

    def server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.url, self.port))
        server_socket.listen(1)
        server_socket.setblocking(False)

        print(f"{self} server listening on port {self.port}")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                break
            except socket.error:
                pass

        client_socket.setblocking(True)

        total_bytes_received = 0
        start_time = time.time()

        while True:
            try:
                data = client_socket.recv(self.pack_size)
                if not data:
                    break
                total_bytes_received += len(data)
            except socket.error:
                pass

        end_time = time.time()
        elapsed_time = end_time - start_time

        pps = self.num_pack / elapsed_time
        bps = total_bytes_received / elapsed_time

        print(f"Time taken: {elapsed_time} seconds")
        print(f"Packets per second: {pps}")
        print(f"Bytes per second: {bps}")
        self.test_results[f'num_pack: {self.num_pack} / pack_size: {self.pack_size}'] = {
            'elapsed_time': elapsed_time,
            'pps': f'{pps:.10f}',
            'bps': f'{bps:.10f}'
        }

        client_socket.close()
        server_socket.close()
