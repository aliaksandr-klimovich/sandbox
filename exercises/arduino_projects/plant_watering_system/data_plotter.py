import os
import webbrowser
from collections import namedtuple
from datetime import timedelta, datetime
from threading import Thread

from data_saver import DB
from logger import get_logger

PLOT_FILE_NAME = 'plot.svg'
PLOT_SIZE = namedtuple('PLOT_SIZE', 'width,height')(width=800, height=600)
PIPE_NAME = 'tmp_pipe'
ROLL_BACK_TIME = timedelta(days=1)

log = get_logger(__name__)


def gnuplot():
    cmd = (
        f'exec 0>/dev/null 1>/dev/null 2>/dev/null 3<{PIPE_NAME};'
        f'gnuplot -e "'
        f'set terminal svg size {PLOT_SIZE.width},{PLOT_SIZE.height};'
        f'set output \'{PLOT_FILE_NAME}\';'
        f'set datafile separator comma;'
        f'set xdata time;'
        f'set timefmt \'%Y-%m-%dT%H:%M:%S\';'
        f'set format x \'%d/%H:%M\';'
        f'unset key;'
        f'plot \'<&3\' using 1:2;";'
    )
    log.debug(cmd)
    os.system(cmd)


def pipe_writer(data):
    log.debug(f'pipe_name = {PIPE_NAME}')
    fd = os.open(PIPE_NAME, os.O_WRONLY)
    log.debug(f'fd = {fd}')
    for x, y in data:
        assert isinstance(x, datetime)
        timestamp = x.isoformat(timespec='seconds')
        os.write(fd, bytes(f'{timestamp},{y}\n', 'utf-8'))
    os.close(fd)


def main():
    if not os.path.exists(PIPE_NAME):
        log.info(f'Pipe does not exit, create pipe {PIPE_NAME}')
        os.mkfifo(PIPE_NAME)

    db = DB()
    data = db.get_data(ROLL_BACK_TIME)
    db.disconnect()

    thread_gnuplot = Thread(target=gnuplot)
    thread_pipe_writer = Thread(target=pipe_writer, args=(data,))

    thread_gnuplot.start()
    thread_pipe_writer.start()

    thread_gnuplot.join()
    thread_pipe_writer.join()

    cwd = os.getcwd()
    log.debug(cwd)
    log.info(f'Open svg file {PLOT_FILE_NAME}')
    webbrowser.open(f'file://{cwd}/{PLOT_FILE_NAME}')

    if os.path.exists(PIPE_NAME):
        log.info(f'Remove pipe {PIPE_NAME}')
        os.remove(PIPE_NAME)


if __name__ == '__main__':
    main()
