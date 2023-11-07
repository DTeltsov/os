import socket
import time
from test_socket import SocketTest


class BlockingUdp(SocketTest):
    port = 54322

    def __str__(self):
        return 'Blocking UDP'

    def client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        start_time = time.time()

        for _ in range(self.num_pack):
            client_socket.sendto(self.get_data_to_send(), (self.url, self.port))
        client_socket.sendto(b"terminate", (self.url, self.port))

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Time taken: {elapsed_time} seconds")

        client_socket.close()

    def server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.url, self.port))

        print(f"{self} server listening on port {self.port}")

        total_bytes_received = 0
        start_time = time.time()

        while True:
            data, _ = server_socket.recvfrom(self.pack_size)
            total_bytes_received += len(data)
            if data == b"terminate":
                break

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

        server_socket.close()
