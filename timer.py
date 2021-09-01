import time

def timer(f):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = f(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(elapsed)
        return value
    return wrapper