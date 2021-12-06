from time import perf_counter

def timer(f):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        value = f(*args, **kwargs)
        elapsed = perf_counter() - start
        print(elapsed)
        return value
    return wrapper