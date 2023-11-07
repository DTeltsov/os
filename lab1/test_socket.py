from threading import Thread


class SocketTest:
    num_pack = 1000
    pack_size = 1024
    data_to_send = b'\xff'
    url = '127.0.0.1'
    testing_params = [
        {'num_pack': 10000, 'pack_size': 1024},
        {'num_pack': 100000, 'pack_size': 1024},
        {'num_pack': 1000000, 'pack_size': 1024},
        {'num_pack': 10000, 'pack_size': 4096},
        {'num_pack': 100000, 'pack_size': 4096},
        {'num_pack': 1000000, 'pack_size': 4096},
    ]

    def __init__(self):
        self.test_results = {}

    @classmethod
    def get_df_headers(cls):
        return [
            f'num_pack: {param.get("num_pack")} / pack_size: {param.get("pack_size")}'
            for param in cls.testing_params
        ]

    def get_data_to_send(self):
        return self.data_to_send * self.pack_size

    def server(self):
        raise NotImplementedError

    def client(self):
        raise NotImplementedError

    def test(self):
        for param in self.testing_params:
            num_pack = param.get('num_pack')
            pack_size = param.get('pack_size')
            print(f'Test {num_pack} packs with size {pack_size}')
            self.num_pack = num_pack
            self.pack_size = pack_size
            server_thread = Thread(target=self.server)
            client_thread = Thread(target=self.client)
            server_thread.start()
            client_thread.start()
            server_thread.join()
            client_thread.join()
            print('\n')
