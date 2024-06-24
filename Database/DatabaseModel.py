from datetime import date, timedelta
from Error_Handler.CatchExceptionDecorator import catch_exceptions


@catch_exceptions
class DatabaseModel:

    def __init__(self, cursor):
        self.cursor = cursor

    def get_data(self, table, row_id):
        query = f"SELECT * FROM {table} WHERE Id = {row_id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_data_custom_query(self, query, count=9999):
        self.cursor.execute(query)
        return self.cursor.fetchmany(count)

    def get_all_data(self, table, count=9999):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        return self.cursor.fetchmany(count)

    def get_latest_data(self, table):
        query = f"SELECT * FROM {table} WHERE Date_Time = (SELECT MAX(Date_Time) FROM {table})"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_date_range_data(self, table, start_date, end_date, count=9999):
        query = f"SELECT * FROM {table} WHERE Date_Time >= '{start_date}' AND Date_Time <= '{end_date}'"
        self.cursor.execute(query)
        return self.cursor.fetchmany(count)

    def get_last_week_data(self, table, count=9999):
        end_date = date.today()
        start_date = (end_date - timedelta(days=7))
        query = f"SELECT * FROM {table} WHERE Date_Time >= '{start_date}' AND Date_Time <= '{end_date}'"

        self.cursor.execute(query)
        return self.cursor.fetchmany(count)

