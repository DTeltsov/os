import mmap
from multiprocessing.shared_memory import SharedMemory
import os
import queue
import sys


class IPC:
    SIZE = 1024
    SYMBOL = b"\0"

    def create_test_file(self):
        pass

    def delete_test_file(self):
        pass

    def read(self, iterations):
        pass

    def write(self, iterations):
        pass


class Mmap(IPC):
    FILE = "mmap_benchmark.txt"

    def __str__(self):
        return 'mmap'

    def create_test_data(self):
        with open(self.FILE, "wb") as file:
            file.write(b'\0' * self.SIZE)

    def delete_test_data(self):
        if os.path.exists(self.FILE):
            os.remove(self.FILE)

    def read(self, iterations):
        data_bytes = 0
        with open(self.FILE, "r+b") as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                for _ in range(iterations):
                    mmapped_file[:self.SIZE]
                    data_bytes += self.SIZE
        return data_bytes

    def write(self, iterations):
        data_bytes = 0
        with open(self.FILE, 'r+b') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_WRITE) as mmapped_file:
                for _ in range(iterations):
                    mmapped_file[:len(self.SYMBOL)] = self.SYMBOL
                    data_bytes += sys.getsizeof(self.SYMBOL)
                mmapped_file.flush()
        return data_bytes


class SharedMemoryIpc(IPC):
    shared_memory = None

    def __str__(self):
        return 'shared_memory'

    def create_test_data(self):
        self.shared_memory = SharedMemory(create=True, size=self.SIZE)

    def delete_test_data(self):
        self.shared_memory.close()
        self.shared_memory.unlink()

    def write(self, num_iterations):
        data_bytes = 0
        for _ in range(num_iterations):
            self.shared_memory.buf[:len(self.SYMBOL)] = self.SYMBOL
            data_bytes += sys.getsizeof(self.SYMBOL)
        return data_bytes

    def read(self, num_iterations):
        data_bytes = 0
        for _ in range(num_iterations):
            self.shared_memory.buf[:self.SIZE]
            data_bytes += self.SIZE
        return data_bytes


class File(IPC):
    FILE = 'testing_file.txt'
    SYMBOL = '\0'

    def __str__(self):
        return 'file'

    def create_test_data(self):
        with open(self.FILE, "w") as file:
            file.write(self.SYMBOL * int(1024 / len(self.SYMBOL.encode('utf-8'))))

    def delete_test_data(self):
        if os.path.exists(self.FILE):
            os.remove(self.FILE)

    def write(self, num_iterations):
        data_bytes = 0
        with open(self.FILE, 'w') as file:
            for _ in range(num_iterations):
                file.write(self.SYMBOL)
                data_bytes += sys.getsizeof(self.SYMBOL)
        return data_bytes

    def read(self, num_iterations):
        data_bytes = 0
        with open(self.FILE, 'r') as file:
            for _ in range(num_iterations):
                data_bytes += sys.getsizeof(file.read())
        return data_bytes


class Fifo(IPC):
    FILE = "test_fifo"
    SYMBOL = '\0'

    def __str__(self):
        return 'fifo'

    def create_test_data(self):
        os.mkfifo(self.FILE)

    def delete_test_data(self):
        if os.path.exists(self.FILE):
            os.remove(self.FILE)

    def write(self, num_iterations):
        with open(self.FILE, "w") as fifo:
            for _ in range(num_iterations):
                fifo.write(self.SYMBOL)

    def read(self, num_iterations):
        with open(self.FILE, "r") as fifo:
            for _ in range(num_iterations):
                fifo.read()


class Queue(IPC):
    queue = None
    SIZE = 1000 * 1000
    SYMBOL = '\0'

    def __str__(self):
        return 'queue'

    def create_test_data(self):
        self.queue = queue.Queue(self.SIZE)
        for i in range(self.SIZE):
            self.queue.put(self.SYMBOL)

    def delete_test_data(self):
        pass

    def write(self, num_iterations):
        data_bytes = 0
        for _ in range(num_iterations):
            self.queue.put(self.SYMBOL)
            data_bytes += sys.getsizeof(self.SYMBOL)
        return data_bytes

    def read(self, num_iterations):
        data_bytes = 0
        for _ in range(num_iterations):
            data_bytes += sys.getsizeof(self.queue.get())
        return data_bytes
