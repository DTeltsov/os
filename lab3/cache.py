import cProfile
import functools


@functools.lru_cache(maxsize=None)
def calculate_fibonacci_with_cache(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci_with_cache(n - 1) + calculate_fibonacci_with_cache(n - 2)


@functools.lru_cache(maxsize=0)
def calculate_fibonacci_no_cache(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci_no_cache(n - 1) + calculate_fibonacci_no_cache(n - 2)


if __name__ == '__main__':
    numbers_to_calculate = [35, 35, 35, 35, 40, 40, 40, 40]
    for num in numbers_to_calculate:
        func = f'calculate_fibonacci_no_cache({num})'
        cProfile.run(func)
    for num in numbers_to_calculate:
        func = f'calculate_fibonacci_with_cache({num})'
        cProfile.run(func)
    print(calculate_fibonacci_no_cache.cache_info())
    print(calculate_fibonacci_with_cache.cache_info())
