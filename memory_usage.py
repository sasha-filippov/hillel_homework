import psutil


def resource_usage(func):

    def wrapper(*args, **kwargs):
        cpu_before = psutil.cpu_percent()
        process = psutil.Process()
        mem_before = process.memory_info().rss
        result = func(*args, **kwargs)
        cpu_after = psutil.cpu_percent()
        mem_after = process.memory_info().rss

        print(f"CPU usage: {cpu_after - cpu_before}%")
        print(f"Memory usage: {mem_after - mem_before} bytes")
        return result

    return wrapper


@resource_usage
def some_loop():
    for x in range(1999999):
        continue
    print("done")


some_loop()
