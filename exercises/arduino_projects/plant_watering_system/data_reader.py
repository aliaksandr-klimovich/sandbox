import time

from data_saver import DB
from logger import get_logger
from serial import Serial
from serial.serialutil import SerialException

# DEVICE_PATH = '/dev/cu.wchusbserial1410'
DEVICE_PATH = 'COM4'

CONNECT_WITH_RETRY_ATTEMPTS = 10
CONNECT_WITH_RETRY_SLEEP_TIME = 5  # [s]

log = get_logger(__name__)


class DataReader:
    def __init__(self, device_path):
        self.device_path = device_path

        self._connection = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    def _connect(self):
        log.debug('_connect()')
        log.info(f'Try to connect to device {self.device_path}')
        try:
            self._connection = Serial(self.device_path)
        except SerialException:
            log.warning(f'[FAIL] Cannot connect to device {self.device_path}')
            self._connected = False
        else:
            log.info(f'[OK] Connected to {self.device_path}')
            self._connected = True

    def _connect_with_retry(self, attempts=CONNECT_WITH_RETRY_ATTEMPTS, sleep_time=CONNECT_WITH_RETRY_SLEEP_TIME):
        log.debug(f'_connect_with_retry(attempts={attempts}, sleep_time={sleep_time})')
        for attempt in range(1, attempts + 1):
            log.info(f'Attempt {attempt}')
            self._connect()
            if self._connected is True:
                break
            else:
                if attempt != attempts:
                    log.info(f'Sleep {sleep_time} seconds before next attempt')
                    time.sleep(sleep_time)

    def connect(self, with_retry=True, **kwargs):
        log.debug(f'connect(with_retry={with_retry}, kwargs={kwargs})')
        if with_retry is True:
            self._connect_with_retry(**kwargs)
        else:
            self._connect()

    def _get_value(self):
        log.debug('_get_value()')
        try:
            value = int(self._connection.readline())
        except SerialException:
            raise DataReaderException('Error in serial connection')
        except KeyboardInterrupt:
            raise DataReaderException('Read serial data interrupted')
        else:
            return value

    def _get_value_with_reconnect(self, **kwargs):
        log.debug('_get_value_with_reconnect()')
        try:
            value = self._get_value()
        except DataReaderException:
            self._connect_with_retry(**kwargs)
            if self._connected is False:
                raise DataReaderException('Cannot read the value from serial port')
            else:
                return self._get_value_with_reconnect(**kwargs)
        else:
            return value

    def get_value(self, with_reconnect=True, **kwargs):
        log.debug(f'get_value(with_reconnect={with_reconnect})')
        if with_reconnect is True:
            return self._get_value_with_reconnect(**kwargs)
        else:
            return self._get_value()


class DataReaderException(Exception):
    pass


def main():
    db = DB()
    reader = DataReader(DEVICE_PATH)

    reader.connect(attempts=3)
    if reader.connected is False:
        log.error(f'Cannot connect to device {DEVICE_PATH}. Leaving...')

    else:
        while True:
            try:
                value = reader.get_value(attempts=5)
            except DataReaderException:
                log.error(f'Cannot connect to device {DEVICE_PATH}. Leaving...')
                break
            else:
                db.insert_value(value)

    db.disconnect()


if __name__ == '__main__':
    main()
