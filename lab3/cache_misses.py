import multiprocessing
import functools
import time


@functools.lru_cache(maxsize=None)
def calculate_fibonacci_with_cache(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci_with_cache(n - 1) + calculate_fibonacci_with_cache(n - 2)


def calculate_fibonacci_no_cache(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci_no_cache(n - 1) + calculate_fibonacci_no_cache(n - 2)


def worker_function_with_cache(n):
    start_time = time.time()
    result = calculate_fibonacci_with_cache(n)
    end_time = time.time()
    print(f"Число Фібоначчі {n} (з кешем) = {result}, час обчислення: {end_time - start_time:.5f} сек")


def worker_function_no_cache(n):
    start_time = time.time()
    result = calculate_fibonacci_no_cache(n)
    end_time = time.time()
    print(f"Число Фібоначчі {n} (без кешу) = {result}, час обчислення: {end_time - start_time:.5f} сек")


if __name__ == '__main__':
    multiprocessing.freeze_support()

    numbers_to_calculate = [35, 35, 35, 35, 40, 40, 40, 40]

    processes_with_cache = []
    processes_no_cache = []

    for num in numbers_to_calculate:
        process_with_cache = multiprocessing.Process(target=worker_function_with_cache, args=(num,))
        process_no_cache = multiprocessing.Process(target=worker_function_no_cache, args=(num,))

        processes_with_cache.append(process_with_cache)
        processes_no_cache.append(process_no_cache)

        process_with_cache.start()
        process_no_cache.start()

    for process_with_cache, process_no_cache in zip(processes_with_cache, processes_no_cache):
        process_with_cache.join()
        process_no_cache.join()

    print("Всі процеси завершили обчислення.")
