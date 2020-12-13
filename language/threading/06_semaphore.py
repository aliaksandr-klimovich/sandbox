import threading


def worker(i, semaphore):
    assert isinstance(semaphore, threading.Semaphore)
    semaphore.acquire()
    print('Working', i)


semaphore = threading.Semaphore(0)
n_workers = 10
for i in range(n_workers):
    t = threading.Thread(target=worker, args=(i, semaphore,))
    t.start()

for i in range(n_workers):
    semaphore.release()
