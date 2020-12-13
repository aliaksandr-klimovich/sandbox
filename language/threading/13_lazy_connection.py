import threading
from socket import socket, AF_INET, SOCK_STREAM
from functools import partial


class LazyConnection:
    def __init__(self, address, family=AF_INET, type_=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type_
        self.local = threading.local()

    def __enter__(self):
        if hasattr(self.local, 'sock'):
            raise RuntimeError('Already connected')
        self.local.sock = socket(self.family, self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.local.sock.close()
        del self.local.sock


def test(connection):
    assert isinstance(connection, LazyConnection)
    with connection as s:
        print('{} Socket id: {}'.format(threading.current_thread().getName(), s))
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')
        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv, 8192), b''))

    print('{} Got {} bytes'.format(threading.current_thread().getName(), len(resp)))


if __name__ == '__main__':
    lazy_connection = LazyConnection(('www.python.org', 80),)
    t1 = threading.Thread(target=test, args=(lazy_connection,))
    t2 = threading.Thread(target=test, args=(lazy_connection,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
