from joblib import Memory, Parallel, delayed
import time

cache_dir = '/tmp/joblib_cache'
memory = Memory(cache_dir, verbose=0)


@memory.cache
def expensive_function(n):
    time.sleep(2)
    return n * 2


if __name__ == '__main__':
    num_jobs = 4

    start_time = time.time()
    results_without_cache = Parallel(n_jobs=num_jobs)(delayed(expensive_function)(i) for i in range(num_jobs))
    end_time = time.time()
    print("Час без кешу:", end_time - start_time)

    start_time = time.time()
    results_with_cache = Parallel(n_jobs=num_jobs)(delayed(expensive_function)(i) for i in range(num_jobs))
    end_time = time.time()
    print("Час з кешем:", end_time - start_time)
