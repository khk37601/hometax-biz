import pymysql

from .connect import DB
from environment import EnvironmentManager


class MariaDB(DB):
    def __init__(self):
        self.config = EnvironmentManager()
        connection = pymysql.connect(
            user=self.config.get('MARIADB_USER_NAME'),
            password=self.config.get('MARIADB_USER_PASSWORD'),
            db=self.config.get('MARIADB_DB_NAME'),
            host=self.config.get('MARIADB_HOST'),
            port=3306,
            read_timeout=2,
            write_timeout=2,
            connect_timeout=2,
        )
        super().__init__(connection, connection.cursor(pymysql.cursors.DictCursor))

    def __del__(self):
        del self.config

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__del__()
