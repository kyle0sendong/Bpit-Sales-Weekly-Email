from datetime import date, timedelta


def get_date_today():
    return date.today()


def get_last_week_date():
    date_time = get_date_today()
    custom_date = (date_time - timedelta(days=7))
    return custom_date


def convert_datetime_string(datetime):
    date_format = "%B %d, %Y. %H:%M:%S"
    return datetime.strftime(date_format)


def convert_date_string(datetime):
    date_format = "%B %d, %Y"
    return datetime.strftime(date_format)


def convert_month_day_string(datetime):
    date_format = "%B %d"
    return datetime.strftime(date_format)


def get_7_day_list() -> list:
    date_now = date.today()-timedelta(days=1)
    date_list = []
    for i in range(7):
        date_list.append(date_now.strftime('%b %d'))
        date_now = date_now - timedelta(days=1)

    return date_list
