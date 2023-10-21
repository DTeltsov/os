import datetime
import inspect


def speed_test(func):
    if inspect.iscoroutine(func):
        async def async_wrapper(self, *args, **kwargs):
            starttime = datetime.datetime.now()
            result = await func(self, *args, **kwargs)
            endtime = datetime.datetime.now()
            print(f'bytes transferred: {result}')
            delta = endtime - starttime
            delta = delta.seconds + delta.microseconds / 1000000.0
            print(f'time used (seconds): {delta}')
            print(f'averaged speed (MB/s): {(result / 1024 / 1024 / delta)}\n\r')
            return result
        return async_wrapper
    else:
        def wrapper(self, *args, **kwargs):
            starttime = datetime.datetime.now()
            result = func(self, *args, **kwargs)
            endtime = datetime.datetime.now()
            print(f'bytes transferred: {result}')
            delta = endtime - starttime
            delta = delta.seconds + delta.microseconds / 1000000.0
            print(f'time used (seconds): {delta}')
            print(f'averaged speed (MB/s): {(result / 1024 / 1024 / delta)}\n\r')
            return result
        return wrapper


class SocketWithTests:
    HOST = "localhost"
    PORT = 50007
    BUFFER = 4096

    def create_socket(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError
