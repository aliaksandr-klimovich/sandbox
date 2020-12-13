import time
from threading import Thread


def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


t = Thread(target=countdown, args=(5,))
# Daemonic threads can’t be joined.
# However, they are destroyed automatically when the main thread terminates.

t.start()
