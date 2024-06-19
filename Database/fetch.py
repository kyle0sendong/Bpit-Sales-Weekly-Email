from datetime import date, timedelta
from Logs.logger import logger


def create_log(level, message):
    execution_logger = logger('database_log',
                              './Logs/db.log',
                              '%(levelname)s. %(message)s %(asctime)s')

    execution_logger.write_log(level=level, message=message)


def get_custom_query(cursor, query, count=200):
    try:
        cursor.execute(query)
        return cursor.fetchmany(count)
    except Exception as e:
        create_log(40, f"Error executing {query}: '{e}'")


def get_all_data(cursor, table_name, count=9999):
    query = f"SELECT * FROM {table_name}"

    try:
        cursor.execute(query)
        return cursor.fetchmany(count)
    except Exception as e:
        create_log(40, f"Error executing {query}: '{e}'")


def get_latest_data(cursor, table_name):
    query = f"SELECT * FROM {table_name} WHERE Date_Time = (SELECT MAX(Date_Time) FROM {table_name})"
    try:
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        create_log(40, f"Error executing {query}: '{e}'")


def get_date_range_data(cursor, table_name, start_date, end_date, count=9999):
    query = f"SELECT * FROM {table_name} WHERE Date_Time >= '{start_date}' AND Date_Time <= '{end_date}'"
    try:
        cursor.execute(query)
        return cursor.fetchmany(count)
    except Exception as e:
        create_log(40, f"Error executing {query}: '{e}'")


def get_last_week_data(cursor, table_name, count=9999):
    end_date = date.today()
    start_date = (end_date - timedelta(days=7))
    query = f"SELECT * FROM {table_name} WHERE Date_Time >= '{start_date}' AND Date_Time <= '{end_date}'"
    try:
        cursor.execute(query)
        return cursor.fetchmany(count)
    except Exception as e:
        create_log(40, f"Error executing {query}: '{e}'")
