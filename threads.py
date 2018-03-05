import threading


def task(x):
    x = 0
    for i in range(1, 300000):
        x = i * i / i / i * i
        x = x * i / i
        # print(x)


def run(threads_count):
    events = {}
    threads = {}
    print(threads_count)
    for i in range(threads_count):
        threads[i] = threading.Thread(target=task, args=(0,))

    for i in range(threads_count):
        threads[i].start()

    for i in range(threads_count):
        threads[i].join()
