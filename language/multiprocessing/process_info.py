from multiprocessing import Process
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process id:', os.getppid())
    print('process id:', os.getpid())


def f():
    info('-- function f --')


if __name__ == '__main__':
    info('-- main --')
    p = Process(target=f)
    p.start()
    p.join()
