import threading, time
from random import random


def f(lock):
    current_thread_name = threading.current_thread().getName()
    for _ in range(5):
        with lock:
            print('{} Lock acquired'.format(current_thread_name))
            time.sleep(random())
        print('{} Lock released'.format(current_thread_name))


_lock = threading.Lock()

for _ in range(5):
    t = threading.Thread(target=f, args=(_lock,))
    t.start()
