import pyodbc

from mysql_create_database import create_database
from tables.customer_table import create_customer_table
from tables.arm_table import create_arm_table
from tables.sales_table import create_sales_table


def connection():
    driver = 'MySQL ODBC 8.1 ANSI Driver'
    server = '127.0.0.1'
    database = 'Sales_Mailer'
    user = 'root'
    password = ''

    return pyodbc.connect(f'DRIVER={driver};'
                                f'SERVER={server};'
                                f'DATABASE={database};'
                                f'UID={user};'
                                f'PWD={password};'
                                f'charset=utf8',
                                autocommit=True)


def database_migrate():
    create_database()
    create_arm_table(connection())
    create_sales_table(connection())
    create_customer_table(connection())


database_migrate()