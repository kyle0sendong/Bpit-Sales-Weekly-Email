import pyodbc


def create_database():
    driver = 'MySQL ODBC 8.1 ANSI Driver'
    server = '127.0.0.1'
    user = 'root'
    password = ''

    try:
        connection = pyodbc.connect(f'DRIVER={driver};'
                                    f'SERVER={server};'
                                    f'UID={user};'
                                    f'PWD={password}')

        cursor = connection.cursor()
        database_name = "Sales_Mailer"

        collation = "utf8mb4_unicode_ci"
        cursor.execute(f"CREATE DATABASE {database_name} "
                       f"CHARACTER SET utf8mb4 "
                       f"COLLATE {collation}")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Database error {e}')
        return
