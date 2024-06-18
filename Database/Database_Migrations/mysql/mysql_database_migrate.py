import pyodbc

from mysql_create_database import create_database
from tables.customer_table import create_customer_table
from tables.arm_table import create_arm_table
from tables.sales_table import create_sales_table

import os
from dotenv import load_dotenv

load_dotenv()

driver = os.getenv("ODBC_DRIVER_MYSQL")
server = os.getenv("SERVER3_MYSQL_LOCALHOST_NAME")
user = os.getenv("SERVER3_MYSQL_LOCALHOST_USERNAME")
password = os.getenv("SERVER3_MYSQL_LOCALHOST_PASSWORD")
database_name = os.getenv("LOCAL_MYSQL_DATABASE")


def connection():

    return pyodbc.connect(f'DRIVER={driver};'
                          f'SERVER={server};'
                          f'DATABASE={database_name};'
                          f'UID={user};'
                          f'PWD={password};'
                          f'charset=utf8',
                          autocommit=True)


def database_migrate():
    create_database(driver, server, user, password, database_name)
    create_arm_table(connection())
    create_sales_table(connection())
    create_customer_table(connection())
    print("Finished migrating")


database_migrate()
