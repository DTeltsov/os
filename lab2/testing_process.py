import time


class TestingProcess:
    PARAMS = ['latency_read', 'latency_write', 'throughput_read', 'throughput_write']

    @staticmethod
    def measure_latency(func, iterations):
        start_time = time.time()
        func(iterations)
        end_time = time.time()
        latency = (end_time - start_time) / iterations
        return latency

    @staticmethod
    def measure_throughput(func, iterations):
        start_time = time.time()
        bytes = func(iterations)
        end_time = time.time()
        throughput = bytes / (end_time - start_time)
        return throughput

    def test(self, ipc, iterations=1000):
        test_result = dict(ipc=[str(ipc)])
        print(f'{ipc}')
        for param in self.PARAMS:
            measurable_param, measurable_io = param.split('_')
            measure_func = getattr(self, f'measure_{measurable_param}')
            param_result = [measure_func(getattr(ipc, measurable_io), iterations) for _ in range(iterations)]
            avg_param_result = sum(param_result) / len(param_result)
            value = 'seconds per operation' if measurable_param == 'latency' else 'bytes per second'
            print(f"\t{measurable_io.capitalize()} {measurable_param}: {avg_param_result:.10f} {value}")
            test_result[param] = [avg_param_result]
        return test_result

