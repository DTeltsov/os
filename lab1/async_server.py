import asyncio
from utils import speed_test, SocketWithTests


class AsyncSocket(SocketWithTests):
    async def create_socket(self):
        server = await asyncio.start_server(self.read, self.HOST, self.PORT)
        print("Server started")
        return server

    @speed_test
    async def read(self, reader, writer):
        addr = writer.get_extra_info("peername")
        count = 0
        print("Connected by", addr)
        while True:
            data = await reader.read(self.BUFFER)
            print(data)
            if data:
                count += len(data)
                del data
                continue
            break
        return count


async def start_server():
    async_server = AsyncSocket()
    server = await async_server.create_socket()
    print(f"Start server...")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start_server())
