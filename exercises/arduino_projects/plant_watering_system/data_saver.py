import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from logger import get_logger

DB_NAME = 'sqlite3_database.db'
TABLE_NAME = 'DATA'

log = get_logger(__name__)


def require_connection(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.connected is True:
            return f(self, *args, **kwargs)
        else:
            log.error(f'Function {f.__name__} requires connection. Skip call...')

    return wrapper


class DB:
    def __init__(self):
        self._connected = False

        self._connection = None
        self._cursor = None

        self.connect()
        self.create()

    @property
    def connected(self):
        return self._connected

    def connect(self):
        log.info(f'Connect to DB {DB_NAME}')
        self._connection = sqlite3.connect(DB_NAME)
        self._cursor = self._connection.cursor()
        self._connected = True

    @require_connection
    def create(self):
        sql = f'create table if not exists {TABLE_NAME} (ts timestamp, v integer)'
        log.debug(sql)
        self._cursor.execute(sql)
        self._connection.commit()

    @require_connection
    def insert_value(self, value: int):
        timestamp = datetime.now()
        sql = f'insert into {TABLE_NAME} values ("{timestamp}", {value})'
        log.debug(sql)
        self._cursor.execute(sql)
        self._connection.commit()

    @require_connection
    def disconnect(self):
        log.debug(f'Disconnect from DB {DB_NAME}')
        self._cursor.close()
        self._connection.close()
        self._connected = False

    @require_connection
    def get_data(self, time_delta_backward: timedelta = timedelta(days=1)):
        log.debug(f'get_data(time_delta_backward={time_delta_backward})')
        datetime_format = "%Y-%m-%d %H:%M:%S.%f"

        sql = f'select ts from {TABLE_NAME} order by ts desc limit 1'
        log.debug(sql)
        self._cursor.execute(sql)
        last_time_stamp = self._cursor.fetchone()[0]
        log.debug(f'last_time_stamp = {last_time_stamp}')

        dt = datetime.strptime(last_time_stamp, datetime_format)
        start_ts = dt - time_delta_backward
        sql = f'select ts, v from {TABLE_NAME} where ts > "{start_ts}"'
        log.debug(sql)
        self._cursor.execute(sql)
        ret_data = self._cursor.fetchall()
        log.debug(f'data_length = {len(ret_data)}, last_sample = {ret_data[-1]}')

        data = []
        for ts, v in ret_data:
            try:
                timestamp = datetime.strptime(ts, datetime_format)
            except ValueError:
                timestamp = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            data.append((timestamp, v))
        return data
