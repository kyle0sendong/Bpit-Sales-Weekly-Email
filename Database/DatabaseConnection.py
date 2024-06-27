from enum import Enum

import pyodbc

from Error_Handler.CatchExceptionDecorator import catch_exceptions


class DatabaseDriver(Enum):
    mssql_driver = 'ODBC Driver 17 for SQL Server'
    mysql_driver = 'MySQL ODBC 8.1 ANSI Driver'


@catch_exceptions
class DatabaseConnection:

    def __init__(self, driver, server, username, password, database) -> None:
        self.server: str = server
        self.database: str = database
        self.username: str = username
        self.password: str = password
        self.driver = driver

        self.connection = pyodbc.connect(f'DRIVER={self.driver};'
                                         f'SERVER={self.server};'
                                         f'DATABASE={self.database};'
                                         f'UID={self.username};'
                                         f'PWD={self.password}')
        self.cursor = self.connection.cursor()

    def get_cursor(self) -> pyodbc.Cursor:
        return self.cursor

    def close_connection(self) -> None:
        self.connection.close()

    def close_cursor(self) -> None:
        self.cursor.close()
