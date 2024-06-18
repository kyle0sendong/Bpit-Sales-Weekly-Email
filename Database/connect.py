import pyodbc


def get_cursor(credentials, driver='ODBC Driver 17 for SQL Server'):

    try:
        connection = pyodbc.connect(f'DRIVER={driver};'
                                    f'SERVER={credentials.ServerName};'
                                    f'DATABASE={credentials.DatabaseName};'
                                    f'UID={credentials.Username};'
                                    f'PWD={credentials.Password}')

        return connection.cursor()

    except Exception as e:
        print(e)
        return None


def get_cursor_localhost_mssql(credentials, driver='ODBC Driver 17 for SQL Server'):

    try:
        connection = pyodbc.connect(f'DRIVER={driver};'
                                    f'SERVER={credentials["ServerName"]};'
                                    f'DATABASE={credentials["DatabaseName"]};'
                                    f'Trusted_Connection=Yes')

        return connection.cursor()

    except Exception as e:
        print(e)
        return None


def get_cursor_localhost_mysql(credentials):

    try:
        connection = pyodbc.connect(f'DRIVER={credentials["Driver"]};'
                                    f'SERVER={credentials["ServerName"]};'
                                    f'DATABASE={credentials["DatabaseName"]};'
                                    f'UID={credentials["Username"]};'
                                    f'PWD={credentials["Password"]}')

        return connection.cursor()

    except Exception as e:
        print(e)
        return None