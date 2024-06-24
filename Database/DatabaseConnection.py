import pyodbc
from enum import Enum
from Error_Handler.CatchExceptionDecorator import catch_exceptions


class DatabaseDriver(Enum):
    mssql_driver = 'ODBC Driver 17 for SQL Server'
    mysql_driver = 'MySQL ODBC 8.1 ANSI Driver'


@catch_exceptions
class DatabaseConnection:

    cursor = None

    def __init__(self, driver, server, username, password, database=None) -> None:
        self.server: str = server
        self.database: str = database
        self.username: str = username
        self.password: str = password
        self.driver = driver

    def get_cursor(self) -> pyodbc.Cursor:

        connection = pyodbc.connect(f'DRIVER={self.driver};'
                                    f'SERVER={self.server};'
                                    f'DATABASE={self.database};'
                                    f'UID={self.username};'
                                    f'PWD={self.password}')
        self.cursor = connection.cursor()
        return connection.cursor()

    def close_cursor(self) -> None:
        self.cursor.close()
