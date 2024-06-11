from datetime import date, timedelta


def get_custom_query(cursor, query, count=200):
    cursor.execute(query)
    return cursor.fetchmany(count)


def get_all_data(cursor, table_name, count=9999):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    return cursor.fetchmany(count)


def get_latest_data(cursor, table_name):
    query = f"SELECT * FROM {table_name} WHERE Date_Time = (SELECT MAX(Date_Time) FROM {table_name})"
    cursor.execute(query)
    return cursor.fetchone()


def get_date_range_data(cursor, table_name, start_date, end_date, count=9999):
    query = f"SELECT * FROM {table_name} WHERE Date_Time >= '{start_date}' AND Date_Time <= '{end_date}'"
    cursor.execute(query)
    return cursor.fetchmany(count)


def get_last_week_data(cursor, table_name, count=9999):
    end_date = date.today()
    start_date = (end_date - timedelta(days=7))
    query = f"SELECT * FROM {table_name} WHERE Date_Time >= '{start_date}' AND Date_Time <= '{end_date}'"
    cursor.execute(query)
    return cursor.fetchmany(count)
