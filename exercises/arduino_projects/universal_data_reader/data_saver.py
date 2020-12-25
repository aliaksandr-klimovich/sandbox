import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from logger import get_default_logger

DEFAULT_DATABASE_NAME = 'sqlite3_database.db'
DEFAULT_TABLE_NAME = 'DATA'
DEFAULT_TIMEDELTA = timedelta(days=1)

log = get_default_logger(__name__)


class DataSaverException(Exception):
    pass


def require_connection(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self._connected is True:
            return f(self, *args, **kwargs)
        else:
            log.error(f'Function {f.__name__} requires connection. Skip call...')

    return wrapper


class DB:
    def __init__(self, database_name=DEFAULT_DATABASE_NAME, table_name=DEFAULT_TABLE_NAME):
        self._database_name = database_name
        self._table_name = table_name
        self._connected = False

        self._connection = None
        self._cursor = None

        self.connect()
        self.create_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def database_name(self) -> str:
        return self._database_name

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self):
        log.info(f'Connect to DB {self._database_name}')
        self._connection = sqlite3.connect(self._database_name)
        self._cursor = self._connection.cursor()
        self._connected = True

    @require_connection
    def create_table(self):
        sql = f'create table if not exists {self._table_name} (ts timestamp, v integer)'
        log.debug(sql)
        self._cursor.execute(sql)
        self._connection.commit()

    @require_connection
    def insert_value(self, value: int):
        timestamp = datetime.now()
        sql = f'insert into {self._table_name} values ("{timestamp}", {value})'
        log.debug(sql)
        self._cursor.execute(sql)
        self._connection.commit()

    @require_connection
    def disconnect(self):
        log.info(f'Disconnect from DB {self._database_name}')
        self._cursor.close()
        self._connection.close()
        self._connected = False

    @require_connection
    def get_data(self,
                 timedelta_backward: timedelta = None,
                 timedelta_start: timedelta = None,
                 timedelta_end: timedelta = None) -> list:

        if timedelta_backward is not None:
            log.debug(f'get_data(time_delta_backward={timedelta_backward})')
            datetime_format = "%Y-%m-%d %H:%M:%S.%f"

            # get last time stamp
            sql = f'select ts from {self._table_name} order by ts desc limit 1'
            log.debug(sql)
            self._cursor.execute(sql)
            last_time_stamp = self._cursor.fetchone()[0]
            log.debug(f'last_time_stamp = {last_time_stamp}')

            # calculate from when to fetch data
            dt = datetime.strptime(last_time_stamp, datetime_format)
            start_ts = dt - timedelta_backward

            # fetch data according to timedelta
            sql = f'select ts, v from {self._table_name} where ts > "{start_ts}"'
            log.debug(sql)
            self._cursor.execute(sql)
            ret_data = self._cursor.fetchall()
            try:
                last_sample = ret_data[-1]
            except IndexError:
                last_sample = None
            log.debug(f'data_length = {len(ret_data)}, last_sample = {last_sample}')

        elif timedelta_start is not None and timedelta_end is not None:
            raise NotImplementedError()

        else:
            raise DataSaverException('Invalid arguments')

            # format data: [(timestamp, value), (timestamp, value), ...]
        data = []
        for ts, v in ret_data:
            timestamp = datetime.strptime(ts, datetime_format)
            data.append((timestamp, v))
        return data

# if __name__ == '__main__':
#     db = DB()
#     while True:
#         try:
#             db.insert_value(0)
#         except KeyboardInterrupt:
#             break
#     db.disconnect()
