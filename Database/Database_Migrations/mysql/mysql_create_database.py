import pyodbc


def create_database(driver, server, user, password, database_name):

    try:
        connection = pyodbc.connect(f'DRIVER={driver};'
                                    f'SERVER={server};'
                                    f'UID={user};'
                                    f'PWD={password}')

        cursor = connection.cursor()

        collation = "utf8mb4_unicode_ci"
        cursor.execute(f"CREATE DATABASE {database_name} "
                       f"CHARACTER SET utf8mb4 "
                       f"COLLATE {collation}")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f'Database error {e}')
        return
